import os
import json
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from github import Github, Auth

def main():
    token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("GITHUB_REPOSITORY", "unb-mds/2026.1-ContraDito")
    
    # Base structure
    metrics = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": repo_name,
        "issues_per_week": [],
        "commit_message_histogram": [],
        "coauthors_per_week": [],
        "commit_heatmap": [],
        "top_committers": [],
        "top_pr_authors": [],
        "top_issue_contributors": [],
        "pull_requests_time_to_merge": [],
        "code_review_matrix": [],
        "lead_time_issues_by_label": [],
        "code_churn_per_week": [],
        "commit_types_distribution": [],
        "bus_factor_risk": []
    }
    
    if not token:
        print("GITHUB_TOKEN não encontrado. Gerando dados mockados para teste local.")
        # Se não houver token, manter os arrays vazios (ou usar o mock)
        output_path = os.path.join(os.path.dirname(__file__), "..", "docs", "productivity", "metrics.json")
        with open(output_path, "w") as f:
            json.dump(metrics, f, indent=2)
        return

    print(f"Conectando ao repositório {repo_name}...")
    auth = Auth.Token(token)
    g = Github(auth=auth)
    repo = g.get_repo(repo_name)
    
    # 1. Commits Analysis (from 'develop' branch)
    print("Processando commits da branch develop (isso pode levar alguns segundos)...")
    try:
        commits = repo.get_commits(sha="develop")
    except Exception as e:
        print(f"Erro ao buscar branch 'develop', tentando default: {e}")
        commits = repo.get_commits()
        
    commit_counts = defaultdict(int)
    commit_types = defaultdict(int)
    msg_lengths = {"0-20": 0, "21-50": 0, "51-100": 0, "101-200": 0, "200+": 0}
    heatmap = defaultdict(int)
    coauthors_weekly = defaultdict(int)
    churn_weekly = defaultdict(lambda: {"additions": 0, "deletions": 0, "modifications": 0})
    
    # Fetching only the last 300 commits to avoid rate limiting for now
    count = 0
    for commit in commits:
        if count > 300:
            break
        count += 1
        
        # Committer
        author = commit.author
        if author:
            commit_counts[author.login] += 1
            
        # Commit message types (conventional commits)
        msg = commit.commit.message
        msg_lower = msg.lower()
        if msg_lower.startswith('feat'): commit_types['feat'] += 1
        elif msg_lower.startswith('fix'): commit_types['fix'] += 1
        elif msg_lower.startswith('docs'): commit_types['docs'] += 1
        elif msg_lower.startswith('chore'): commit_types['chore'] += 1
        elif msg_lower.startswith('refactor'): commit_types['refactor'] += 1
        elif msg_lower.startswith('test'): commit_types['test'] += 1
        else: commit_types['other'] += 1

        # Message Histogram
        l = len(msg)
        if l <= 20: msg_lengths["0-20"] += 1
        elif l <= 50: msg_lengths["21-50"] += 1
        elif l <= 100: msg_lengths["51-100"] += 1
        elif l <= 200: msg_lengths["101-200"] += 1
        else: msg_lengths["200+"] += 1

        # Heatmap
        dt = commit.commit.author.date
        day = dt.weekday()
        hour = dt.hour
        heatmap[(day, hour)] += 1

        # Co-authors
        week = dt.strftime("%Y-W%V")
        coauthors_weekly[week] += msg_lower.count("co-authored-by:")
        
        # Code Churn (Limited to first 50 commits due to API constraints)
        if count <= 50 and commit.stats:
            churn_weekly[week]["additions"] += commit.stats.additions
            churn_weekly[week]["deletions"] += commit.stats.deletions
            churn_weekly[week]["modifications"] += commit.stats.total - commit.stats.additions - commit.stats.deletions

    for range_k, c in msg_lengths.items():
        if c > 0:
            metrics["commit_message_histogram"].append({"range": range_k, "count": c})
            
    for (day, hour), c in heatmap.items():
        metrics["commit_heatmap"].append({"day": day, "hour": hour, "count": c})
        
    for week, c in sorted(coauthors_weekly.items()):
        metrics["coauthors_per_week"].append({"week": week, "count": c})
        
    for week, data in sorted(churn_weekly.items()):
        metrics["code_churn_per_week"].append({"week": week, **data})

    for username, c in sorted(commit_counts.items(), key=lambda item: item[1], reverse=True)[:10]:
        metrics["top_committers"].append({
            "username": username,
            "name": username,
            "commits": c
        })
        
    for c_type, c in commit_types.items():
        if c > 0:
            metrics["commit_types_distribution"].append({
                "type": c_type,
                "count": c
            })

    # 2. Issues Analysis (Open/Closed)
    print("Processando issues (isso pode levar alguns segundos)...")
    issues = repo.get_issues(state='all')
    issues_by_week = defaultdict(lambda: {"opened": 0, "closed": 0})
    issue_contributors = defaultdict(lambda: {"opened": 0, "closed": 0, "total": 0})
    lead_time_by_label = defaultdict(list)
    
    count = 0
    for issue in issues:
        if count > 200:
            break
        count += 1
        
        # Evitar N+1 API calls verificando a URL em vez de issue.pull_request
        if "/pull/" in issue.html_url:
            continue # Ignore PRs here
            
        week = issue.created_at.strftime("%Y-W%V")
        issues_by_week[week]["opened"] += 1
        
        if issue.user:
            issue_contributors[issue.user.login]["opened"] += 1
            issue_contributors[issue.user.login]["total"] += 1
        
        if issue.state == 'closed' and issue.closed_at:
            close_week = issue.closed_at.strftime("%Y-W%V")
            issues_by_week[close_week]["closed"] += 1
            if issue.closed_by:
                issue_contributors[issue.closed_by.login]["closed"] += 1
                issue_contributors[issue.closed_by.login]["total"] += 1
                
            # Lead time por label
            days_to_close = (issue.closed_at - issue.created_at).total_seconds() / 86400.0
            for label in issue.labels:
                lead_time_by_label[label.name].append(days_to_close)

    for week, counts in sorted(issues_by_week.items())[-10:]:
        metrics["issues_per_week"].append({
            "week": week,
            "opened": counts["opened"],
            "closed": counts["closed"]
        })
        
    for username, counts in sorted(issue_contributors.items(), key=lambda item: item[1]['total'], reverse=True)[:10]:
        metrics["top_issue_contributors"].append({
            "username": username,
            "name": username,
            "opened": counts["opened"],
            "closed": counts["closed"],
            "total": counts["total"]
        })
        
    for label_name, times in lead_time_by_label.items():
        if times:
            avg_days = sum(times) / len(times)
            metrics["lead_time_issues_by_label"].append({
                "label": label_name,
                "avg_days_to_close": round(avg_days, 1)
            })

    # 3. Pull Requests Analysis
    print("Processando PRs (isso pode levar alguns segundos)...")
    prs = repo.get_pulls(state='all')
    pr_authors = defaultdict(int)
    pr_merge_times_by_week = defaultdict(list)
    
    count = 0
    for pr in prs:
        if count > 100:
            break
        count += 1
        
        pr_author = pr.user.login if pr.user else "unknown"
        if pr.user:
            pr_authors[pr_author] += 1
            
        if pr.merged_at and pr.created_at:
            week = pr.merged_at.strftime("%Y-W%V")
            hours = (pr.merged_at - pr.created_at).total_seconds() / 3600.0
            pr_merge_times_by_week[week].append(hours)
            
    for username, c in sorted(pr_authors.items(), key=lambda item: item[1], reverse=True)[:10]:
        metrics["top_pr_authors"].append({
            "username": username,
            "name": username,
            "prs_opened": c
        })

    for week, times in sorted(pr_merge_times_by_week.items())[-10:]:
        if times:
            avg_hours = sum(times) / len(times)
            metrics["pull_requests_time_to_merge"].append({
                "week": week,
                "avg_hours": round(avg_hours, 1)
            })

    # Bus Factor Approximation
    if metrics["top_committers"]:
        total_commits_counted = sum(c["commits"] for c in metrics["top_committers"])
        if total_commits_counted > 0:
            for top_dev in metrics["top_committers"]:
                ownership = (top_dev["commits"] / total_commits_counted) * 100
                metrics["bus_factor_risk"].append({
                    "module": "Repositório Inteiro",
                    "top_contributor": top_dev["username"],
                    "ownership_percentage": round(ownership, 1)
                })

    output_path = os.path.join(os.path.dirname(__file__), "..", "docs", "productivity", "metrics.json")
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Métricas coletadas e salvas em {output_path}")

if __name__ == "__main__":
    main()
