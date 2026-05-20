# Diplom
Программа для Дипломной работы

## Описание проекта

Система анализа энергоэффективности многоквартирных домов (МКД) с использованием ML-методов и соблюдением нормативных требований РФ (ПП №354, №124, СП 50.13330).

## 🏗️ Архитектура

4-уровневая архитектура:
1. **Источники данных** - АСКУТЭ, Росгидромет, справочники
2. **Брокер и валидация** - RabbitMQ/Kafka, первичная валидация
3. **Хранение и ETL** - PostgreSQL+TimescaleDB, MinIO, Prefect пайплайны
4. **Аналитика и API** - FastAPI, ML модели (регрессия, ARIMA, Prophet, anomaly detection)

Подробности в [ARCHITECTURE.md](./ARCHITECTURE.md)

## 🚀 Быстрый старт

```bash
# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps

# Логи backend
docker-compose logs -f backend
```

### Доступ к сервисам

| Сервис | URL |
|--------|-----|
| API Docs | http://localhost:8000/docs |
| Frontend | http://localhost:5173 |
| Grafana | http://localhost:3001 (admin/admin) |
| Prometheus | http://localhost:9090 |

См. [DEPLOYMENT.md](./docs/DEPLOYMENT.md) для подробностей.

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
