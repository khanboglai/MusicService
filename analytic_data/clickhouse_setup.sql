-- consumer
-- принимает сырые данные от базы и хранит их строкой
CREATE TABLE IF NOT EXISTS kafka_analytic (
    _raw String
) ENGINE = Kafka(
  'kafka:9092',                      -- Брокер Kafka
  'debezium_AnalyticsInteractions.public.AnalyticsInteractions', -- Топик
  'clickhouse-group',                -- Группа потребителя
  'JSONAsString'                     -- Формат данных
)
-- для тестов маленькие значения ставим, для прода большие
SETTINGS
  kafka_max_block_size = 3,      -- Макс. сообщений в блоке
  kafka_poll_timeout_ms = 5000,      -- Таймаут опроса (мс)
  kafka_flush_interval_ms = 10000;   -- Интервал сброса (мс)


CREATE TABLE IF NOT EXISTS interactions (
    user_id Int64,
    track_id Int64,
    track_name String,
    artist_id Int64,
    artist_name String,
    genre_id Int64,
    genre_name String,
    listen_time Int64,
    interaction_date DateTime,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (track_id);


CREATE TABLE IF NOT EXISTS interactions_raw_buffer (
    user_id Int64,
    track_id Int64,
    track_name String,
    artist_id Int64,
    artist_name String,
    genre_id Int64,
    genre_name String,
    listen_time Int64,
    interaction_date DateTime,
    created_at DateTime DEFAULT now()
) ENGINE = Buffer(
  'default',                  -- База данных
  'interactions',         -- Целевая таблица
  16,                        -- Количество "ведер"
  3,                        -- Минимальная задержка в секундах (1 минута)
  10,                      -- Максимальная задержка в секундах (1 час)
  1,                     -- Минимальное количество строк для сброса
  100000,                    -- Максимальное количество строк для сброса
  10000000,                  -- Минимальный размер данных в байтах для сброса
  100000000                  -- Максимальный размер данных в байтах для сброса
);


CREATE MATERIALIZED VIEW interactions_raw_mv TO interactions_raw_buffer AS
SELECT
    JSONExtractInt(_raw, 'after', 'user_id') AS user_id,
    JSONExtractInt(_raw, 'after', 'track_id') AS track_id,
    JSONExtractString(_raw, 'after', 'track_name') AS track_name,
    JSONExtractInt(_raw, 'after', 'artist_id') AS artist_id,
    JSONExtractString(_raw, 'after', 'artist_name') AS artist_name,
    JSONExtractInt(_raw, 'after', 'genre_id') AS genre_id,
    JSONExtractString(_raw, 'after', 'genre_name') AS genre_name,
    JSONExtractInt(_raw, 'after', 'listen_time') AS listen_time,
    parseDateTime64BestEffort(JSONExtractString(_raw, 'after', 'last_interaction'), 6) AS interaction_date
FROM kafka_analytic
WHERE JSONExtractString(_raw, 'op') IN ('c', 'u', 'r');


-- запросы для аналитики

-- Track per day
SELECT
    track_name,
    sum(toHour(interaction_date) BETWEEN 6 AND 11) AS "Утро (6:00-12:00)",
    sum(toHour(interaction_date) BETWEEN 12 AND 17) AS "День (12:00-18:00)",
    sum(toHour(interaction_date) BETWEEN 18 AND 23) AS "Вечер (18:00-00:00)",
    sum(toHour(interaction_date) BETWEEN 0 AND 5 OR toHour(interaction_date) = 23) AS "Ночь (00:00-6:00)"
FROM interactions
GROUP BY track_name
LIMIT 20;


-- top artists per season
SELECT
    season,
    artist_name,
    interactions
FROM (
    SELECT
        CASE
            WHEN toMonth(interaction_date) IN (12, 1, 2) THEN 'Winter'
            WHEN toMonth(interaction_date) IN (3, 4, 5) THEN 'Spring'
            WHEN toMonth(interaction_date) IN (6, 7, 8) THEN 'Summer'
            WHEN toMonth(interaction_date) IN (9, 10, 11) THEN 'Autumn'
        END AS season,
        artist_name,
        count() AS interactions,
        row_number() OVER (PARTITION BY
            CASE
                WHEN toMonth(interaction_date) IN (12, 1, 2) THEN 'Winter'
                WHEN toMonth(interaction_date) IN (3, 4, 5) THEN 'Spring'
                WHEN toMonth(interaction_date) IN (6, 7, 8) THEN 'Summer'
                WHEN toMonth(interaction_date) IN (9, 10, 11) THEN 'Autumn'
            END
            ORDER BY count() DESC) AS rank
    FROM interactions
    WHERE toYear(interaction_date) = 2024
    GROUP BY
        artist_name,
        season
) t
WHERE rank <= 3
ORDER BY
    CASE season
        WHEN 'Winter' THEN 1
        WHEN 'Spring' THEN 2
        WHEN 'Summer' THEN 3
        WHEN 'Autumn' THEN 4
    END,
    interactions DESC


-- Statistic by day part
SELECT
    CASE
        WHEN toHour(interaction_date) BETWEEN 6 AND 11 THEN 'Утро (06:00-12:00)'
        WHEN toHour(interaction_date) BETWEEN 12 AND 17 THEN 'День (12:00-18:00)'
        WHEN toHour(interaction_date) BETWEEN 18 AND 23 THEN 'Вечер (18:00-00:00)'
        ELSE 'Ночь (00:00-06:00)'
    END AS time_period,
    count() AS interactions_
FROM interactions
GROUP BY time_period
ORDER BY
    CASE time_period
        WHEN 'Утро (06:00-12:00)' THEN 1
        WHEN 'День (12:00-18:00)' THEN 2
        WHEN 'Вечер (18:00-00:00)' THEN 3
        ELSE 4
    END;


-- Top track per season
SELECT
    season,
    track_name,
    interactions
FROM (
    SELECT
        CASE
            WHEN toMonth(interaction_date) IN (12, 1, 2) THEN 'Winter'
            WHEN toMonth(interaction_date) IN (3, 4, 5) THEN 'Spring'
            WHEN toMonth(interaction_date) IN (6, 7, 8) THEN 'Summer'
            WHEN toMonth(interaction_date) IN (9, 10, 11) THEN 'Autumn'
        END AS season,
        track_name,
        count() AS interactions,
        row_number() OVER (PARTITION BY
            CASE
                WHEN toMonth(interaction_date) IN (12, 1, 2) THEN 'Winter'
                WHEN toMonth(interaction_date) IN (3, 4, 5) THEN 'Spring'
                WHEN toMonth(interaction_date) IN (6, 7, 8) THEN 'Summer'
                WHEN toMonth(interaction_date) IN (9, 10, 11) THEN 'Autumn'
            END
            ORDER BY count() DESC) AS rank
    FROM interactions
    WHERE toYear(interaction_date) = 2024
    GROUP BY
        track_name,
        season
) t
WHERE rank <= 3
ORDER BY
    CASE season
        WHEN 'Winter' THEN 1
        WHEN 'Spring' THEN 2
        WHEN 'Summer' THEN 3
        WHEN 'Autumn' THEN 4
    END,
    interactions DESC


-- top 3 tracks per 30 days
SELECT
    track_name,
    count(*) AS interactions
FROM interactions
WHERE interaction_date >= toDate(now() - toIntervalMonth(1))
GROUP BY track_name
ORDER BY interactions DESC
LIMIT 3;


-- top 3 artists per 30 days
SELECT
    artist_name,
    count(*) AS interactions
FROM interactions
WHERE interaction_date >= toDate(now() - toIntervalMonth(1))
GROUP BY artist_name
ORDER BY interactions DESC
LIMIT 3;

-- top 3 genres per 30 days
SELECT
    genre_name,
    count(*) AS interactions
FROM interactions
WHERE interaction_date >= toDate(now() - toIntervalMonth(1))
GROUP BY genre_name
ORDER BY interactions DESC
LIMIT 3;
