---
layout: post
lang: pt-BR
permalink: /posts/prompt-engineering/
title: "Prompt Engineering para desenvolvedores: como escrever instruções claras para IA"
seo_title: "Prompt Engineering para desenvolvedores | Marcelo Miyake"
date: 2026-09-17 00:00:00 -0300
categories: [Engineering]
tags: [prompt-engineering, ai, llm, coding, best-practices]
description: "Aprenda a escrever prompts eficazes para agentes de IA com escopo claro, contexto técnico, critérios de aceite e avaliação sistemática de resultados."
---

Quando você pede para um assistente de IA "criar uma tela de login", você deixa decisões críticas de arquitetura e produto em aberto: qual framework utilizar, como os tokens de autenticação serão armazenados, como os estados de erro devem ser exibidos e o que realmente define que a tarefa foi concluída. O modelo preencherá essas lacunas com suposições plausíveis, mas que frequentemente não se alinham ao padrão do seu projeto em produção.

**Prompt engineering** para desenvolvedores é a prática de estruturar instruções, contexto técnico e restrições para que assistentes de IA produzam código adequado à tarefa e ao repositório. Prompts mais claros reduzem ambiguidades, mas o código gerado ainda precisa de revisão e verificação.

Este é o primeiro artigo de uma série em seis partes sobre agentes de programação com IA — sistemas que leem arquivos de repositórios, executam comandos em terminal e propõem alterações validadas no código:

1. **Prompt Engineering** (este artigo): Escrita de instruções claras e testáveis.
2. [AI Gateways e roteamento de modelos](/posts/ai-gateway-routing/): Direcionamento de requisições e aplicação de políticas.
3. [Context Engineering](/posts/context-engineering/): Fornecendo o contexto certo de repositórios e serviços para agentes.
4. [Harness Engineering](/posts/harness-engineering/): Ferramentas seguras, sandboxes e ambientes de execução.
5. [Spec-Driven Development](/posts/spec-driven-development/): Planejando especificações e arquitetura antes de gerar código.
6. [Loop Engineering](/posts/loop-engineering/): Automatizando ciclos de feedback com testes e validação em runtime.

Ao longo de toda a série, usamos um exemplo prático recorrente: **adicionar suporte a código de desconto em um fluxo de checkout de e-commerce**.

---

## Quatro elementos de um prompt de programação útil {#four-elements-of-a-useful-coding-prompt}

Todo prompt de programação eficaz possui quatro pilares fundamentais:

### 1. Objetivo e escopo
{: id="1-goal-and-scope"}

Defina com precisão o comportamento desejado e a fronteira exata da alteração no código.

* **Prompt fraco:** "Melhore o checkout."
* **Prompt forte:** "Evite envios duplicados de pedidos quando o usuário clica no botão de checkout várias vezes consecutivas."

Para features complexas, peça ao agente para inspecionar o repositório primeiro e propor um plano dividido em etapas modulares, fáceis de revisar em um code review. Atribuir uma persona (como "Engenheiro Backend Sênior") pode ajustar levemente o vocabulário, mas nunca substitui requisitos técnicos objetivos, restrições e dados concretos.

### 2. Contexto relevante
{: id="2-relevant-context"}

Aponte diretamente para os arquivos, contratos de API e padrões que o modelo deve seguir.

* Indique os caminhos exatos dos arquivos: a implementação atual, uma feature similar de referência e o schema de contrato aplicável.
* Ao reportar bugs, inclua o comando exato executado, o stack trace completo e as variáveis de ambiente relevantes.

Se o seu agente possui ferramentas de acesso ao repositório (como busca em arquivos e listagem de diretórios), oriente-o a inspecionar esses arquivos antes de editar. Se você estiver usando uma interface tradicional de chat sem ferramentas integradas, forneça os trechos de código relevantes no próprio prompt. Nunca espere que a IA adivinhe APIs internas ou convenções não documentadas da sua equipe.

### 3. Restrições e comportamento esperado
{: id="3-constraints-and-expected-behavior"}

Explicite todas as restrições técnicas e arquiteturais logo no início:

* Versão da linguagem e runtime (por exemplo, Node.js 22, Python 3.12, Java 21).
* Dependências permitidas e bibliotecas proibidas (por exemplo, "Reutilize utilitários existentes; não instale novos pacotes npm").
* Interfaces públicas e requisitos de retrocompatibilidade.

Prefira descrever comportamentos observáveis em vez de adjetivos vagos como "código robusto", "seguro" ou "escalável". Por exemplo: "Se a requisição contiver um idempotency key já processado, retorne a resposta HTTP 200 em cache sem cobrar o gateway de pagamento novamente."

### 4. Critérios de aceitação e formato de entrega
{: id="4-acceptance-criteria-and-delivery-format"}

Os critérios de aceitação definem o que significa ter sucesso. O formato de entrega define como o resultado deve ser apresentado.

* **Critérios de aceitação:** "Todos os testes unitários existentes continuam passando, e novos testes cobrem entradas vazias, tokens expirados e timeouts de rede."
* **Formato de entrega:** "Exiba um git diff unificado, seguido pela lista de arquivos alterados, comandos executados e o relatório de testes."

Separar esses dois aspectos evita que o modelo gere uma resposta bem formatada na superfície, mas sem validação real de funcionamento.

---

## Exemplo: torne explícita uma política de validação {#example-make-a-validation-policy-explicit}

Veja um pedido comum e genérico de desenvolvimento:

```text
Escreva uma função que valide endereços de e-mail em TypeScript.
```

Esse prompt não define o tipo do input, o tratamento de espaços em branco, domínios internacionalizados ou formatos especiais. Pedir uma "regex 100% aderente à RFC 5322" geralmente gera uma expressão regular ilegível de 2.000 caracteres que ainda falha em regras de negócio básicas.

Em uma aplicação real de produção, você precisa de uma política de produto clara e testável:

```text
Tarefa: Crie a função isValidEmail(input: unknown): boolean como export nomeado.

Contexto:
- Inspecione os utilitários de validação existentes em src/utils/validation.ts.
- Reutilize a configuração do Jest e o TypeScript do projeto.

Política de produto:
- Retorne false para entradas que não sejam string (null, undefined, números, objetos).
- Rejeite strings vazias e qualquer espaço em branco no início, fim ou meio. Não faça trim automático.
- Parte local: Permita apenas letras ASCII, dígitos, pontos (.), underscores (_), sinais de mais (+) e hífens (-).
- Parte local: Não pode começar nem terminar com ponto, nem conter pontos consecutivos (..).
- Domínio: Exija exatamente um símbolo '@' e pelo menos dois labels de domínio não vazios.
- Labels de domínio: Devem conter apenas letras ASCII, dígitos e hífens, não podendo começar nem terminar com hífen.
- Rede: Rejeite qualquer outro caractere. Não execute chamadas de rede ou consultas DNS.

Exemplos para testes de aceitação:
- Válidos (true): "alex@example.com", "alex+shop@sub.example.com"
- Inválidos (false): null, 42, "", " alex@example.com", "alex..lee@example.com", "alex@localhost", "alex@-example.com"

Entrega:
- Implemente a função em src/utils/validation.ts e adicione os testes em src/utils/validation.test.ts.
- Execute a suíte de testes e valide todos os cenários de borda.
- Informe os arquivos modificados, os comandos executados, os resultados dos testes e premissas pendentes.
```

Com esse nível de clareza, qualquer desenvolvedor em code review ou ferramenta automatizada pode verificar se o código gerado atende fielmente aos requisitos.

---

## Erros comuns em prompts para desenvolvedores {#common-mistakes}

Fique atento a estas falhas recorrentes ao trabalhar com IA:

