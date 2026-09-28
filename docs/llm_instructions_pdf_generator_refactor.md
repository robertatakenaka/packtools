# Instruções para LLM: reorganização do gerador de PDF

Contexto: `packtools/sps/formats/pdf/` gera PDF a partir de XML SPS/JATS
(XML → estrutura intermediária → DOCX via python-docx → PDF via LibreOffice).
O código cresceu somando correções pontuais num arquivo único de extração
(`pipeline/xml.py`) e precisa ser reorganizado. Há PRs abertos alterando
esses mesmos arquivos, então **o estado do código pode ser diferente do que
este documento descreve**. Trate nomes de funções, arquivos e números citados
aqui como referência de intenção, não como fatos: confira sempre no código
antes de agir.

A decisão de manter Python (e não migrar para XSLT) já foi tomada. Não
reabra essa discussão.

---

## 1. Antes de começar qualquer etapa

1. **Verifique o estado dos PRs relacionados à épica** (reorganização da
   extração do PDF). Use `gh pr list` / `gh pr view` e a issue da épica.
   Se houver PR aberto que altera os mesmos arquivos da etapa que você vai
   fazer, **pare e avise**: não comece a etapa, não faça rebase de PR alheio,
   não altere PR aberto.
2. **Leia o código atual** dos módulos envolvidos na etapa e o arquivo
   `docs/pdf_generator_architecture.md` (se já existir, ele prevalece sobre
   este documento).
3. **Rode a suíte** `tests/sps/formats/pdf/` e registre o resultado de
   partida. Se já houver falhas, reporte-as; não as corrija junto com a
   reorganização.
4. **Gere a saída de referência** (PDFs das fixtures do corpus definido na
   Fase 0) com o código *antes* da sua mudança, para comparar depois.

---

## 2. Princípios

- **Uma responsabilidade por módulo.** Metadados, corpo, tabela, figura,
  referências, citação, layout e conversão OOXML não convivem no mesmo
  arquivo.
- **Mover não é mudar.** Nas etapas de reorganização, a saída do gerador deve
  ser equivalente. Se perceber um bug durante a mudança, registre (issue ou
  nota no PR) e não corrija na mesma etapa.
- **Um PR por etapa, pequeno e sequencial.** Cada PR parte do resultado do
  anterior já mergeado.
- **Siga o estilo do código existente**: nomes, docstrings, densidade de
  comentários, idioma dos comentários (o código mistura português e inglês;
  mantenha o do trecho que estiver editando).
- **Preserve o conhecimento acumulado.** Comentários que explicam
  peculiaridades do LibreOffice ou referenciam issues (`#13xx`) vão junto
  com o código que eles explicam.

---

## 3. Arquitetura alvo (intenção)

```
packtools/sps/formats/pdf/
├── extract/        # XML -> estrutura intermediária para o render (sem python-docx)
│   ├── inline/     # ÚNICO dono do conteúdo misto (ver seção 4)
│   ├── metadata    # título, doi, contribs, abstract, keywords, rodapé...
│   ├── body        # sec / p / list
│   ├── tables      # lê table-wrap; junta com layout/
│   ├── figures
│   ├── references
│   ├── acknowledgments
│   ├── supplementary_material
│   └── citation    # caminho final definido na Fase 0 (alinhar com a issue de citação)
├── layout/         # decisões de layout a partir de dados JÁ EXTRAÍDOS (nunca XML)
├── ooxml/          # MathML -> OMML, namespaces OOXML
├── pipeline/       # orquestração (docx.py)
├── renderer/docx/  # emissão DOCX; style.py = única fonte dos nomes 'SCL *'
└── utils/
```

A granularidade exata (arquivo vs. subpacote) e os nomes finais são
decididos na Fase 0. Se o documento de arquitetura divergir desta árvore,
siga o documento.

### Regras de dependência (verificáveis)

- `extract/` não importa `docx` (python-docx), `pipeline/` nem `renderer/`.
- `renderer/` não importa `pipeline/`.
- `layout/` não importa `extract/`, `pipeline/` nem `renderer/`.
- Constantes ficam no módulo dono do assunto; nomes de estilo `SCL *` só em
  `renderer/docx/style.py`.
- Cada arquivo de teste espelha um módulo.

Verifique com `grep` antes de abrir o PR.

---

## 4. Conteúdo misto: reuso e recursão

Elementos inline (`italic`, `bold`, `sup`, `sub`, `sc`, `inline-formula`,
`inline-graphic`, `xref`, `ext-link`, …) aparecem em muitos contextos:
título, afiliação, parágrafo, item de lista, legenda, célula de tabela,
referência, nota. O tratamento de cada elemento deve existir **uma vez** e
ser reaproveitado em todos os contextos, de forma recursiva, no espírito do
`xsl:apply-templates`.

Contrato de `extract/inline/`:

- **Dispatcher por tag**: um registro `tag -> tratador`. Adicionar suporte a
  um elemento = registrar um tratador, sem editar uma cadeia de `if/elif`.
- **Tratador** recebe `(node, ctx)` e devolve uma lista de segmentos.
- **Regra padrão** para tag não registrada: descer nos filhos.
- **Ignorar** uma tag = tratador que devolve lista vazia (substitui
  parâmetros do tipo `skip_tags`).
