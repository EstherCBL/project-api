# Orientações – Avaliação Prática: API de Reserva de Salas

Disciplina: Desenvolvimento de API Backend (UniEVANGÉLICA)
Stack escolhida: **Python + FastAPI**
Repositório: https://github.com/EstherCBL/api-rest

---

## 1. Objetivo

Construir uma API REST para gerenciamento e reserva de salas e laboratórios. Usuários reservam espaços em dias e horários. O projeto cobre cadastro, autenticação, gerenciamento de salas, criação e cancelamento de reservas, validação de dados e regras de negócio.

Regra de negócio central (foco da arguição): **não pode haver duas reservas da mesma sala no mesmo horário.**

## 2. Stack (Python)

| Camada | Tecnologia |
|---|---|
| Framework | FastAPI |
| Banco e ORM | SQLite ou PostgreSQL com SQLAlchemy |
| Migrations | Alembic |
| Validação | Pydantic (nativo do FastAPI) |
| Senha | bcrypt (ou passlib) |
| Autenticação | JWT com PyJWT e OAuth2PasswordBearer |
| Testes | pytest com TestClient |

O contrato da API (rotas, regras, códigos HTTP) é igual para todas as stacks.

## 3. Recursos

- **users**: nome, e-mail, senha (só o hash é gravado) e papel `user` ou `admin`. Cadastro e login com JWT.
- **rooms**: nome, capacidade e localização. CRUD completo; só admin cria, edita e remove.
- **reservations**: sala, usuário, início, fim e motivo.

## 4. Rotas

```
POST   /api/register
POST   /api/login                          (devolve o token JWT)
GET    /api/rooms                          (lista paginada: ?page=1&size=10)
POST   /api/rooms                          (admin)
PUT    /api/rooms/{id}                     (admin)
DELETE /api/rooms/{id}                     (admin)
GET    /api/rooms/{id}/reservations?date=2026-11-20
POST   /api/reservations
GET    /api/reservations/me
DELETE /api/reservations/{id}              (só o dono ou o admin)
```

- Todas as rotas, **exceto** `register`, `login` e `GET /api/rooms`, exigem o header `Authorization: Bearer <token>`.
- **Não há rota de logout.** O JWT é sem estado: o cliente descarta o token e ele vale até expirar. Usar expiração curta (ex.: 1 hora). Isso é pergunta provável na arguição.

## 5. Regras de negócio

1. `fim` deve ser depois de `início`, e a reserva não pode ser no passado → erro **422**.
2. Reserva que conflita com outra da mesma sala → **409**. Condição de conflito:
   `novo_inicio < fim_existente AND novo_fim > inicio_existente`
3. Só o dono ou o admin cancela uma reserva; os demais recebem **403**. A checagem fica numa função/dependência de autorização, não espalhada pelas rotas.

## 6. Formato de erro (padronizado)

Todo erro responde JSON no mesmo formato:

```json
{ "status": 409, "message": "A sala já está reservada nesse horário." }
```

Erros de validação incluem a lista de campos:

```json
{ "status": 422, "message": "Erro de validação.", "errors": [{ "field": "end", "message": "..." }] }
```

No FastAPI isso exige tratar `RequestValidationError`, porque o formato padrão é outro.

Códigos HTTP usados: **201, 204, 401, 403, 404, 409, 422**.

## 7. Conhecimentos cobrados (FastAPI)

| Conceito | Como fica no FastAPI |
|---|---|
| Migrations e chaves estrangeiras | models SQLAlchemy e Alembic |
| Relacionamentos e consulta | `relationship` e `ForeignKey`; consulta de conflito com `select().where()` |
| Validação | modelos Pydantic no corpo da requisição |
| Saída padronizada (sem vazar o hash) | `response_model` com Pydantic |
| Autenticação | dependência com `Depends(get_current_user)` |
| Autorização | dependência `require_admin` e checagem de dono |
| Testes | 4 a 6 testes com TestClient e banco de teste (SQLite em memória serve) |

## 8. Cronograma

### Cronograma de desenvolvimento

O projeto é desenvolvido progressivamente, com entregas e atividades distribuídas entre as semanas 15 e 19.

**Semana 15 – Planejamento e estruturação**

- Estruturação dos grupos: grupos de 5 pessoas.
- Compreensão dos requisitos do projeto.
- Escolha da tecnologia e do framework.
- Configuração do ambiente de desenvolvimento.
- Criação da estrutura inicial da API.
- Configuração do banco de dados.

**Semana 16 – Banco de dados e gerenciamento de salas**

- Criação dos modelos e relacionamentos.
- Configuração das migrations.
- Implementação do CRUD de salas.
- Validação dos dados e tratamento de respostas.
- Configuração do usuário administrador inicial.

**Semana 17 – Usuários e autenticação**

- Implementação do cadastro de usuários.
- Implementação do login.
- Geração e validação de tokens JWT.
- Criptografia/hash de senhas.
- Implementação dos mecanismos de autenticação e autorização.

