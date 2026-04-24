import re

def limpar_texto_discurso(texto_bruto: str) -> str:
    """
    Higieniza discursos parlamentares (Câmara e Senado) para 
    otimizar a geração de embeddings semânticos.
    """
    if not texto_bruto:
        return ""

    # 1. Remove tags HTML residuais.
    texto = re.sub(r'<[^>]+>', ' ', texto_bruto)

    # 2. Remove prefixos de orador genéricos e variações com partidos/UF
    texto = re.sub(r'^(O SR\.|A SRA\.|O SENHOR|A SENHORA)[A-ZÁÉÍÓÚÀÂÊÔÃÕÇ\s\.\-\(\)]+-\s*', '', texto, flags=re.IGNORECASE)

    # 3. Remove notas taquigráficas e reações do plenário
    texto = re.sub(r'\[.*?\]', ' ', texto)  
    texto = re.sub(r'\(.*?\)', ' ', texto) 

    # 4. Remove jargões de protocolo do Congresso
    termos_inuteis = [
        r'Sr\. Presidente',
        r'Sras\. e Srs\. Deputados',
        r'Sras\. e Srs\. Senadores',
        r'peço a palavra',
        r'concedo a palavra',
        r'pela ordem'
    ]
    for termo in termos_inuteis:
        texto = re.sub(termo, '', texto, flags=re.IGNORECASE)

    # 5. Higienização final: remove espaços duplicados e quebras de linha isoladas
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto