# Social Event Platform - Database Objects Assignment

## 📋 Tabela de Atribuição de Objetos de Base de Dados

### Tabelas PostgreSQL

| Objeto | Tipo | Descrição | Relacionado com Requisitos | Responsável |
|--------|------|-----------|---------------------------|-------------|
| **users** | Tabela | Gestão de utilizadores e perfis | RF-1.1, RF-1.2 | António |
| **user_preferences** | Tabela | Preferências de notificações, privacidade e display | RF-1.2, RF-9.4 | Joel |
| **friendships** | Tabela | Relações de amizade entre utilizadores | RF-2.1 | António |
| **events** | Tabela | Eventos principais com detalhes e configurações | RF-3.1, RF-3.3, RF-4.1 | Luis |
| **event_invitations** | Tabela | Convites e participação em eventos | RF-3.2 | Joel |
| **event_cohosts** | Tabela | Co-anfitriões com permissões específicas | RF-3.2 | António |
| **event_series** | Tabela | Gestão de eventos recorrentes | RF-3.1 | Simão |
| **checkins** | Tabela | Check-ins e check-outs em eventos | RF-4.2 | Luis |
| **expenses** | Tabela | Despesas associadas a eventos | RF-7.1 | Simão |
| **expense_shares** | Tabela | Divisão de despesas entre participantes | RF-7.2 | António |
| **expense_receipts** | Tabela | Recibos digitalizados com OCR | RF-7.1 | Joel |
| **payments** | Tabela | Registo de pagamentos entre utilizadores | RF-7.3 | Simão |
| **polls** | Tabela | Votações em eventos | RF-8.1 | Joel |
| **poll_options** | Tabela | Opções das votações | RF-8.1 | Simão |
| **poll_votes** | Tabela | Votos dos utilizadores | RF-8.2 | António |
| **tags** | Tabela | Tags reutilizáveis para categorização | RF-6.4 | Luis |
| **media_tags** | Tabela | Tags aplicadas a media | RF-6.4 | António |
| **user_tags** | Tabela | Tags de utilizadores em media (fotos) | RF-6.4 | Simão |
| **event_activities** | Tabela | Feed de atividades por evento | RF-10.1 | Joel |
| **event_analytics** | Tabela | Métricas e analytics de eventos | RF-11.1 | Luis |

---

### Views

| View | Descrição | Relacionado com Requisitos | Responsável |
|------|-----------|---------------------------|-------------|
| **v_active_events** | Eventos ativos com informação do host e contagem de participantes | RF-3.3, RF-10.2 | Simão |
| **v_user_expense_summary** | Resumo de despesas por utilizador (deve/pago) | RF-7.4 | António |
| **v_event_attendance** | Estatísticas de participação em eventos (confirmados, maybe, declined, check-ins) | RF-11.1 | Joel |
| **v_poll_results** | Resultados das votações com percentagens e médias | RF-8.3 | Simão |
| **v_user_friends** | Rede social de amizades simplificada | RF-2.1 | Luis |

---

### Funções e Triggers

| Função/Trigger | Tipo | Descrição | Relacionado com Requisitos | Responsável |
|----------------|------|-----------|---------------------------|-------------|
| **update_updated_at_column()** | Function + Triggers | Atualização automática de timestamps em múltiplas tabelas | Geral | António |
| **validate_expense_shares()** | Function + Trigger | Validação de que divisão de despesas não excede o valor total | RF-7.2 | Joel |
| **update_expense_settled_status()** | Function + Trigger | Atualização automática do status de despesas pagas | RF-7.3 | António |
| **log_event_activity()** | Function + Triggers | Registo automático de atividades (convites, despesas, polls, check-ins) | RF-10.1 | Luis |
| **normalize_friendship_users()** | Function + Trigger | Normalização de IDs em friendships (user_id_1 < user_id_2) | RF-2.1 | Simão |
| **get_user_upcoming_events()** | Function | Obter eventos futuros do utilizador com papel (host/co-host/attendee) | RF-3.3, RF-10.2 | António |
| **calculate_event_balance()** | Function | Calcular balanço financeiro de utilizador em evento específico | RF-7.4 | Joel |
| **get_mutual_friends()** | Function | Obter amigos em comum entre dois utilizadores | RF-2.1 | Simão |

---

### Tipos Personalizados (ENUMs)

| Tipo ENUM | Valores | Utilizado em | Responsável |
|-----------|---------|--------------|-------------|
| **friendship_status** | pending, accepted, blocked | friendships | Luis |
| **event_status** | draft, published, cancelled, completed | events | António |
| **invitation_status** | pending, accepted, declined, maybe | event_invitations | Joel |
| **invitation_role** | attendee, co-host, moderator | event_invitations | Simão |
| **payment_status** | pending, completed, failed, refunded | payments | Joel |
| **poll_type** | single_choice, multiple_choice, ranking | polls | Simão |
| **tag_type** | user, event, media, general | tags | Luis |

---

### MongoDB Collections (Referência)

| Collection | Descrição | Relacionado com Requisitos | Responsável |
|------------|-----------|---------------------------|-------------|
| **media** | Armazenamento de fotos e vídeos com metadata | RF-6.1, RF-6.2 | Joel |
| **messages** | Mensagens de chat em tempo real | RF-5.1 | António |
| **notifications** | Centro de notificações com histórico | RF-9.1, RF-9.3 | Simão |

---