**Semana 18 – Reservas e regras de negócio**

- Implementação do cadastro de reservas.
- Consulta das reservas realizadas pelo usuário.
- Cancelamento de reservas.
- Validação de datas e horários.
- Implementação da regra que impede duas reservas conflitantes para a mesma sala.
- Controle de permissões para cancelamento.

**Semana 19 – Finalização e apresentação**

- Revisão geral da implementação.
- Execução dos testes da API.
- Organização do repositório Git.
- Elaboração do README com instruções de instalação e execução.
- Preparação de exemplos de requisições utilizando Postman ou Insomnia.

### Avaliação e apresentação

Ao final de cada Sprint, cada grupo deve demonstrar a API em funcionamento, executar operações e explicar as principais decisões técnicas adotadas durante o desenvolvimento.

Durante a apresentação, podem ser solicitadas alterações, demonstrações de funcionalidades e explicações sobre trechos específicos do código.

### Entregas (Sprints)

| Sprint | Referente à semana | Prazo | Pontos |
|---|---|---|---|
| 1 | 15 | Semana 16, até 08h00 | 0,0 |
| 2 | 16 | Semana 17, até 08h00 | 10,0 |
| 3 | 17 | Semana 18, até 08h00 | 10,0 |
| 4 | 18 | Semana 19, até 08h00 | 10,0 |
| 5 | 19 | Semana 20, até 08h00 | 10,0 |

Cada semana conta como nota: não deixar tudo para a última.

## 9. Relatório individual (obrigatório em toda Sprint)

Cada integrante envia o seu, individualmente, no AVA (um relatório por aluno, não um por grupo). Responder sempre às 3 perguntas, mesmo sem impedimentos ou atividades incompletas:

1. **O que você fez?** Atividades da semana e suas contribuições.
2. **O que você vai fazer?** O que pretende desenvolver na próxima semana.
3. **Quais foram os impedimentos?** Dificuldades técnicas, problemas, dependências.

Regras:
- Não enviar no prazo = **zero** na entrega.
- Faltar à entrega presencial (quando houver) = zero naquela entrega.
- O relatório deve ser verdadeiro e compatível com o andamento do projeto.
- A pontuação é individual: considera relatório, participação e domínio técnico demonstrado.

## 10. Grupos

- Grupos de 5 pessoas; um membro envia pelo grupo quando for entrega do grupo.
- Divisão inicial sugerida: 3 no desenvolvimento e 2 nos testes, com rodízio ao longo das semanas.
- Todos precisam participar do desenvolvimento e dos testes e saber explicar tudo.

## 11. Avaliação final

| Critério | Peso |
|---|---|
| Funcionalidade e regras de negócio | 40% |
| Arguição e domínio da solução | 30% |
| Testes (implementação e execução) | 15% |
| Organização (Git, README) | 15% |

- Apresentação: até 10 minutos, com a API rodando ao vivo.
- O professor pode pedir alterações, demonstrações e explicações de trechos do código na hora.
- Em qualquer Sprint, podem ser feitas perguntas individuais: explicar funcionalidades, mostrar trechos, justificar decisões, explicar regras e validações, e apontar problemas encontrados.

## 12. Perguntas típicas da arguição (prepare as respostas)

1. Mostre onde está a regra de conflito. Por que essa condição detecta sobreposição?
2. Qual a diferença entre 401 e 403 na sua API? Prove com uma chamada.
3. Onde está a validação? O que acontece se eu enviar `fim` antes de `início`?
4. Como você impede que o hash da senha saia na resposta? Mostre no código (`response_model`).
5. Mude a capacidade de uma sala: que rota, que verbo e por quê? (`PUT /api/rooms/{id}`)
6. O que vai dentro do seu token? Por que não existe logout?
7. Rode os testes. Explique um deles.

## 13. Orientações importantes

- O projeto é desenvolvido por todos do grupo; é preciso entender e saber explicar todas as partes.
- Não basta a API funcionar: serão avaliados o domínio dos conceitos e das decisões técnicas.
- Repositório Git organizado e API executável no momento da apresentação.
- Prova substitutiva: mesmo nível de exigência, tempo menor e provavelmente individual.

## 14. Checklist final

- [ ] Rotas todas implementadas conforme a seção 4
- [ ] Senha salva só com hash (bcrypt) e nunca devolvida nas respostas
- [ ] JWT com expiração curta; 401 sem token/token inválido; 403 sem permissão
- [ ] Regra de conflito (409) e validação de datas (422)
- [ ] Autorização de cancelamento centralizada (dono ou admin)
- [ ] Erros no formato padrão, inclusive o 422 com `errors`
- [ ] Seed com admin e salas de exemplo
- [ ] 4 a 6 testes passando
- [ ] README com instalação, execução e exemplos de chamadas (ou coleção Postman/Insomnia)
- [ ] Commits de todos os integrantes no Git
- [ ] Relatório individual enviado em cada Sprint, antes das 08h00
