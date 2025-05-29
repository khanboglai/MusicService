## Инструкция по настройке пайплайна аналитики

1. Создать папку `plugins` в `analytic_data`
2. Дать права на папку: 
```bash 
sudo chmod -R a+rwx ./plugins
```
*это нужно для grafana*
3. Установить плагины для `debezium`

```bash
mkdir -p analytic_data/plugins/debezium
cd analytic_data/plugins/debezium
wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/2.3.3.Final/debezium-connector-postgres-2.3.3.Final-plugin.tar.gz
tar -xzf debezium-connector-postgres-2.3.3.Final-plugin.tar.gz
```
4. Запустить внешний `docker-compose`.
5. Дождаться, когда все логи остановятся
6. Выполнить регистрацию нового `connector`.

**Перед выполнением запроса проверить, что WAL в БД включен**

```docker
command:
  - "postgres"
  - "-c"
  - "wal_level=logical"
  - "-c"
  - "max_wal_senders=10"
  - "-c"
  - "max_replication_slots=10"
```

```bash
curl -i -X POST -H "Accept:application/json" \
  -H "Content-Type:application/json" http://localhost:8083/connectors/ \
  -d '{
    "name": "AnalyticsInteractions-connector",
    "config": {
      "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
      "database.hostname": "listener_postgres_db",
      "database.port": "5432",
      "database.user": "debug",
      "database.password": "pswd",
      "database.dbname": "listener",
      "database.server.name": "AnalyticsInteractions-server",
      "topic.prefix": "debezium_AnalyticsInteractions",
      "schema.include.list": "public",
      "table.include.list": "public.AnalyticsInteractions",
      "snapshot.mode": "initial",
      "plugin.name": "pgoutput",
      "publication.name": "dbz_publication",
      "slot.name": "dbz_slot",
      "key.converter": "org.apache.kafka.connect.json.JsonConverter",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "key.converter.schemas.enable": "false",
      "value.converter.schemas.enable": "false"
    }
}'
```
*Тут уже все готово для проекта*

*debezium работает с любым пользователем БД*

7. Подключение к `clickhouse`
8. Выполняем команды из `clickhouse_setup.sql`
9. Если все правильно сделали, то все будет работать.

10. `grafana` сразу доступна, в ней надо установить плагин для работы с ckickhouse.

*administration->plugins and data-> plugins->ClickHouse*

11. Витрины создаем сами или импортируем из `json`, которые лежат в `analytic_data`