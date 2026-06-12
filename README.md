# Neurodynamics · Controle de Documentos

Sistema de gestão documental da equipe (estilo PLM) sobre o GitHub.
Os arquivos e o fluxo de aprovação vivem **neste repositório privado**; um
**catálogo** estático (só metadados) é publicado no GitHub Pages.

## O que tem aqui

```
.
├── PUB/ PES/ PRO/ CLI/ MKT/ DIR/ REL/   arquivos por setor (Público + Controlado)
├── controle/
│   ├── NRO-PUB-001.xlsx                  matriz de controle (fonte da verdade)
│   ├── NRO-PUB-001_metadados.xlsx        objetivo / template / relações
│   └── build_data.py                     gera o catálogo
├── docs/
│   ├── index.html                        o site (duas interfaces)
│   └── data.js                           gerado — não editar à mão
├── .github/
│   ├── CODEOWNERS                         quem aprova cada setor
│   ├── pull_request_template.md
│   └── workflows/build-catalog.yml        regenera + publica o catálogo
├── FLUXO.md                              o fluxo de aprovação em detalhe
├── MIGRACAO.md                           como trazer os arquivos do Drive
└── .gitignore                            barra Confidencial/segredos
```

## Início rápido

```bash
# 1. dentro da pasta do repo
git init -b main
git add .
git commit -m "Estrutura inicial do controle de documentos"

# 2. crie o repo PRIVADO no GitHub (org Neurodynamics) e conecte
git remote add origin git@github.com:neurodynamics/documentos.git
git push -u origin main
```

Depois, no GitHub:
1. **Settings → Pages → Source: GitHub Actions** (publica o catálogo).
2. **Settings → Branches** → ruleset na `main`: *Require a pull request*,
   *Require approvals (1)*, **Require review from Code Owners**. Ver `FLUXO.md`.
3. **Organization → Teams**: crie `diretoria`, `mantenedores`, `aprovadores-*`
   e dê acesso de escrita ao repo. Ajuste o `.github/CODEOWNERS` se usar usuários.
4. Traga os arquivos do Drive seguindo `MIGRACAO.md`.

## Atualizar o catálogo

```bash
pip install openpyxl
python controle/build_data.py        # regenera docs/data.js
```

Prévia local: abra `docs/index.html` no navegador (lê `data.js` via `<script>`).

## Leia também
- **FLUXO.md** — ciclo de vida (rascunho → submeter → aprovar → vigente) e proteção de branch.
- **MIGRACAO.md** — passo a passo do Drive para o repositório.
