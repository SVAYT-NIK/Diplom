-- Инициализация базы данных PostgreSQL 15
-- Адаптировано для обычного PostgreSQL (без TimescaleDB)
-- Используется нативное декларативное партиционирование

-- Включение необходимых расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Основная таблица для временных рядов измерений с партиционированием
CREATE TABLE IF NOT EXISTS metering_data (
    time TIMESTAMPTZ NOT NULL,
    device_id VARCHAR(100) NOT NULL,
    mcd_id UUID NOT NULL,
    parameter_type VARCHAR(50) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'valid',
    quality_flag INTEGER DEFAULT 100,
    metadata JSONB DEFAULT '{}'::jsonb
) PARTITION BY RANGE (time);

-- Создание партиций по месяцам (пример на 2 года вперёд)
-- В продакшене можно автоматизировать создание будущих партиций через cron
CREATE TABLE IF NOT EXISTS metering_data_2024_01 PARTITION OF metering_data
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE IF NOT EXISTS metering_data_2024_02 PARTITION OF metering_data
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
CREATE TABLE IF NOT EXISTS metering_data_2024_03 PARTITION OF metering_data
    FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');
CREATE TABLE IF NOT EXISTS metering_data_2024_04 PARTITION OF metering_data
    FOR VALUES FROM ('2024-04-01') TO ('2024-05-01');
CREATE TABLE IF NOT EXISTS metering_data_2024_05 PARTITION OF metering_data
    FOR VALUES FROM ('2024-05-01') TO ('2024-06-01');
CREATE TABLE IF NOT EXISTS metering_data_2024_06 PARTITION OF metering_data
    FOR VALUES FROM ('2024-06-01') TO ('2024-07-01');
CREATE TABLE IF NOT EXISTS metering_data_2024_07 PARTITION OF metering_data
    FOR VALUES FROM ('2024-07-01') TO ('2024-08-01');
CREATE TABLE IF NOT EXISTS metering_data_2024_08 PARTITION OF metering_data
    FOR VALUES FROM ('2024-08-01') TO ('2024-09-01');
CREATE TABLE IF NOT EXISTS metering_data_2024_09 PARTITION OF metering_data
    FOR VALUES FROM ('2024-09-01') TO ('2024-10-01');
CREATE TABLE IF NOT EXISTS metering_data_2024_10 PARTITION OF metering_data
    FOR VALUES FROM ('2024-10-01') TO ('2024-11-01');
CREATE TABLE IF NOT EXISTS metering_data_2024_11 PARTITION OF metering_data
    FOR VALUES FROM ('2024-11-01') TO ('2024-12-01');
CREATE TABLE IF NOT EXISTS metering_data_2024_12 PARTITION OF metering_data
    FOR VALUES FROM ('2024-12-01') TO ('2025-01-01');
CREATE TABLE IF NOT EXISTS metering_data_2025_01 PARTITION OF metering_data
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
CREATE TABLE IF NOT EXISTS metering_data_2025_02 PARTITION OF metering_data
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
CREATE TABLE IF NOT EXISTS metering_data_2025_03 PARTITION OF metering_data
    FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');
CREATE TABLE IF NOT EXISTS metering_data_2025_04 PARTITION OF metering_data
    FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');
CREATE TABLE IF NOT EXISTS metering_data_2025_05 PARTITION OF metering_data
    FOR VALUES FROM ('2025-05-01') TO ('2025-06-01');
CREATE TABLE IF NOT EXISTS metering_data_2025_06 PARTITION OF metering_data
    FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');

-- Индексы для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_metering_device_time 
    ON metering_data (device_id, time DESC);

CREATE INDEX IF NOT EXISTS idx_metering_mcd_time 
    ON metering_data (mcd_id, time DESC);

CREATE INDEX IF NOT EXISTS idx_metering_parameter_time 
    ON metering_data (parameter_type, time DESC);

-- Таблица для погодных данных с партиционированием
CREATE TABLE IF NOT EXISTS weather_data (
    time TIMESTAMPTZ NOT NULL,
    location_id VARCHAR(100) NOT NULL,
    temperature_out DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    wind_speed DOUBLE PRECISION,
    solar_radiation DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    metadata JSONB DEFAULT '{}'::jsonb
) PARTITION BY RANGE (time);

