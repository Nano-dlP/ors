#!/bin/bash

############################
# CONFIGURACION
############################

DB_NAME="db_salud_mental"
DB_USER="postgres"
DB_PASSWORD="Playadito_22"
DB_HOST="localhost"
DB_PORT="5432"

BACKUP_DIR="/var/backups/postgres"

DAILY_DIR="$BACKUP_DIR/daily"
WEEKLY_DIR="$BACKUP_DIR/weekly"
MONTHLY_DIR="$BACKUP_DIR/monthly"

DATE=$(date +"%Y-%m-%d_%H-%M")
DAY_OF_WEEK=$(date +%u)
DAY_OF_MONTH=$(date +%d)

export PGPASSWORD=$DB_PASSWORD

############################
# CREAR CARPETAS
############################

mkdir -p $DAILY_DIR
mkdir -p $WEEKLY_DIR
mkdir -p $MONTHLY_DIR

############################
# BACKUP DIARIO
############################

pg_dump -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME | gzip > $DAILY_DIR/${DB_NAME}_$DATE.sql.gz

############################
# BACKUP SEMANAL (domingo)
############################

if [ "$DAY_OF_WEEK" -eq 7 ]; then
    pg_dump -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME | gzip > $WEEKLY_DIR/${DB_NAME}_$DATE.sql.gz
fi

############################
# BACKUP MENSUAL (día 1)
############################

if [ "$DAY_OF_MONTH" -eq 01 ]; then
    pg_dump -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME | gzip > $MONTHLY_DIR/${DB_NAME}_$DATE.sql.gz
fi

############################
# LIMPIEZA AUTOMATICA
############################

# borrar diarios de más de 7 días
find $DAILY_DIR -type f -mtime +7 -delete

# borrar semanales de más de 30 días
find $WEEKLY_DIR -type f -mtime +30 -delete

# borrar mensuales de más de 365 días
find $MONTHLY_DIR -type f -mtime +365 -delete

echo "Backup completado: $DATE"