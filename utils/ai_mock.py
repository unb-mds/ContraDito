def gerar_embedding_mock(texto_limpo: str) -> list[float]:
    """
    Mock temporário do motor SBERT (paraphrase-multilingual-mpnet-base-v2).
    Retorna um vetor nulo de 768 dimensões para não bloquear a pipeline de ETL.
    """
    if not texto_limpo:
        return []
        
    # Opcional: print para você ver o mock trabalhando no terminal
    print(f"  [IA] Gerando vetor mockado (768d) para texto de {len(texto_limpo)} chars...")
    
    # Retorna uma lista com 768 posições preenchidas com 0.0
    return [0.0] * 768