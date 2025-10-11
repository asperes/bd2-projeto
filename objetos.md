# Social Event Platform - Database Objects Assignment

## 📋 Tabela de Atribuição de Objetos de Base de Dados

### Tabelas PostgreSQL

| Objeto | Tipo | Descrição | Relacionado com Requisitos | Responsável |
|--------|------|-----------|---------------------------|-------------|
| **users** | Tabela | Gestão de utilizadores e perfis | RF-1.1, RF-1.2 | António |
| **user_preferences** | Tabela | Preferências de notificações, privacidade e display | RF-1.2, RF-9.4 | António |
| **friendships** | Tabela | Relações de amizade entre utilizadores | RF-2.1 | Luis |
| **events** | Tabela | Eventos principais com detalhes e configurações | RF-3.1, RF-3.3, RF-4.1 | Simão |
| **event_invitations** | Tabela | Convites e participação em eventos | RF-3.2 | Simão |
| **event_cohosts** | Tabela | Co-anfitriões com permissões específicas | RF-3.2 | Simão |
| **event_series** | Tabela | Gestão de eventos recorrentes | RF-3.1 | Simão |
| **checkins** | Tabela | Check-ins e check-outs em eventos | RF-4.2 | Simão |
| **expenses** | Tabela | Despesas associadas a eventos | RF-7.1 | Luis |
| **expense_shares** | Tabela | Divisão de despesas entre participantes | RF-7.2 | Luis |
| **expense_receipts** | Tabela | Recibos digitalizados com OCR | RF-7.1 | Luis |
| **payments** | Tabela | Registo de pagamentos entre utilizadores | RF-7.3 | Luis |
| **polls** | Tabela | Votações em eventos | RF-8.1 | Luis |
| **poll_options** | Tabela | Opções das votações | RF-8.1 | Luis |
| **poll_votes** | Tabela | Votos dos utilizadores | RF-8.2 | Luis |
| **tags** | Tabela | Tags reutilizáveis para categorização | RF-6.4 | Joel |
| **media_tags** | Tabela | Tags aplicadas a media | RF-6.4 | Joel |
| **user_tags** | Tabela | Tags de utilizadores em media (fotos) | RF-6.4 | Joel |
| **event_activities** | Tabela | Feed de atividades por evento | RF-10.1 | Simão |
| **event_analytics** | Tabela | Métricas e analytics de eventos | RF-11.1 | António |

---

### Views

| View | Descrição | Relacionado com Requisitos | Responsável |
|------|-----------|---------------------------|-------------|
| **v_active_events** | Eventos ativos com informação do host e contagem de participantes | RF-3.3, RF-10.2 | Simão |
| **v_user_expense_summary** | Resumo de despesas por utilizador (deve/pago) | RF-7.4 | Luis |
| **v_event_attendance** | Estatísticas de participação em eventos (confirmados, maybe, declined, check-ins) | RF-11.1 | Simão |
| **v_poll_results** | Resultados das votações com percentagens e médias | RF-8.3 | Luis |
| **v_user_friends** | Rede social de amizades simplificada | RF-2.1 | Luis |

---

### Funções e Triggers

| Função/Trigger | Tipo | Descrição | Relacionado com Requisitos | Responsável |
|----------------|------|-----------|---------------------------|-------------|
| **update_updated_at_column()** | Function + Triggers | Atualização automática de timestamps em múltiplas tabelas | Geral | António |
| **validate_expense_shares()** | Function + Trigger | Validação de que divisão de despesas não excede o valor total | RF-7.2 | Luis |
| **update_expense_settled_status()** | Function + Trigger | Atualização automática do status de despesas pagas | RF-7.3 | Luis |
| **log_event_activity()** | Function + Triggers | Registo automático de atividades (convites, despesas, polls, check-ins) | RF-10.1 | Simão |
| **normalize_friendship_users()** | Function + Trigger | Normalização de IDs em friendships (user_id_1 < user_id_2) | RF-2.1 | Luis |
| **get_user_upcoming_events()** | Function | Obter eventos futuros do utilizador com papel (host/co-host/attendee) | RF-3.3, RF-10.2 | Simão |
| **calculate_event_balance()** | Function | Calcular balanço financeiro de utilizador em evento específico | RF-7.4 | Luis |
| **get_mutual_friends()** | Function | Obter amigos em comum entre dois utilizadores | RF-2.1 | Luis |

---

### Tipos Personalizados (ENUMs)

| Tipo ENUM | Valores | Utilizado em | Responsável |
|-----------|---------|--------------|-------------|
| **friendship_status** | pending, accepted, blocked | friendships | Luis |
| **event_status** | draft, published, cancelled, completed | events | Simão |
| **invitation_status** | pending, accepted, declined, maybe | event_invitations | Simão |
| **invitation_role** | attendee, co-host, moderator | event_invitations | Simão |
| **payment_status** | pending, completed, failed, refunded | payments | Luis |
| **poll_type** | single_choice, multiple_choice, ranking | polls | Luis |
| **tag_type** | user, event, media, general | tags | Joel |

---

### Políticas de Row Level Security (RLS)

| Política | Tabela | Descrição | Relacionado com Requisitos | Responsável |
|----------|--------|-----------|---------------------------|-------------|
| **event_access_policy** | events | Controlo de acesso a eventos (público, host, convidado, co-host) | RF-12.2 | António |
| **invitation_access_policy** | event_invitations | Controlo de acesso a convites (invitee, inviter, host) | RF-12.2 | António |
|  **expense_access_policy** | expenses | Controlo de acesso a despesas | RF-12.2 | Luis |
|  **expense_shares_access_policy** | expense_shares | Controlo de acesso a divisões | RF-12.2 | Luis |
|  **poll_access_policy** | polls | Controlo de acesso a votações | RF-12.2 | Luis |

---

### Índices Especiais

| Índice | Tabela | Tipo | Descrição | Relacionado com Requisitos | Responsável |
|--------|--------|------|-----------|---------------------------|-------------|
| **idx_event_location** | events | GiST (PostGIS) | Pesquisa geoespacial de eventos por proximidade | RF-3.3, RF-4.1 | Simão |
| **idx_activity_event_time** | event_activities | B-tree (DESC) | Timeline de atividades otimizada para ordenação temporal | RF-10.1 | Simão |
| **unq_event_analytics_date** | event_analytics | Unique | Analytics diários únicos por evento | RF-11.1 | António |
| **unq_event_user_date** | checkins | Unique | Um check-in por utilizador por evento por dia | RF-4.2 | Simão |

---

### MongoDB Collections (Referência)

| Collection | Descrição | Relacionado com Requisitos | Responsável |
|------------|-----------|---------------------------|-------------|
| **media** | Armazenamento de fotos e vídeos com metadata | RF-6.1, RF-6.2 | Joel |
| **messages** | Mensagens de chat em tempo real | RF-5.1 | Luis |
| **notifications** | Centro de notificações com histórico | RF-9.1, RF-9.3 | Luis |

---
