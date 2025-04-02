#!/bin/bash

# Load environment variables
set -a
source ../.env
set +a

# Set backup filename with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_PATH}/db_backup_${TIMESTAMP}.sql"
BACKUP_FILE_COMPRESSED="${BACKUP_FILE}.gz"

# Create backup
echo "Creating database backup..."
docker-compose exec -T db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > ${BACKUP_FILE}

# Compress backup
echo "Compressing backup..."
gzip ${BACKUP_FILE}

# Delete old backups
echo "Cleaning old backups..."
find ${BACKUP_PATH} -name "db_backup_*.sql.gz" -type f -mtime +${BACKUP_RETENTION_DAYS} -delete

# Backup configuration files
echo "Backing up configuration files..."
CONFIG_BACKUP="${BACKUP_PATH}/config_backup_${TIMESTAMP}.tar.gz"
tar -czf ${CONFIG_BACKUP} \
    ../docker-compose.yml \
    ../.env \
    ../deployment/nginx/

# Keep only recent config backups
find ${BACKUP_PATH} -name "config_backup_*.tar.gz" -type f -mtime +${BACKUP_RETENTION_DAYS} -delete

echo "Backup completed successfully!"