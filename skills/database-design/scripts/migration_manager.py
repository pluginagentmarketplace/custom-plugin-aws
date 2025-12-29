#!/usr/bin/env python3
"""
Database Migration Manager
Manages schema migrations with rollback support.
"""

import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor


class MigrationManager:
    """Manage database migrations."""

    def __init__(self, connection_string: str, migrations_dir: str = "migrations"):
        self.conn_string = connection_string
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(exist_ok=True)

    def _get_connection(self):
        """Get database connection."""
        return psycopg2.connect(self.conn_string)

    def _ensure_migrations_table(self):
        """Create migrations tracking table if not exists."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        id SERIAL PRIMARY KEY,
                        version VARCHAR(14) NOT NULL UNIQUE,
                        name VARCHAR(255) NOT NULL,
                        checksum VARCHAR(64) NOT NULL,
                        applied_at TIMESTAMPTZ DEFAULT NOW()
                    )
                """)
            conn.commit()

    def _get_applied_migrations(self) -> Dict[str, Dict]:
        """Get list of applied migrations."""
        self._ensure_migrations_table()
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM schema_migrations ORDER BY version")
                return {row["version"]: dict(row) for row in cur.fetchall()}

    def _get_pending_migrations(self) -> List[Path]:
        """Get list of pending migration files."""
        applied = self._get_applied_migrations()
        pending = []

        for file in sorted(self.migrations_dir.glob("*.sql")):
            version = file.stem.split("_")[0]
            if version not in applied:
                pending.append(file)

        return pending

    def _calculate_checksum(self, content: str) -> str:
        """Calculate SHA-256 checksum of migration content."""
        return hashlib.sha256(content.encode()).hexdigest()

    def create(self, name: str) -> Path:
        """Create a new migration file."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{name}.sql"
        filepath = self.migrations_dir / filename

        template = f"""-- Migration: {name}
-- Created: {datetime.now().isoformat()}

-- Up Migration
-- Write your forward migration SQL here

-- Example:
-- CREATE TABLE example (
--     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
--     name VARCHAR(255) NOT NULL,
--     created_at TIMESTAMPTZ DEFAULT NOW()
-- );

-- Down Migration (for rollback)
-- @rollback
-- DROP TABLE IF EXISTS example;
"""

        filepath.write_text(template)
        return filepath

    def migrate(self, target_version: str = None) -> List[str]:
        """Apply pending migrations."""
        applied = []
        pending = self._get_pending_migrations()

        with self._get_connection() as conn:
            for migration_file in pending:
                version = migration_file.stem.split("_")[0]

                if target_version and version > target_version:
                    break

                content = migration_file.read_text()
                up_sql = self._extract_up_migration(content)
                checksum = self._calculate_checksum(content)

                try:
                    with conn.cursor() as cur:
                        cur.execute(up_sql)
                        cur.execute(
                            """
                            INSERT INTO schema_migrations (version, name, checksum)
                            VALUES (%s, %s, %s)
                            """,
                            (version, migration_file.stem, checksum)
                        )
                    conn.commit()
                    applied.append(migration_file.stem)
                    print(f"Applied: {migration_file.stem}")
                except Exception as e:
                    conn.rollback()
                    raise RuntimeError(f"Migration {migration_file.stem} failed: {e}")

        return applied

    def rollback(self, steps: int = 1) -> List[str]:
        """Rollback last N migrations."""
        rolled_back = []
        applied = self._get_applied_migrations()
        versions = sorted(applied.keys(), reverse=True)[:steps]

        with self._get_connection() as conn:
            for version in versions:
                migration_file = None
                for f in self.migrations_dir.glob(f"{version}_*.sql"):
                    migration_file = f
                    break

                if not migration_file:
                    continue

                content = migration_file.read_text()
                down_sql = self._extract_down_migration(content)

                if not down_sql:
                    print(f"No rollback SQL for {migration_file.stem}")
                    continue

                try:
                    with conn.cursor() as cur:
                        cur.execute(down_sql)
                        cur.execute(
                            "DELETE FROM schema_migrations WHERE version = %s",
                            (version,)
                        )
                    conn.commit()
                    rolled_back.append(migration_file.stem)
                    print(f"Rolled back: {migration_file.stem}")
                except Exception as e:
                    conn.rollback()
                    raise RuntimeError(f"Rollback {migration_file.stem} failed: {e}")

        return rolled_back

    def _extract_up_migration(self, content: str) -> str:
        """Extract up migration SQL from file content."""
        lines = content.split("\n")
        up_lines = []
        in_rollback = False

        for line in lines:
            if "@rollback" in line.lower():
                in_rollback = True
                continue
            if not in_rollback and not line.strip().startswith("--"):
                up_lines.append(line)

        return "\n".join(up_lines)

    def _extract_down_migration(self, content: str) -> Optional[str]:
        """Extract down migration SQL from file content."""
        lines = content.split("\n")
        down_lines = []
        in_rollback = False

        for line in lines:
            if "@rollback" in line.lower():
                in_rollback = True
                continue
            if in_rollback and not line.strip().startswith("--"):
                down_lines.append(line)

        return "\n".join(down_lines) if down_lines else None

    def status(self) -> Dict:
        """Get migration status."""
        applied = self._get_applied_migrations()
        pending = self._get_pending_migrations()

        return {
            "applied": len(applied),
            "pending": len(pending),
            "applied_migrations": list(applied.keys()),
            "pending_migrations": [p.stem for p in pending]
        }


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Migration Manager")
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL"))
    parser.add_argument("--migrations-dir", default="migrations")

    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("name", help="Migration name")

    subparsers.add_parser("migrate")
    subparsers.add_parser("status")

    rollback_parser = subparsers.add_parser("rollback")
    rollback_parser.add_argument("--steps", type=int, default=1)

    args = parser.parse_args()

    if not args.database_url:
        print("Error: DATABASE_URL not set")
        return

    manager = MigrationManager(args.database_url, args.migrations_dir)

    if args.command == "create":
        path = manager.create(args.name)
        print(f"Created: {path}")
    elif args.command == "migrate":
        manager.migrate()
    elif args.command == "rollback":
        manager.rollback(args.steps)
    elif args.command == "status":
        import json
        print(json.dumps(manager.status(), indent=2))


if __name__ == "__main__":
    main()