- **`tail`** é tratado só pelo dispatcher, nunca pelos tratadores.
- **Contexto imutável** com o estilo ativo (italic/bold/sup/sub…), o modo
  (`title`, `body`, `table-cell`, `caption`, `ref`, `footer`…) e dados
  auxiliares (idioma, diretório de assets). Tratadores derivam um novo
  contexto em vez de alterar o atual.
- **Comportamento dependente de contexto** (ex.: `xref` de nota no título)
  é decidido pelo `ctx.mode` dentro do tratador, não por funções duplicadas.
- **Formato de saída**: os mesmos dicionários de segmento usados hoje pelo
  renderer. Não introduza um novo modelo de dados nesta épica.
- **Normalização** de espaços e pontuação continua como pós-processamento
  único sobre a lista de segmentos (reaproveite a lógica existente).
- Blocos recursivos (`p`, `list`, `boxed-text`, `sec`, `disp-formula`)
  podem seguir o mesmo padrão; uma célula de tabela ou uma legenda deve
  reaproveitar os mesmos tratadores de bloco e inline.

Regra de uso: `itertext()` / `.text` só para valores atômicos (DOI, idioma,
ids, datas). Todo texto que pode conter marcação passa por `extract/inline/`.

Do lado do render, deve haver **um único ponto** que converte segmentos em
runs/OMML/imagens inline, usado por parágrafo, célula, legenda, cabeçalho,
rodapé e referência.

---

## 5. Etapas

A ordem importa. Cada etapa = uma issue + um PR. Adapte o conteúdo exato ao
estado do código no momento.

**Fase 0: documentar (sem código de produção).** Criar
`docs/pdf_generator_architecture.md` com: a árvore de módulos, as regras de
dependência, o fluxo tabela → layout, o contrato de `extract/inline/`, o
protocolo de comparação de saída (corpus, ferramenta, limiar), a decisão de
compatibilidade de imports de `pipeline/xml.py` (reexport com
`DeprecationWarning`, padrão já usado em `sps/models`, ou quebra declarada),
os caminhos finais de `citation` e `supplementary_material`, e a posição
sobre `packtools/sps/models` (eles devolvem texto/HTML serializado; o PDF
pode usá-los para localizar nós, mas o texto misto sai de `extract/inline/`).

**Fases de mudança de lugar (saída equivalente):**

1. Mover o que não depende da função central de extração do corpo:
   metadados, figuras, referências, agradecimentos. Remover código
   comprovadamente morto (confirme com `grep` em `packtools/` e `tests/`).
2. Mover a citação para o módulo definido na Fase 0.
3. Criar o módulo do corpo (sec/p/list) e isolar a ponte de fórmulas usando
   a assinatura de tratador `(node, ctx)`.
4. **Criar `extract/inline/`** reproduzindo *exatamente* o comportamento
   atual da montagem de segmentos. A função utilitária existente vira um
   wrapper. Testes: os atuais continuam verdes, mais testes unitários por
   tratador.
5. Separar tabela (leitura do XML) de layout (decisão sobre dados
   extraídos). A decisão de layout deixa de receber o nó XML e considera o
   `table-wrap` inteiro (todas as `<table>`).
6. Isolar a conversão OOXML de fórmulas em `ooxml/` e eliminar a
   dependência `renderer → pipeline`.
7. Centralizar nomes de estilo e constantes de layout; dividir os testes
   restantes por módulo.

Em cada fase com mudança de lugar: se a decisão da Fase 0 for manter
compatibilidade, atualize os reexports em `pipeline/xml.py`.

**Épica seguinte (muda a saída de propósito, fora desta épica):** aplicar
`extract/inline/` nos pontos que hoje achatam texto (título, afiliação,
legenda, célula, referência, nota), um grupo por PR, cada um com testes de
itálico/sup/sub/inline-formula/inline-graphic no contexto. Mudanças na API de
célula de tabela devem usar `extract/inline/`, e não parâmetros específicos
novos.

---

## 6. Critérios para abrir cada PR

- [ ] Suíte `tests/sps/formats/pdf/` verde (e o resto da suíte do projeto
      não piorou).
- [ ] Saída equivalente segundo o protocolo da Fase 0: mesmo número de
      páginas, texto extraído equivalente, diff visual dentro do limiar. Não
      compare PDFs byte a byte (o LibreOffice altera metadados).
- [ ] Regras de dependência verificadas com `grep`.
- [ ] Nenhuma mudança funcional misturada com mudança de lugar.
- [ ] Testes movidos junto com o código, espelhando o novo módulo.
- [ ] Descrição do PR: o que foi movido, de onde para onde, como a
      equivalência foi verificada, e o que ficou para depois.

---

## 7. Quando parar e perguntar

- Há PR aberto tocando os mesmos arquivos.
- O código atual não corresponde ao que este documento ou o documento de
  arquitetura supõem (função renomeada, módulo já criado em outro lugar).
- A equivalência de saída não fecha e a causa não é óbvia.
- Uma etapa exigiria mudança de comportamento para ser concluída.
- A decisão da Fase 0 sobre algum ponto ainda não foi tomada.

## 8. O que não fazer

- Não migrar para XSLT.
- Não alterar PRs abertos de outras pessoas.
- Não introduzir novo modelo de dados (dataclasses) nesta épica.
- Não mover a emissão DOCX de `pipeline/docx.py` para `renderer/` nesta épica.
- Não tornar o layout configurável por periódico aqui (issue própria).
- Não apagar comentários que explicam peculiaridades do LibreOffice ou
  referenciam issues.