* **Instruções conflitantes:** Pedir "retorne apenas o código sem explicações" e ao mesmo tempo "explique os trade-offs arquiteturais". Defina claramente qual é a prioridade.
* **Escopo excessivamente amplo:** Pedir para "refatorar todo o serviço de checkout para microsserviços". Divida tarefas grandes em passos pequenos e revisáveis.
* **Falta de exemplos e casos de borda:** Regras descritivas ajudam, mas exemplos concretos de entrada e saída esperadas comunicam a intenção com muito mais precisão.
* **Tratar a primeira resposta gerada como verificada:** Uma explicação convincente gerada pelo modelo não substitui testes executados, linters e análise estática.
* **Complexidade arquitetural prematura:** Pedir "Clean Architecture, CQRS e Event Sourcing" para um CRUD simples introduz custo de manutenção desnecessário. A menos que esses padrões já façam parte da base de código, prefira a solução mais simples que atenda aos requisitos. Veja mais no nosso artigo sobre [Spec-Driven Development](/posts/spec-driven-development/#cheap-scaffolding-can-create-expensive-maintenance).

---

## Qual idioma devo usar? {#which-language-should-i-use}

Use o idioma no qual você expressa os requisitos de negócio e nuances técnicas com maior facilidade e clareza. Você não precisa traduzir seus pensamentos para o inglês antes de formular um prompt.

Se você está trabalhando em times brasileiros ou com produtos locais, escreva seus prompts em **português brasileiro (pt-BR)**. É perfeitamente natural escrever a prosa de orientação em português e manter nomes de variáveis, queries SQL, campos de API JSON, logs de erro e contratos técnicos exatamente em inglês, como fazemos no dia a dia.

### Benchmarks e impacto em tokens

A diferença de capacidade dos modelos de ponta entre idiomas diminuiu expressivamente. No benchmark [zero-shot MMLU da OpenAI](https://cdn.openai.com/gpt-4-5-system-card-2272025.pdf), o modelo o1 alcançou **92,3% em inglês** e **89,5% em português brasileiro**. Essa diferença de 2,8 pontos percentuais em questões de conhecimento geral não indica inferioridade para tarefas práticas de engenharia de software.

O fator que varia na prática é o consumo de tokens. Como a maioria dos tokenizers é treinada predominantemente com dados em inglês, frases em português costumam ser fragmentadas em mais tokens:

* **Inglês:** *"Please explain how the number of input tokens affects the context window and API cost."* (16 tokens com OpenAI `o200k_base`)
* **Português brasileiro:** *"Explique como a quantidade de tokens de entrada afeta a janela de contexto e o custo da API."* (21 tokens com OpenAI `o200k_base`)

Neste exemplo, o prompt em português utilizou cerca de 31% mais tokens. Embora isso represente uma leve diferença no custo de entrada e na janela de contexto, a clareza da regra de negócio sempre compensa esse impacto. Para prompts críticos em escala, compare ambas as abordagens com métricas objetivas. Confira a análise detalhada em [Context Engineering](/posts/context-engineering/#language-coverage-training-data-and-token-budgets).

---

## Revise um prompt com base em uma falha observada {#revise-a-prompt-around-an-observed-failure}

Vejamos como aplicar esse ciclo no nosso exemplo de checkout de e-commerce.

Imagine que o seu prompt inicial tenha sido apenas: *"Adicione suporte a código de desconto no checkout."*

O modelo devolveu uma implementação que calcula os descontos via JavaScript no navegador do cliente e grava o valor cheio original no banco de dados. Em vez de adicionar apelos genéricos ("Por favor, faça isso de forma segura!"), identifique a responsabilidade arquitetural ausente e reformule a instrução:

```text
Tarefa: Adicione suporte opcional a código de desconto no fluxo de checkout.

Contexto:
- Localize o contrato de pricing atual em services/pricing/contracts.
- Mapeie o fluxo de cotação entre o web storefront, order-service e pricing-service.

Comportamento esperado:
- O Pricing Service é o único responsável pela validação e cálculo; o web storefront apenas exibe a cotação retornada.
- O Order Service persiste o ID da cotação aprovada e os totais recebidos diretamente do Pricing Service.
- Se nenhum cupom for informado, mantenha o comportamento atual do checkout intacto.
- Se o cupom for inválido ou estiver expirado, exiba a mensagem de erro retornada pelo Pricing Service e bloqueie a criação do pedido com desconto.

Verificação:
- Derive testes de borda a partir destas regras e do contrato de pricing.
- Valide o fluxo ponta a ponta: exibição do valor na UI e persistência no banco.
- Relate todos os testes executados, cenários não cobertos e dúvidas em aberto.
```

Ao especificar a divisão de responsabilidades entre os serviços, você elimina a causa raiz do problema arquitetural.

---

## Reutilize um exemplo funcional e um registro de decisões {#reuse-a-working-example-and-a-decision-record}

Como demonstra Rahul Garg em [Patterns for Reducing Friction in AI-Assisted Development](https://martinfowler.com/articles/reduce-friction-ai/), ambientar o agente com exemplos reais da própria base de código acelera significativamente o desenvolvimento.

Antes de solicitar a implementação de um novo código, faça uma etapa de orientação:

```text
1. Localize no repositório uma feature recente de checkout que siga nossos padrões atuais.
2. Identifique o handler da rota, o client de pricing e as fixtures de teste relevantes por seus caminhos de arquivo.
3. Explique quais convenções se aplicam ao código de desconto e onde serão necessárias adaptações.
4. Sinalize eventuais divergências com o contrato de pricing antes de iniciar a codificação.
5. Registre as decisões confirmadas e questões em aberto em docs/decisions/checkout-discounts.md.
```

Essa abordagem garante que convenções de nomenclatura, tratamento de erros e estruturas de testes sejam mantidas de forma consistente.

---

## Aprimore prompts com evidências {#improve-prompts-with-evidence}

Prompts para desenvolvimento de software devem ser versionados e avaliados com critérios objetivos, seguindo a metodologia descrita por Chip Huyen em *AI Engineering* ([Capítulo 5, "Prompt Engineering"](https://www.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html) e [Capítulo 3, "Evaluation Methodology"](https://www.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html)):

1. **Defina casos de teste:** Crie cenários para códigos válidos, expirados, ausência de cupom e divergências de cálculo.
2. **Crie conjuntos de benchmark:** Use um grupo de cenários para evoluir o Prompt A para o Prompt B, reservando um conjunto separado para validação cega.
3. **Execute testes comparativos:** Rode o Prompt A e o Prompt B em cópias limpas do repositório, com o mesmo modelo, ferramentas, permissões e limite de tempo.
4. **Meça resultados completos:** Acompanhe a taxa de aprovação, regressões, número de tentativas de correção, tempo de code review, latência e custo de tokens.

Registre os resultados em uma tabela comparativa. Os valores abaixo são ilustrativos, não resultados medidos:

| Tarefa / Commit Inicial | Versão do Prompt & Modelo | Testes de Aceite Aprovados | Regressões | Tentativas de Correção | Tempo de Review | Latência | Custo Total |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Desconto checkout #482 | Prompt v1 / Claude 3.5 | 4 / 5 | 1 | 2 | 12 min | 45s | \$0,042 |
| Desconto checkout #482 | Prompt v2 / Claude 3.5 | 5 / 5 | 0 | 0 | 4 min | 28s | \$0,028 |

Para avaliações automatizadas em escala, você pode usar ferramentas de scoring estruturado como a [primitiva Score do TypeSafe Jev](https://docs.typesafe.ai/primitives/score) para avaliar a cobertura de requisitos e a qualidade dos diffs, aplicando o [padrão de composite scoring](https://docs.typesafe.ai/patterns/composite-scoring).

---

## Conclusão e próximos passos

Dominar a elaboração de prompts é a base para obter o máximo rendimento de agentes de programação:

* Estruture cada prompt com **objetivo claro, contexto técnico, restrições e critérios de aceite testáveis**.
* Forneça exemplos práticos de entrada e saída esperada em vez de adjetivos abstratos.
* Use o idioma em que você se expressa melhor, mantendo identificadores técnicos em inglês.
* Teste e aprimore seus prompts com base em métricas e evidências reais.

Instruções bem escritas direcionam o modelo sobre *o que* fazer. No próximo artigo da série, [AI Gateways e roteamento de modelos](/posts/ai-gateway-routing/), veremos como a infraestrutura direciona as requisições para o modelo mais adequado, gerenciando custos, latência e guardrails de segurança.
