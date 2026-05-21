# Система мониторинга и анализа энергопотребления МКД

## 📋 Описание
Система предназначена для сбора, хранения, анализа и визуализации данных о потреблении тепловой энергии в многоквартирных домах (МКД) с учётом погодных условий и нормативных требований РФ.

## 🏗️ Архитектура
Проект реализует 4-уровневую архитектуру:
1. **Источники данных** - АСКУТЭ, погодные API, справочники
2. **Брокер сообщений** - RabbitMQ для буферизации потоков данных
3. **Хранение и ETL** - PostgreSQL + Prefect для обработки и нормализации
4. **Аналитика и API** - FastAPI backend + ML модели + React frontend

### Технологический стек
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy (async), Celery
- **Frontend**: React 18 + TypeScript, Vite, Ant Design
- **БД**: PostgreSQL 15 (с нативным партиционированием)
- **Очереди**: Redis, RabbitMQ
- **ML**: pandas, scikit-learn, statsmodels, prophet, pyod, MLflow
- **Инфраструктура**: Docker, Docker Compose, Prometheus, Grafana

## 🚀 Быстрый старт

### Требования
- Docker 20.10+
- Docker Compose 2.0+
- Git

### Установка и запуск

```bash
# Клонирование репозитория
git clone <repository-url>
cd workspace

# Запуск всех сервисов
docker compose up -d --build

# Просмотр логов
docker compose logs -f

# Остановка
docker compose down
```

### Доступ к сервисам после запуска

| Сервис | URL | Логин/Пароль |
|--------|-----|--------------|
| API Docs | http://localhost:8000/docs | - |
| Frontend | http://localhost:3000 | - |
| Grafana | http://localhost:3001 | admin/admin |
| Prometheus | http://localhost:9090 | - |
| MLflow | http://localhost:5000 | - |
| MinIO Console | http://localhost:9001 | minioadmin/minioadmin |
| RabbitMQ Management | http://localhost:15672 | guest/guest |

## 📁 Структура проекта

```
/workspace
├── backend/                 # Backend на FastAPI
│   ├── api/                # API endpoints, schemas, models
│   ├── core/               # Config, security
│   ├── db/                 # DB models, session
│   ├── middleware/         # Auth, logging
│   ├── services/           # Business logic
│   │   ├── etl/           # ETL pipelines
│   │   ├── analytics/     # Analytics engine
│   │   ├── compliance/    # Regulatory compliance
│   │   └── integrations/  # External APIs
│   └── utils/              # Utilities
├── frontend/               # React + TypeScript SPA
├── ml_models/              # ML модели
│   ├── regression/        # Регрессионные модели
│   ├── time_series/       # Временные ряды (ARIMA, Prophet)
│   ├── anomaly_detection/ # Детекция аномалий
│   └── clustering/        # Кластеризация МКД
├── prefect_flows/          # Prefect ETL пайплайны
├── infrastructure/         # Docker, K8s, мониторинг
├── docs/                   # Документация
│   ├── ARCHITECTURE.md    # Архитектура системы
│   ├── DEPLOYMENT.md      # Руководство по развёртыванию
│   └── openapi.yaml       # OpenAPI спецификация
├── tests/                  # Тесты
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── configs/                # Конфигурационные файлы
```

## 🛠️ Технологический стек

| Категория | Технологии |
|-----------|------------|
| Backend | Python 3.11+, FastAPI, SQLAlchemy async, Celery |
| Frontend | React 18, TypeScript, Vite, Recharts, Leaflet |
| БД | PostgreSQL 15 + TimescaleDB, Redis, MinIO |
| Брокер | RabbitMQ / Apache Kafka |
| ETL | Prefect, pandas |
| ML | scikit-learn, statsmodels, Prophet, pyod, MLflow |
| Инфраструктура | Docker, Docker Compose, Kubernetes |
| Мониторинг | Prometheus, Grafana, Loki, Sentry |

## 📊 Ключевые возможности

- ✅ Сбор данных с приборов учёта (АСКУТЭ)
- ✅ Погодная нормализация (ГСОП по СП 50.13330)
- ✅ Детекция аномалий (LOF, Isolation Forest, EWMA, консенсус)
- ✅ Прогнозирование (SARIMA, Prophet, квантили)
- ✅ Кластеризация МКД по профилям потребления
- ✅ Генерация отчётов (PDF, Excel, ГИС ЖКХ)
- ✅ Соответствие ПП РФ №354, №124, ФСТЭК

## 🧪 Тестирование

```bash
# Unit тесты
pytest tests/unit -v

# Integration тесты
pytest tests/integration -v

# Нагрузочное тестирование
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

## 📄 Лицензия

Proprietary (учебный проект)

## 👥 Контакты

Автор: Diplom Project
