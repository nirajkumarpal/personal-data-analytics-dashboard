# Personal Data Analysis UML

## Class Diagram (Mermaid)
```mermaid
classDiagram
    class User {
        +int id
        +string username
        +string email
        +string password_hash
        +float study_goal
        +to_dict()
    }

    class DailyLog {
        +int id
        +int user_id
        +date date
        +float study_hours
        +float screen_time_hours
        +int mood_score
        +to_dict()
    }

    class Task {
        +int id
        +int log_id
        +string task_name
        +bool is_completed
        +to_dict()
    }

    class AuthRoutes {
        +register()
        +login()
    }

    class LogRoutes {
        +add_log()
        +fetch_logs()
        +update_log()
        +delete_log()
        +update_task_status()
    }

    class AnalyticsRoutes {
        +get_summary()
        +weekly_summary()
        +get_insights()
    }

    class GoalRoutes {
        +set_goal()
        +get_goal()
    }

    class InsightsService {
        +calculate_productivity_score()
        +generate_smart_insights()
        +generate_weekly_summary()
    }

    User "1" --> "0..*" DailyLog : has
    DailyLog "1" --> "0..*" Task : has

    AuthRoutes ..> User : uses
    LogRoutes ..> DailyLog : manages
    LogRoutes ..> Task : manages
    AnalyticsRoutes ..> DailyLog : reads
    AnalyticsRoutes ..> InsightsService : uses
    GoalRoutes ..> User : updates goal
    GoalRoutes ..> DailyLog : reads today data
```

## Use Case Diagram (PlantUML)
```plantuml
@startuml
left to right direction
actor User

rectangle "Personal Analytics System" {
  usecase "Register Account" as UC_Register
  usecase "Login" as UC_Login
  usecase "Set Daily Goal" as UC_SetGoal
  usecase "View Daily Goal Progress" as UC_ViewGoal
  usecase "Add Daily Log" as UC_AddLog
  usecase "Add Tasks with Daily Log" as UC_AddTasks
  usecase "View Log History" as UC_ViewLogs
  usecase "Update Daily Log" as UC_UpdateLog
  usecase "Delete Daily Log" as UC_DeleteLog
  usecase "Mark Task Complete/Pending" as UC_TaskStatus
  usecase "View Dashboard Summary" as UC_Summary
  usecase "View Weekly Summary" as UC_Weekly
  usecase "View Insights" as UC_Insights
}

User --> UC_Register
User --> UC_Login
User --> UC_SetGoal
User --> UC_ViewGoal
User --> UC_AddLog
User --> UC_ViewLogs
User --> UC_UpdateLog
User --> UC_DeleteLog
User --> UC_TaskStatus
User --> UC_Summary
User --> UC_Weekly
User --> UC_Insights

UC_AddLog .> UC_AddTasks : <<include>>
UC_Summary .> UC_Weekly : <<include>>
UC_Summary .> UC_Insights : <<include>>
@enduml
```

## ER Diagram (Mermaid)
```mermaid
erDiagram
    USERS {
        INT id PK
        VARCHAR username
        VARCHAR email UK
        VARCHAR password_hash
        FLOAT study_goal
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    DAILY_LOGS {
        INT id PK
        INT user_id FK
        DATE date
        FLOAT study_hours
        FLOAT screen_time_hours
        INT mood_score
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    TASKS {
        INT id PK
        INT log_id FK
        VARCHAR task_name
        BOOLEAN is_completed
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    USERS ||--o{ DAILY_LOGS : "has"
    DAILY_LOGS ||--o{ TASKS : "contains"
```
## Endpoint Mapping (Quick Reference)
- Register: `POST /api/auth/register`
- Login: `POST /api/auth/login`
- Add log: `POST /api/logs/add`
- Fetch logs: `GET /api/logs/fetch?user_id=...`
- Update log: `PUT /api/logs/update/<log_id>`
- Delete log: `DELETE /api/logs/delete/<log_id>?user_id=...`
- Update task status: `PUT /api/logs/<log_id>/tasks/<task_id>/status`
- Dashboard summary: `GET /api/analytics/summary?user_id=...`
- Weekly summary: `GET /api/analytics/weekly-summary?user_id=...`
- Insights: `GET /api/analytics/insights?user_id=...`
- Set goal: `POST /api/goals/set`
- Get goal: `GET /api/goals/get?user_id=...`

