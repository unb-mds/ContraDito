import xml.etree.ElementTree as ET
import json

tree = ET.parse("amostras/discursos_deputado.xml")
root = tree.getroot()

discurso = root.find(".//discurso")

if discurso is not None:
    data  = discurso.findtext("dataHoraInicio", default="")
    texto = discurso.findtext("transcricao", default="")
else:
    data = ""
    texto = ""

# Como a API de discursos não traz o nome do deputado, colocamos manualmente
# os dados do Aécio Neves, já que usamos o ID 74646 na extração.
contrato = {
    "deputado": {
        "id_camara": "74646",
        "nome":      "Aécio Neves",
        "partido":   "PSDB",
        "estado":    "MG"
    },
    "contexto_original": {
        "tipo_documento": "discurso",
        "data_evento":    data,
        "texto_extraido": texto
    }
}

# 5. Salva como JSON para passar ao Luiz
with open("amostras/amostra_para_luiz.json", "w", encoding="utf-8") as f:
    json.dump(contrato, f, ensure_ascii=False, indent=2)

print("✔ amostra_para_luiz.json salvo")
print(f"  Deputado : Aécio Neves (PSDB/MG)")
print(f"  Data     : {data}")
print(f"  Texto    : {texto[:80]}..." if len(texto) > 80 else f"  Texto: {texto}")