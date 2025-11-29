cat > infra/scripts/bootstrap_db.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

echo "[bootstrap_db] Starting database bootstrap..."

DB_HOST="${POSTGRES_HOST:-db}"
DB_PORT="${POSTGRES_PORT:-5432}"

echo "[bootstrap_db] DB host: ${DB_HOST}, port: ${DB_PORT}"
echo "[bootstrap_db] Assuming init.sql was applied by Postgres entrypoint."

echo "[bootstrap_db] Done."
EOF

chmod +x infra/scripts/bootstrap_db.sh
