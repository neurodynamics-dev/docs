# Migração do Drive para o repositório

Passo a passo para trazer os arquivos do Drive, decidindo o que entra no Git e o
que permanece só no Drive. Faça uma vez; depois, novas versões entram por Pull Request.

## Regra de decisão (por classe)

| Classe do documento | Vai para o repositório? | Onde fica o arquivo | Link no catálogo (coluna TEMPLATE) |
|---|---|---|---|
| **Público** | Sim | pasta do setor (`PRO/`, `PES/`…) | `github.com/<org>/documentos/blob/main/…` |
| **Controlado** | Sim (repo privado) | pasta do setor | mesmo link `blob` (só membros logados abrem) |
| **Confidencial** | **Não** | permanece no Drive, acesso restrito | link do Drive |
| Status **INEXISTENTE** | Não há arquivo | — | deixar em branco |

> Confidenciais conhecidos hoje: **NRO-PES-005** (Quadro de Pessoal) e
> **NRO-DIR-003** (Contas Digitais). O `.gitignore` já barra esses códigos por segurança.

## Passos

### 1. Baixar do Drive
No Drive, selecione os arquivos (ou a pasta) → **Baixar**. Pastas vêm como `.zip`; descompacte.

### 2. Separar Confidencial
Tire de lado **NRO-PES-005** e **NRO-DIR-003** (e qualquer outro Confidencial).
Eles **não** sobem. Anote o link de cada um no Drive para usar no passo 5.

### 3. Nomear e distribuir por setor
Renomeie cada arquivo começando pelo código e coloque na pasta do setor. Ex.:
```
PRO/NRO-PRO-004 USRS.xlsx
PES/NRO-PES-006 Procedimento de Admissão.docx
DIR/NRO-DIR-001 Estatuto.pdf
```
Documentos **INEXISTENTE** não têm arquivo — pule (continuam no catálogo como placeholder).

### 4. Primeiro commit dos arquivos
```bash
git add PUB PES PRO CLI MKT DIR REL
git commit -m "Importa arquivos Público e Controlado do Drive"
git push
```

### 5. Coletar os links e preencher a coluna TEMPLATE
Na planilha `controle/NRO-PUB-001_metadados.xlsx`, aba **Metadados**, coluna **TEMPLATE**:
- **No repo:** abra o arquivo no GitHub, copie a URL da barra (formato
  `https://github.com/<org>/documentos/blob/main/PRO/NRO-PRO-004%20USRS.xlsx`).
- **No Drive (Confidencial):** copie o link de compartilhamento restrito do Drive.

Cole o link na linha do código correspondente.

### 6. Regenerar o catálogo
```bash
pip install openpyxl
python controle/build_data.py
git add controle/NRO-PUB-001_metadados.xlsx catalogo/data.js
git commit -m "Preenche links de arquivo (TEMPLATE)"
git push
```
A partir daí os botões "Abrir / baixar versão atual" funcionam para todos os documentos.

### 7. Conferir
- Catálogo no Pages mostra os 45 documentos e as relações.
- Clicar num arquivo do repo logado como membro → abre; deslogado/externo → 404 (acesso protegido).
- Confidenciais abrem só pelo link do Drive, gated lá.

## Daqui pra frente
Nada de arrastar arquivo direto na `main`. Toda atualização é por **Pull Request**
(ver `FLUXO.md`): branch → PR → revisão do time dono → merge = nova versão vigente.
