-- первый способ
-- -- 1. Создаём таблицу для чтения из Kafka (используем String вместо JSON)
-- CREATE TABLE kafka_inventory (
--     _raw String
-- ) ENGINE = Kafka(
--   'kafka:9092',
--   'debezium_inventory.public.inventory',
--   'clickhouse-group',
--   'JSONAsString'
-- );
--
-- -- 2. Создаём целевую таблицу
-- CREATE TABLE inventory (
--     id Int32,
--     name String,
--     quantity Int32
-- ) ENGINE = MergeTree()
-- ORDER BY id;
--
-- -- 3. Создаём материализованное представление с парсингом JSON через функции JSONExtract*
-- CREATE MATERIALIZED VIEW inventory_mv TO inventory AS
-- SELECT
--     JSONExtractInt(_raw, 'after', 'id') as id,
--     JSONExtractString(_raw, 'after', 'name') as name,
--     JSONExtractInt(_raw, 'after', 'quantity') as quantity
-- FROM kafka_inventory
-- WHERE JSONExtractString(_raw, 'op') IN ('c', 'u', 'r'); -- 'c'=create, 'u'=update, 'r'=read
--
--
-- select * from inventory;

-- второй способ
-- этот способ лучше, так как мы кусками сбрасываем данные в хранилище. Для "прода" надо выставлять не 3, а 1000 или больше

-- consumer
-- принимает сырые данные от базы и хранит их строкой
CREATE TABLE kafka_inventory (
    _raw String
) ENGINE = Kafka(
  'kafka:9092',                      -- Брокер Kafka
  'debezium_inventory.public.inventory', -- Топик
  'clickhouse-group',                -- Группа потребителя
  'JSONAsString'                     -- Формат данных
)
-- для тестов маленькие значения ставим, для прода большие
SETTINGS
  kafka_max_block_size = 3,      -- Макс. сообщений в блоке
  kafka_poll_timeout_ms = 5000,      -- Таймаут опроса (мс)
  kafka_flush_interval_ms = 10000;   -- Интервал сброса (мс)


-- таблица в clickhouse, хранит наши данные
CREATE TABLE inventory (
    id Int32,
    name String,
    quantity Int32
    -- Опционально для дедупликации (если данные могут дублироваться)
)
ENGINE = MergeTree()  -- Удаляет дубликаты по версии
ORDER BY (id);                        -- Сортировка для быстрого поиска


-- накопительный буфер, чтобы скидывать не по одной строке, а сразу по несколько
CREATE TABLE inventory_buffer (
    id Int32,
    name String,
    quantity Int32,
    _batch_time DateTime DEFAULT now()
) ENGINE = Buffer(
  'default',                     -- База назначения
  'inventory',                   -- Таблица назначения
  16,                            -- Количество "ведер" (buckets)
  10,                            -- Мин. время задержки (сек)  его можно поменять для тестов
  60,                            -- Макс. время задержки (сек)
  3,                          -- Мин. строк для сброса
  10000,                         -- Макс. строк для сброса
  1000000,                       -- Мин. размер данных (байт)
  10000000,                      -- Макс. размер данных (байт)
  10000,                         -- Интервал сброса по времени (мс)
  10000,                         -- Интервал сброса по строкам
  10000000                       -- Интервал сброса по размеру (байт)
);


-- представление, парсинг данных кафки в нормальные поля таблицы inventory
CREATE MATERIALIZED VIEW inventory_mv TO inventory_buffer AS
SELECT
    JSONExtractInt(_raw, 'after', 'id') as id,
    JSONExtractString(_raw, 'after', 'name') as name,
    JSONExtractInt(_raw, 'after', 'quantity') as quantity
FROM kafka_inventory
WHERE JSONExtractString(_raw, 'op') IN ('c', 'u', 'r'); -- 'c'=create, 'u'=update, 'r'=read