-- Партиции для погодных данных
CREATE TABLE IF NOT EXISTS weather_data_2024_01 PARTITION OF weather_data
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE IF NOT EXISTS weather_data_2024_02 PARTITION OF weather_data
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
CREATE TABLE IF NOT EXISTS weather_data_2024_03 PARTITION OF weather_data
    FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');
CREATE TABLE IF NOT EXISTS weather_data_2024_04 PARTITION OF weather_data
    FOR VALUES FROM ('2024-04-01') TO ('2024-05-01');
CREATE TABLE IF NOT EXISTS weather_data_2024_05 PARTITION OF weather_data
    FOR VALUES FROM ('2024-05-01') TO ('2024-06-01');
CREATE TABLE IF NOT EXISTS weather_data_2024_06 PARTITION OF weather_data
    FOR VALUES FROM ('2024-06-01') TO ('2024-07-01');
CREATE TABLE IF NOT EXISTS weather_data_2024_07 PARTITION OF weather_data
    FOR VALUES FROM ('2024-07-01') TO ('2024-08-01');
CREATE TABLE IF NOT EXISTS weather_data_2024_08 PARTITION OF weather_data
    FOR VALUES FROM ('2024-08-01') TO ('2024-09-01');
CREATE TABLE IF NOT EXISTS weather_data_2024_09 PARTITION OF weather_data
    FOR VALUES FROM ('2024-09-01') TO ('2024-10-01');
CREATE TABLE IF NOT EXISTS weather_data_2024_10 PARTITION OF weather_data
    FOR VALUES FROM ('2024-10-01') TO ('2024-11-01');
CREATE TABLE IF NOT EXISTS weather_data_2024_11 PARTITION OF weather_data
    FOR VALUES FROM ('2024-11-01') TO ('2024-12-01');
CREATE TABLE IF NOT EXISTS weather_data_2024_12 PARTITION OF weather_data
    FOR VALUES FROM ('2024-12-01') TO ('2025-01-01');
CREATE TABLE IF NOT EXISTS weather_data_2025_01 PARTITION OF weather_data
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
CREATE TABLE IF NOT EXISTS weather_data_2025_02 PARTITION OF weather_data
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
CREATE TABLE IF NOT EXISTS weather_data_2025_03 PARTITION OF weather_data
    FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');
CREATE TABLE IF NOT EXISTS weather_data_2025_04 PARTITION OF weather_data
    FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');
CREATE TABLE IF NOT EXISTS weather_data_2025_05 PARTITION OF weather_data
    FOR VALUES FROM ('2025-05-01') TO ('2025-06-01');
CREATE TABLE IF NOT EXISTS weather_data_2025_06 PARTITION OF weather_data
    FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');

CREATE INDEX IF NOT EXISTS idx_weather_location_time 
    ON weather_data (location_id, time DESC);

