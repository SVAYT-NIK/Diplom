-- Инициализация базы данных TimescaleDB

-- Включение расширения TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Создание гипертаблицы для временных рядов измерений
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
);

-- Преобразование в гипертаблицу (партиционирование по времени)
SELECT create_hypertable('metering_data', 'time', if_not_exists => TRUE);

-- Индексы для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_metering_device_time 
    ON metering_data (device_id, time DESC);

CREATE INDEX IF NOT EXISTS idx_metering_mcd_time 
    ON metering_data (mcd_id, time DESC);

CREATE INDEX IF NOT EXISTS idx_metering_parameter_time 
    ON metering_data (parameter_type, time DESC);

-- Гипертаблица для погодных данных
CREATE TABLE IF NOT EXISTS weather_data (
    time TIMESTAMPTZ NOT NULL,
    location_id VARCHAR(100) NOT NULL,
    temperature_out DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    wind_speed DOUBLE PRECISION,
    solar_radiation DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    metadata JSONB DEFAULT '{}'::jsonb
);

SELECT create_hypertable('weather_data', 'time', if_not_exists => TRUE);

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

SELECT create_hypertable('consumption_aggregates', 'time', if_not_exists => TRUE);

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

-- Политики хранения данных (retention policies)
-- Хранение сырых данных - 3 года (согласно ПП РФ №124)
SELECT add_retention_policy('metering_data', INTERVAL '3 years', if_not_exists => TRUE);
SELECT add_retention_policy('weather_data', INTERVAL '3 years', if_not_exists => TRUE);

-- Агрегированные данные - 5 лет
SELECT add_retention_policy('consumption_aggregates', INTERVAL '5 years', if_not_exists => TRUE);

-- Аномалии и прогнозы - 1 год
SELECT add_retention_policy('anomaly_results', INTERVAL '1 year', if_not_exists => TRUE);
SELECT add_retention_policy('forecasts', INTERVAL '6 months', if_not_exists => TRUE);

-- Компрессия данных для экономии места (сжатие старых данных)
SELECT add_compression_policy('metering_data', INTERVAL '30 days', if_not_exists => TRUE);
SELECT add_compression_policy('weather_data', INTERVAL '30 days', if_not_exists => TRUE);
SELECT add_compression_policy('consumption_aggregates', INTERVAL '90 days', if_not_exists => TRUE);

-- Представление для быстрой статистики по МКД
CREATE OR REPLACE VIEW mcd_stats AS
SELECT 
    mcd_id,
    COUNT(DISTINCT device_id) as devices_count,
    MAX(time) as last_measurement,
    MIN(time) as first_measurement
FROM metering_data
GROUP BY mcd_id;

COMMENT ON TABLE metering_data IS 'Временные ряды измерений приборов учёта (гипертаблица TimescaleDB)';
COMMENT ON TABLE weather_data IS 'Погодные данные (гипертаблица TimescaleDB)';
COMMENT ON TABLE consumption_aggregates IS 'Агрегированные данные потребления (гипертаблица)';
COMMENT ON TABLE anomaly_results IS 'Результаты детекции аномалий';
COMMENT ON TABLE forecasts IS 'Прогнозы потребления';
