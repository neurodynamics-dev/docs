#!/usr/bin/env python3
"""
Gera catalogo/data.js e catalogo/neurodynamics-data.json a partir de:
  1. controle/NRO-PUB-001.xlsx            -> status, classe, autoria, revisões
  2. controle/NRO-PUB-001_metadados.xlsx  -> objetivo, template, projeto, relações

Resolve os caminhos relativos a este script, então funciona de qualquer cwd:
  pip install openpyxl
  python controle/build_data.py
"""
import os, sys, json, datetime, openpyxl

BASE = os.path.dirname(os.path.abspath(__file__))          # .../controle
REPO = os.path.dirname(BASE)                                # raiz do repo
OUT  = os.path.join(REPO, "docs")

CONTROLE  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "NRO-PUB-001.xlsx")
METADADOS = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "NRO-PUB-001_metadados.xlsx")

SET = {
    "PUB": {"nome": "Pública", "desc": "Governança do próprio sistema documental."},
    "PES": {"nome": "Pessoas", "desc": "Admissão, desligamento, políticas e registros de membros."},
    "PRO": {"nome": "Projetos", "desc": "Ciclo de vida técnico: requisitos, design, validação, riscos."},
    "CLI": {"nome": "Clínico", "desc": "Departamento clínico."},
    "REL": {"nome": "Relações Institucionais", "desc": ""},
    "DIR": {"nome": "Diretoria", "desc": "Estatuto, regimento e governança da equipe."},
    "MKT": {"nome": "Marketing", "desc": "Comunicação, redes e exposição pública."},
}

def fmt(v):
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime("%d/%m/%Y")
    return ("" if v is None else str(v)).strip()

wb = openpyxl.load_workbook(CONTROLE, data_only=True)
docs, by = [], {}
for name in wb.sheetnames:
    setor = name.split("-")[1]
    ws = wb[name]
    for r in range(3, ws.max_row + 1):
        code = ws.cell(r, 1).value
        if not code:
            continue
        d = dict(code=str(code).strip(), setor=setor, nome=fmt(ws.cell(r, 2).value),
                 status=fmt(ws.cell(r, 3).value), tipo=fmt(ws.cell(r, 4).value),
                 subtipo=fmt(ws.cell(r, 5).value), classe=fmt(ws.cell(r, 6).value),
                 autor=fmt(ws.cell(r, 7).value), data_autor=fmt(ws.cell(r, 8).value),
                 revisor=fmt(ws.cell(r, 9).value), data_rev=fmt(ws.cell(r, 10).value),
                 objetivo="", template_url="", projeto="", seriado=False, escopo_serie="")
        docs.append(d); by[d["code"]] = d

md = openpyxl.load_workbook(METADADOS, data_only=True)
ws = md["Metadados"]
head = {fmt(c.value).upper(): i for i, c in enumerate(ws[2], 1)}
def col(h):
    for k, i in head.items():
        if h in k:
            return i
    return None
c_code, c_obj, c_tmpl, c_proj = col("CÓDIGO"), col("OBJETIVO"), col("TEMPLATE"), col("PROJETO")
c_ser, c_esc = col("SERIADO"), col("ESCOPO")
for r in range(3, ws.max_row + 1):
    code = ws.cell(r, c_code).value if c_code else None
    if not code:
        continue
    code = str(code).strip()
    if code in by:
        if c_obj:  by[code]["objetivo"] = fmt(ws.cell(r, c_obj).value)
        if c_tmpl: by[code]["template_url"] = fmt(ws.cell(r, c_tmpl).value)
        if c_proj: by[code]["projeto"] = fmt(ws.cell(r, c_proj).value)
        if c_ser:  by[code]["seriado"] = fmt(ws.cell(r, c_ser).value).upper() == "SIM"
        if c_esc:
            e = fmt(ws.cell(r, c_esc).value).upper()
            by[code]["escopo_serie"] = e if e in ("DEPARTAMENTO", "PROJETO") else ""

# séries (serial numbers) — aba opcional
instancias = []
if "Séries" in md.sheetnames:
    sw = md["Séries"]
    for r in range(3, sw.max_row + 1):
        sn = fmt(sw.cell(r, 1).value)
        pn = fmt(sw.cell(r, 2).value)
        if not sn or not pn:
            continue
        num = sw.cell(r, 4).value
        instancias.append({"sn": sn, "pn": pn, "escopo": fmt(sw.cell(r, 3).value).upper(),
                           "numero": int(num) if isinstance(num, (int, float)) else fmt(num),
                           "titulo": fmt(sw.cell(r, 5).value), "data": fmt(sw.cell(r, 6).value),
                           "autor": fmt(sw.cell(r, 7).value), "status": fmt(sw.cell(r, 8).value).upper() or "EMITIDO",
                           "arquivo": fmt(sw.cell(r, 9).value), "nota": fmt(sw.cell(r, 10).value)})

rl = md["Relações"]
relacoes = []
for r in range(3, rl.max_row + 1):
    de, tipo, para = fmt(rl.cell(r, 1).value), fmt(rl.cell(r, 3).value), fmt(rl.cell(r, 4).value)
    if de and para and tipo:
        relacoes.append({"de": de, "tipo": tipo.upper(), "para": para, "nota": fmt(rl.cell(r, 6).value)})

# projetos registrados (edite aqui ao abrir novos projetos)
PROJETOS = [{"id": "EEGLSL", "nome": "EEG/LSL"}]

data = {"_meta": {"fonte_controle": os.path.basename(CONTROLE), "gerado": datetime.date.today().isoformat()},
        "setores": SET, "projetos": PROJETOS, "documentos": docs,
        "relacoes": relacoes, "instancias": instancias}

os.makedirs(OUT, exist_ok=True)
json.dump(data, open(os.path.join(OUT, "neurodynamics-data.json"), "w"), ensure_ascii=False, indent=2)
with open(os.path.join(OUT, "data.js"), "w") as f:
    f.write("// Gerado por build_data.py. Não editar à mão.\n")
    f.write("window.NEURO_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")

# injeta os dados embutidos no index.html (para funcionar via duplo-clique e no Pages)
import re
idx = os.path.join(OUT, "index.html")
if os.path.exists(idx):
    html = open(idx, encoding="utf-8").read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = re.sub(r'(<script id="nd-data" type="application/json">).*?(</script>)',
                  lambda m: m.group(1) + payload + m.group(2), html, flags=re.S)
    open(idx, "w", encoding="utf-8").write(html)
    print("index.html: dados embutidos")

print(f"OK · {len(docs)} documentos · {len(relacoes)} relações · {len(instancias)} séries -> docs/data.js")
