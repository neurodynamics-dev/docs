# Fluxo de aprovação (PLM sobre GitHub)

Como o ciclo de vida dos documentos (rascunho → submissão → revisão → vigência)
roda usando os mecanismos nativos do GitHub.

## Estrutura do repositório (privado)

```
documentos/                 ← repositório PRIVADO
├── PUB/  PES/  PRO/  CLI/  MKT/  DIR/  REL/   ← arquivos por setor (Público + Controlado)
├── controle/
│   ├── NRO-PUB-001.xlsx                 ← matriz de controle
│   ├── NRO-PUB-001_metadados.xlsx       ← objetivo / template / relações
│   └── build_data.py                    ← gera o data.js
├── catalogo/
│   ├── index.html                       ← o site (só metadados)
│   └── data.js                          ← gerado pelo build
├── .github/
│   ├── CODEOWNERS                        ← quem aprova cada setor
│   ├── pull_request_template.md
│   └── workflows/build-catalog.yml       ← regenera + publica o catálogo
└── README.md
```

> **Confidencial** (Quadro de Pessoal, Contas Digitais) **não entra no repositório.**
> Permanece no Drive com acesso restrito; o catálogo apenas aponta o link.

## Público × Privado — a regra de ouro

| | Repo público | Repo privado |
|---|---|---|
| Quem lê os arquivos | Mundo todo | Só membros (logados) |
| Adequado para | Apenas Público | Público + Controlado |
| Pages (o site) | Público | Despublicado no Free; público no Pro; privado só no Enterprise |

**Recomendado:** repo **privado** para os arquivos; catálogo no Pages **público** mostrando
só metadados, com os botões "Abrir arquivo" linkando para o `blob` do repo privado
(o GitHub libera só para membros logados) ou para o Drive (Confidencial).

## Mapeamento do ciclo de vida

| Etapa (PLM) | No GitHub |
|---|---|
| RASCUNHO | Branch de trabalho (`rev/NRO-PRO-004-revC`) ou PR em *draft* |
| Submeter para aprovação | Abrir o Pull Request → CODEOWNERS solicita o time do setor |
| Revisão | Comentários / "Request changes" no PR |
| Aprovar e publicar (EM VIGÊNCIA) | Aprovação do CODEOWNER + **merge** na `main` |
| Histórico de revisões (Rev. A–P) | Histórico do Git; opcionalmente uma *tag* por versão |
| Grupos de usuário | GitHub **Teams** (referenciados no CODEOWNERS) |

### Passo a passo de uma nova versão
1. Crie um branch: `git switch -c rev/NRO-PRO-004-revC`
2. Atualize o arquivo em `PRO/`, o `NRO-PUB-001` e a planilha de metadados se preciso.
3. Abra o PR (o template é preenchido automaticamente). O CODEOWNERS marca o time aprovador.
4. O time revisa. Mudanças? Novos commits no mesmo branch.
5. Aprovado → **merge**. A versão na `main` passa a ser a vigente, e a Action regenera o catálogo.
6. (Opcional) `git tag NRO-PRO-004-revC && git push --tags` para fixar a revisão.

## Configurar a proteção (uma vez)

**Settings → Branches → Add branch ruleset** (ou *Branch protection rule* clássico) na `main`:
- ✅ **Require a pull request before merging**
- ✅ **Require approvals** (mínimo 1)
- ✅ **Require review from Code Owners**  ← liga o CODEOWNERS como gate
- ✅ (opcional) **Require status checks to pass** → selecione o job do build
- ✅ **Do not allow bypassing the above settings** (vale também para admins)

**Settings → Pages → Source: GitHub Actions** (para o workflow publicar o catálogo).

### Times (org) e o CODEOWNERS
- Crie os times em **Organization → Teams**: `diretoria`, `mantenedores`,
  `aprovadores-projetos`, `aprovadores-pessoas`, `aprovadores-clinico`, `aprovadores-marketing`.
- Adicione os membros e dê ao time **acesso de escrita** no repositório.
- Sem organização (conta pessoal)? Times não existem — use **usuários** no CODEOWNERS
  (ver comentário no fim do arquivo). O gate de Code Owners exige plano que suporte a regra.

## Por que isso satisfaz o modelo de permissões

- **Visualizar** = ter acesso de leitura ao repo privado (ou ver o metadado no Pages).
- **Submeter** = abrir PR (qualquer membro com acesso).
- **Aprovar e substituir a versão** = aprovar + merge, restrito ao CODEOWNER do setor.

A maquete visual do site (seletor "Logado como") continua útil como documentação do
modelo; a **aplicação real** é a combinação acima.
