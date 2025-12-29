#!/bin/bash
# RDS Backup and Restore Script

set -e

echo "💾 RDS Backup/Restore Utility"
echo "============================="

usage() {
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  snapshot <db-id>           Create manual snapshot"
    echo "  list <db-id>               List snapshots for instance"
    echo "  restore <snapshot-id>      Restore from snapshot"
    echo "  export <db-id>             Export to S3 (Aurora only)"
    echo "  status <db-id>             Check instance status"
}

if [ $# -lt 2 ]; then
    usage
    exit 1
fi

COMMAND=$1
DB_ID=$2
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

case $COMMAND in
    snapshot)
        SNAPSHOT_ID="${DB_ID}-snapshot-${TIMESTAMP}"
        echo "📸 Creating snapshot: $SNAPSHOT_ID"

        aws rds create-db-snapshot \
            --db-instance-identifier "$DB_ID" \
            --db-snapshot-identifier "$SNAPSHOT_ID"

        echo "Waiting for snapshot to complete..."
        aws rds wait db-snapshot-available \
            --db-snapshot-identifier "$SNAPSHOT_ID"

        echo "✅ Snapshot created: $SNAPSHOT_ID"
        ;;

    list)
        echo "📋 Snapshots for $DB_ID:"
        aws rds describe-db-snapshots \
            --db-instance-identifier "$DB_ID" \
            --query 'DBSnapshots[].[DBSnapshotIdentifier,Status,SnapshotCreateTime]' \
            --output table
        ;;

    restore)
        SNAPSHOT_ID=$2
        NEW_DB_ID="${3:-${DB_ID}-restored}"

        echo "🔄 Restoring from $SNAPSHOT_ID to $NEW_DB_ID"

        aws rds restore-db-instance-from-db-snapshot \
            --db-instance-identifier "$NEW_DB_ID" \
            --db-snapshot-identifier "$SNAPSHOT_ID"

        echo "Waiting for instance to be available..."
        aws rds wait db-instance-available \
            --db-instance-identifier "$NEW_DB_ID"

        echo "✅ Restored to: $NEW_DB_ID"

        # Get endpoint
        ENDPOINT=$(aws rds describe-db-instances \
            --db-instance-identifier "$NEW_DB_ID" \
            --query 'DBInstances[0].Endpoint.Address' \
            --output text)

        echo "Endpoint: $ENDPOINT"
        ;;

    status)
        echo "📊 Status of $DB_ID:"
        aws rds describe-db-instances \
            --db-instance-identifier "$DB_ID" \
            --query 'DBInstances[0].{Status:DBInstanceStatus,Engine:Engine,Class:DBInstanceClass,MultiAZ:MultiAZ,Storage:AllocatedStorage,Endpoint:Endpoint.Address}' \
            --output table
        ;;

    *)
        echo "Unknown command: $COMMAND"
        usage
        exit 1
        ;;
esac
