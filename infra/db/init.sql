cat > infra/db/init.sql << 'EOF'
-- Phase 0: simple DB sanity setup. Extensions for TimescaleDB/pgvector will be added later.

CREATE TABLE IF NOT EXISTS app_health (
    id SERIAL PRIMARY KEY,
    checked_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
EOF
