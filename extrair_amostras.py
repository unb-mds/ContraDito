import httpx
import os

BASE = "https://dadosabertos.camara.leg.br/api/v2"
HEADERS = {"Accept": "application/xml"}
os.makedirs("amostras", exist_ok=True)

# ── AMOSTRA 1: Ementa da proposição ──────────────────────────────
r_prop = httpx.get(
    f"{BASE}/proposicoes",
    params={"numero": "2630", "ano": "2020", "itens": "1"},
    headers=HEADERS,
    timeout=30
)
with open("amostras/ementa_proposicao.xml", "w", encoding="utf-8") as f:
    f.write(r_prop.text)
print("✔ ementa_proposicao.xml salvo")

# ── AMOSTRA 2: Discursos de um deputado ──────────────────────────
r_disc = httpx.get(
    f"{BASE}/deputados/74646/discursos",
    params={"dataInicio": "2023-01-01", "dataFim": "2023-12-31"},
    headers=HEADERS,
    timeout=30
)
with open("amostras/discursos_deputado.xml", "w", encoding="utf-8") as f:
    f.write(r_disc.text)
print("✔ discursos_deputado.xml salvo")