-- Таблица для агрегированных данных (часовые/дневные сводки)
CREATE TABLE IF NOT EXISTS consumption_aggregates (
    time TIMESTAMPTZ NOT NULL,
    mcd_id UUID NOT NULL,
    parameter_type VARCHAR(50) NOT NULL,
    aggregation_period VARCHAR(20) NOT NULL, -- 'hour', 'day', 'month'
    total_value DOUBLE PRECISION NOT NULL,
    avg_value DOUBLE PRECISION NOT NULL,
    min_value DOUBLE PRECISION,
    max_value DOUBLE PRECISION,
    sample_count INTEGER NOT NULL,
    gsop_normalized DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_aggregates_mcd_period 
    ON consumption_aggregates (mcd_id, aggregation_period, time DESC);

-- Таблица для результатов анализа аномалий
CREATE TABLE IF NOT EXISTS anomaly_results (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    time TIMESTAMPTZ NOT NULL,
    mcd_id UUID NOT NULL,
    device_id VARCHAR(100),
    anomaly_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    score DOUBLE PRECISION NOT NULL,
    actual_value DOUBLE PRECISION,
    expected_value DOUBLE PRECISION,
    detectors TEXT[], -- Массив детекторов, обнаруживших аномалию
    status VARCHAR(20) DEFAULT 'new',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_anomalies_mcd_time 
    ON anomaly_results (mcd_id, time DESC);

CREATE INDEX IF NOT EXISTS idx_anomalies_status 
    ON anomaly_results (status);

-- Таблица для прогнозов
CREATE TABLE IF NOT EXISTS forecasts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    mcd_id UUID NOT NULL,
    parameter_type VARCHAR(50) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    forecast_horizon_hours INTEGER NOT NULL,
    predictions JSONB NOT NULL, -- Массив {timestamp, value, lower_bound, upper_bound}
    metrics JSONB, -- {mae, rmse, mape}
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_forecasts_mcd 
    ON forecasts (mcd_id, created_at DESC);

-- Функция для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггеры для updated_at
CREATE TRIGGER update_anomaly_updated_at
    BEFORE UPDATE ON anomaly_results
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Функция для управления retention policy (удаление старых данных)
-- В отличие от TimescaleDB, в обычном PostgreSQL нужно вручную управлять удалением партиций
CREATE OR REPLACE FUNCTION drop_old_partitions(table_name TEXT, retention_interval INTERVAL)
RETURNS VOID AS $$
DECLARE
    partition_record RECORD;
    cutoff_time TIMESTAMPTZ;
BEGIN
    cutoff_time := NOW() - retention_interval;
    
    -- Поиск и удаление партиций, которые полностью старше cutoff_time
    FOR partition_record IN 
        SELECT inhrelid::regclass::text AS partition_name,
               pg_get_expr(relpartbound, inhrelid) AS partition_bound
        FROM pg_inherits
        JOIN pg_class parent ON pg_inherits.inhparent = parent.oid
        JOIN pg_class child ON pg_inherits.inhrelid = child.oid
        WHERE parent.relname = table_name
    LOOP
        -- Извлечение верхней границы партиции (упрощённая логика)
        -- В продакшене нужен более сложный парсер pg_get_expr результата
        IF partition_record.partition_bound LIKE '%' || to_char(cutoff_time, 'YYYY-MM-DD') || '%' THEN
            -- Пропускаем удаление, если партиция содержит актуальные данные
            CONTINUE;
        END IF;
        
        -- Здесь можно добавить логику удаления старых партиций
        -- EXECUTE format('DROP TABLE IF EXISTS %I CASCADE', partition_record.partition_name);
        RAISE NOTICE 'Partition % is older than %, consider manual cleanup', 
                     partition_record.partition_name, retention_interval;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Замечание: Политики хранения данных (retention policies) для обычного PostgreSQL
-- В TimescaleDB использовались функции add_retention_policy, которые автоматически удаляют старые данные.
-- В обычном PostgreSQL необходимо:
-- 1. Регулярно запускать функцию drop_old_partitions через pg_cron или внешний планировщик
-- 2. Вручную создавать новые партиции перед началом нового месяца
-- 3. Мониторить размер таблиц и при необходимости архивировать данные в MinIO

-- Пример вызова для очистки данных старше 3 лет (раскомментировать для использования):
-- SELECT drop_old_partitions('metering_data', INTERVAL '3 years');
-- SELECT drop_old_partitions('weather_data', INTERVAL '3 years');

-- Компрессия данных:
-- В обычном PostgreSQL нет встроенной компрессии на уровне таблиц как в TimescaleDB.
-- Рекомендации:
-- 1. Использовать TOAST для автоматического сжатия больших полей (JSONB, TEXT)
-- 2. Настроить сжатие на уровне файловой системы или использовать ZFS
-- 3. Архивировать старые партиции в MinIO с применением gzip/zstd
-- 4. Рассмотреть расширение pg_compression для PostgreSQL 14+

-- Представление для быстрой статистики по МКД
CREATE OR REPLACE VIEW mcd_stats AS
SELECT 
    mcd_id,
    COUNT(DISTINCT device_id) as devices_count,
    MAX(time) as last_measurement,
    MIN(time) as first_measurement
FROM metering_data
GROUP BY mcd_id;

COMMENT ON TABLE metering_data IS 'Временные ряды измерений приборов учёта (партицированная таблица PostgreSQL)';
COMMENT ON TABLE weather_data IS 'Погодные данные (партицированная таблица PostgreSQL)';
COMMENT ON TABLE consumption_aggregates IS 'Агрегированные данные потребления';
COMMENT ON TABLE anomaly_results IS 'Результаты детекции аномалий';
COMMENT ON TABLE forecasts IS 'Прогнозы потребления';
COMMENT ON FUNCTION drop_old_partitions IS 'Функция для удаления старых партиций (аналог retention policy TimescaleDB)';
