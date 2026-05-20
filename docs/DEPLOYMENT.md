# Руководство по развёртыванию и запуску проекта

## Быстрый старт (Development)

### Предварительные требования

- Docker >= 24.0
- Docker Compose >= 2.20
- Python 3.11+ (для локальной разработки)
- Node.js 20+ (для frontend)

### Запуск всех сервисов

```bash
# Клонирование репозитория
cd /workspace

# Запуск в фоновом режиме
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f backend
```

### Доступ к сервисам

| Сервис | URL | Логин/Пароль |
|--------|-----|--------------|
| Backend API | http://localhost:8000 | - |
| API Docs (Swagger) | http://localhost:8000/docs | - |
| API Docs (ReDoc) | http://localhost:8000/redoc | - |
| Frontend | http://localhost:5173 | - |
| PostgreSQL | localhost:5432 | postgres/postgres |
| Redis | localhost:6379 | - |
| RabbitMQ Management | http://localhost:15672 | guest/guest |
| MinIO Console | http://localhost:9001 | minioadmin/minioadmin |
| MLflow | http://localhost:5000 | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3001 | admin/admin |

### Остановка сервисов

```bash
# Остановка с сохранением данных
docker-compose down

# Полная очистка (данные будут удалены!)
docker-compose down -v
```

## Локальная разработка (без Docker)

### Backend

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r backend/requirements.txt

# Запуск сервера разработки
uvicorn backend.main:create_app --reload --host 0.0.0.0 --port 8000

# Запуск Celery worker
celery -A backend.services.tasks.celery_app worker --loglevel=debug

# Запуск Celery beat (scheduler)
celery -A backend.services.tasks.celery_app beat --loglevel=info
```

### Frontend

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev-сервера
npm run dev

# Сборка для production
npm run build
```

## Production развёртывание

### Переменные окружения

Создайте файл `.env` с производственными настройками:

```bash
# Безопасность
JWT_SECRET_KEY=<сложный_ключ_минимум_32_символа>
ENVIRONMENT=production

# База данных
DB_HOST=postgres.internal
DB_PASSWORD=<сложный_пароль>

# MinIO
MINIO_ACCESS_KEY=<access_key>
MINIO_SECRET_KEY=<secret_key>

# Sentry (мониторинг ошибок)
SENTRY_DSN=https://<key>@sentry.io/<project_id>
```

### Production Docker Compose

```bash
# Использование production конфигурации
docker-compose -f docker-compose.prod.yml up -d

# Масштабирование workers
docker-compose up -d --scale celery-worker=5
```

### Kubernetes (опционально)

```bash
# Применение манифестов
kubectl apply -f infrastructure/k8s/

# Проверка статуса
kubectl get pods -n diplom
```

## Тестирование

### Unit тесты

```bash
pytest tests/unit -v --cov=backend
```

### Integration тесты

```bash
# Требуется запущенный docker-compose
pytest tests/integration -v --cov=backend
```

### Нагрузочное тестирование

```bash
# Запуск Locust
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

## Миграции базы данных

### Alembic (рекомендуется)

```bash
# Инициализация Alembic
alembic init alembic

# Создание новой миграции
alembic revision --autogenerate -m "Description"

# Применение миграций
alembic upgrade head

# Откат миграций
alembic downgrade -1
```

### Ручное применение SQL скриптов

```bash
psql -h localhost -U postgres -d diplom_db -f infrastructure/docker/init-db/*.sql
```

## Мониторинг и алерты

### Grafana Dashboards

Импортируйте дашборды из `infrastructure/docker/grafana/dashboards/`:

1. Откройте Grafana (http://localhost:3001)
2. Перейдите в Dashboards → Import
3. Загрузите JSON файлы дашбордов

### Алерты

Настройте алерты в Grafana для:
- Высокой latency API (>500ms p95)
- Глубины очередей RabbitMQ (>1000 сообщений)
- Ошибок в Sentry (>10/мин)
- Недоступности сервисов

## Безопасность

### TLS/SSL

Для production используйте обратный прокси (Nginx/Traefik) с TLS:

```yaml
# Traefik example
labels:
  - "traefik.http.routers.backend.rule=Host(`api.example.com`)"
  - "traefik.http.routers.backend.tls=true"
  - "traefik.http.routers.backend.tls.certresolver=myresolver"
```

### Secrets Management

В production используйте HashiCorp Vault или аналоги:

```bash
# Пример получения секрета из Vault
export DB_PASSWORD=$(vault kv get -field=password secret/db)
```

### ФСТЭК требования

- Шифрование данных at rest (AES-256)
- Шифрование in transit (TLS 1.3)
- Неизменяемость аудит-логов
- Разграничение прав доступа (RBAC)
- Локализация данных в РФ

## Troubleshooting

### Backend не запускается

```bash
# Проверка логов
docker-compose logs backend

# Проверка подключения к БД
docker-compose exec backend python -c "from backend.core.config import get_settings; print(get_settings().database_url)"
```

### Ошибки миграций

```bash
# Сброс и повторная инициализация БД (WARNING: данные будут удалены!)
docker-compose down -v
docker-compose up -d postgres
# Подождите готовности БД
docker-compose up -d
```

### Проблемы с очередями

```bash
# Очистка очередей RabbitMQ
docker-compose exec rabbitmq rabbitmqctl purge_queue <queue_name>

# Перезапуск workers
docker-compose restart celery-worker
```

## Контакты и поддержка

- Документация: `/docs`
- API Spec: `/openapi.json`
- Issues: GitHub Issues
- Чат: Slack/Telegram канал проекта
