#!/bin/bash
exec >> init.log 2>&1
set -e

set -a
source ./src/.env
set +a

echo "[*] Иницилизации Базы Данных..."
./wait-for-it.sh postgres:5432 --timeout=30 --strict -- echo "База данных в работе!"


# PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c '\q' 2>/dev/null

# if [ $? -eq 0 ]; then
#   echo "База данных '$DB_NAME' доступна.\n"
# else
#   echo "Не удалось подключиться к базе '$DB_NAME'.\n"
#   exit 1
# fi

# python3 ./src/check_connect_to_bd.py

if [ ! -f ./src/certs/private.pem ]; then
  echo "[*] Генерация RSA ключей..."
  mkdir -p certs
  openssl genrsa -out certs/private.pem 2048
  openssl rsa -in certs/private.pem -pubout -out certs/public.pem
fi

alembic upgrade head

echo "[*] Создание администратора..."
python -m src.init_admin

exec uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

# echo "[*] Запуск приложения..."
# python3 -m src.main