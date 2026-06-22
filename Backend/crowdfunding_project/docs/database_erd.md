# Database ERD

Tai lieu nay duoc tong hop tu cac Django models trong project.

## ERD tong quan

```mermaid
erDiagram
    USERS ||--o| ACCOUNTS_WALLET : owns
    USERS ||--o| RISK_PROFILES : has
    USERS ||--o| PROJECT_OWNER_APPLICATIONS : submits
    USERS ||--o{ PROJECT_OWNER_APPLICATIONS : reviews
    USERS ||--o{ BANK_ACCOUNTS : has
    USERS ||--o{ PROJECTS : owns
    USERS ||--o{ TRANSACTIONS : makes
    USERS ||--o{ USER_INTERACTIONS : performs
    USERS ||--o{ AI_RECOMMENDATIONS : receives
    USERS ||--o{ AUDIT_LOGS : creates

    PROJECTS ||--o{ TRANSACTIONS : receives
    PROJECTS ||--o{ USER_INTERACTIONS : tracked_by

    BANK_ACCOUNTS ||--o{ TRANSACTIONS : used_for
```

## Schema chi tiet

```mermaid
erDiagram
    USERS {
        bigint id PK
        varchar email UK
        text password
        varchar full_name
        varchar phone UK
        varchar role
        varchar bank_name
        varchar bank_account
        varchar bank_branch
        boolean is_active
        boolean is_verified
        datetime created_at
        datetime updated_at
    }

    ACCOUNTS_WALLET {
        bigint id PK
        bigint user_id FK "OneToOne users.id"
        decimal balance
        varchar currency
        datetime updated_at
    }

    BANK_ACCOUNTS {
        bigint id PK
        bigint user_id FK
        varchar bank_name
        varchar account_number
        varchar account_holder
        boolean is_default
        datetime created_at
    }

    PROJECT_OWNER_APPLICATIONS {
        bigint id PK
        bigint user_id FK "OneToOne users.id"
        varchar business_name
        varchar business_type
        varchar tax_code
        varchar id_number
        text bio
        text experience
        varchar document_url
        varchar status
        text reject_reason
        bigint reviewed_by_id FK
        datetime reviewed_at
        datetime created_at
        datetime updated_at
    }

    RISK_PROFILES {
        bigint id PK
        bigint user_id FK "OneToOne users.id"
        int age
        bigint income
        int investment_experience
        int risk_tolerance
        decimal base_score
        varchar risk_tier
        datetime updated_at
    }

    PROJECTS {
        bigint id PK
        bigint owner_id FK
        varchar name
        varchar category
        text description
        varchar location
        decimal funding_target
        decimal raised
        decimal apr_expected
        datetime start_at
        datetime end_at
        varchar status
        smallint risk_level
        smallint expected_return_score
        smallint liquidity_score
        decimal min_invest_amount
        decimal max_invest_amount
        int min_invest_duration_months
        datetime created_at
        datetime updated_at
    }

    TRANSACTIONS {
        bigint id PK
        bigint user_id FK
        bigint project_id FK
        bigint bank_account_id FK
        decimal amount
        varchar currency
        varchar type
        varchar payment_method
        varchar status
        varchar description
        varchar stripe_payment_intent_id
        varchar stripe_charge_id
        varchar external_reference
        datetime created_at
        datetime updated_at
    }

    USER_INTERACTIONS {
        bigint id PK
        bigint user_id FK
        bigint project_id FK
        varchar interaction_type
        float value
        varchar source
        varchar session_id
        datetime created_at
    }

    AI_RECOMMENDATIONS {
        bigint id PK
        bigint user_id FK
        json projects_json
        varchar generated_by
        datetime created_at
    }

    AUDIT_LOGS {
        bigint id PK
        bigint user_id FK
        varchar action
        varchar entity_type
        bigint entity_id
        json metadata
        datetime created_at
    }

    USERS ||--o| ACCOUNTS_WALLET : "user_id"
    USERS ||--o| RISK_PROFILES : "user_id"
    USERS ||--o| PROJECT_OWNER_APPLICATIONS : "user_id"
    USERS ||--o{ PROJECT_OWNER_APPLICATIONS : "reviewed_by_id"
    USERS ||--o{ BANK_ACCOUNTS : "user_id"
    USERS ||--o{ PROJECTS : "owner_id"
    USERS ||--o{ TRANSACTIONS : "user_id"
    USERS ||--o{ USER_INTERACTIONS : "user_id"
    USERS ||--o{ AI_RECOMMENDATIONS : "user_id"
    USERS ||--o{ AUDIT_LOGS : "user_id"

    PROJECTS ||--o{ TRANSACTIONS : "project_id"
    PROJECTS ||--o{ USER_INTERACTIONS : "project_id"
    BANK_ACCOUNTS ||--o{ TRANSACTIONS : "bank_account_id"
```

## Ghi chu quan he

- `users` la bang trung tam cua he thong.
- `accounts_wallet`, `risk_profiles`, `project_owner_applications` la quan he 1-1 voi `users`.
- `projects.owner_id` tro toi `users.id`, the hien chu du an.
- `transactions.user_id` la nguoi thuc hien giao dich.
- `transactions.project_id` co the null vi nap/rut tien khong nhat thiet gan voi du an.
- `transactions.bank_account_id` co the null vi khong phai moi giao dich deu dung tai khoan ngan hang.
- `project_owner_applications.reviewed_by_id` tro toi admin/user duyet ho so va co the null.
- `audit_logs.entity_type` va `entity_id` la tham chieu logic, khong phai foreign key that.
- Django se tu tao them cac bang phu cho quyen/nhom cua `PermissionsMixin`, vi vay ERD tren tap trung vao domain models cua project.
