#!/bin/bash
# CloudWatch Alarm Management Script

set -e

echo "🚨 CloudWatch Alarm Manager"
echo "==========================="

usage() {
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  create-ec2 <instance-id>    Create standard EC2 alarms"
    echo "  create-lambda <function>    Create Lambda alarms"
    echo "  create-rds <db-id>          Create RDS alarms"
    echo "  list                        List all alarms"
    echo "  status                      Show alarms in ALARM state"
    echo "  delete <alarm-name>         Delete alarm"
}

SNS_TOPIC=${SNS_TOPIC:-"arn:aws:sns:us-east-1:123456789012:alerts"}

create_alarm() {
    local NAME=$1
    local NAMESPACE=$2
    local METRIC=$3
    local DIMENSION_NAME=$4
    local DIMENSION_VALUE=$5
    local THRESHOLD=$6
    local COMPARISON=$7
    local STATISTIC=${8:-Average}
    local PERIOD=${9:-300}

    aws cloudwatch put-metric-alarm \
        --alarm-name "$NAME" \
        --metric-name "$METRIC" \
        --namespace "$NAMESPACE" \
        --statistic "$STATISTIC" \
        --period "$PERIOD" \
        --threshold "$THRESHOLD" \
        --comparison-operator "$COMPARISON" \
        --evaluation-periods 2 \
        --dimensions "Name=$DIMENSION_NAME,Value=$DIMENSION_VALUE" \
        --alarm-actions "$SNS_TOPIC" \
        --ok-actions "$SNS_TOPIC"

    echo "  ✅ Created: $NAME"
}

if [ $# -lt 1 ]; then
    usage
    exit 1
fi

COMMAND=$1
shift

case $COMMAND in
    create-ec2)
        INSTANCE_ID=$1
        echo "Creating EC2 alarms for $INSTANCE_ID..."

        create_alarm "${INSTANCE_ID}-high-cpu" \
            "AWS/EC2" "CPUUtilization" "InstanceId" "$INSTANCE_ID" \
            80 "GreaterThanThreshold"

        create_alarm "${INSTANCE_ID}-status-check" \
            "AWS/EC2" "StatusCheckFailed" "InstanceId" "$INSTANCE_ID" \
            1 "GreaterThanOrEqualToThreshold" "Maximum" 60

        echo "✅ EC2 alarms created!"
        ;;

    create-lambda)
        FUNCTION=$1
        echo "Creating Lambda alarms for $FUNCTION..."

        create_alarm "${FUNCTION}-errors" \
            "AWS/Lambda" "Errors" "FunctionName" "$FUNCTION" \
            5 "GreaterThanThreshold" "Sum" 60

        create_alarm "${FUNCTION}-duration" \
            "AWS/Lambda" "Duration" "FunctionName" "$FUNCTION" \
            10000 "GreaterThanThreshold" "Average" 60

        create_alarm "${FUNCTION}-throttles" \
            "AWS/Lambda" "Throttles" "FunctionName" "$FUNCTION" \
            1 "GreaterThanThreshold" "Sum" 60

        echo "✅ Lambda alarms created!"
        ;;

    create-rds)
        DB_ID=$1
        echo "Creating RDS alarms for $DB_ID..."

        create_alarm "${DB_ID}-high-cpu" \
            "AWS/RDS" "CPUUtilization" "DBInstanceIdentifier" "$DB_ID" \
            80 "GreaterThanThreshold"

        create_alarm "${DB_ID}-low-storage" \
            "AWS/RDS" "FreeStorageSpace" "DBInstanceIdentifier" "$DB_ID" \
            5368709120 "LessThanThreshold"  # 5GB

        create_alarm "${DB_ID}-connections" \
            "AWS/RDS" "DatabaseConnections" "DBInstanceIdentifier" "$DB_ID" \
            100 "GreaterThanThreshold"

        echo "✅ RDS alarms created!"
        ;;

    list)
        aws cloudwatch describe-alarms \
            --query 'MetricAlarms[].[AlarmName,StateValue,MetricName]' \
            --output table
        ;;

    status)
        echo "Alarms in ALARM state:"
        aws cloudwatch describe-alarms \
            --state-value ALARM \
            --query 'MetricAlarms[].[AlarmName,StateReason]' \
            --output table
        ;;

    delete)
        ALARM_NAME=$1
        aws cloudwatch delete-alarms --alarm-names "$ALARM_NAME"
        echo "✅ Deleted: $ALARM_NAME"
        ;;

    *)
        echo "Unknown command: $COMMAND"
        usage
        exit 1
        ;;
esac
