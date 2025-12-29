#!/usr/bin/env python3
"""
AWS Resource Health Checker
Monitors AWS resources and reports their status.
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any


class AWSResourceChecker:
    """Check health status of common AWS resources."""

    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.session = boto3.Session(region_name=region)

    def check_ec2_instances(self) -> List[Dict[str, Any]]:
        """Check EC2 instance status."""
        ec2 = self.session.client('ec2')
        response = ec2.describe_instances()

        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'id': instance['InstanceId'],
                    'type': instance['InstanceType'],
                    'state': instance['State']['Name'],
                    'launch_time': instance.get('LaunchTime', '').isoformat() if instance.get('LaunchTime') else None,
                    'public_ip': instance.get('PublicIpAddress'),
                    'private_ip': instance.get('PrivateIpAddress'),
                    'tags': {t['Key']: t['Value'] for t in instance.get('Tags', [])}
                })
        return instances

    def check_rds_instances(self) -> List[Dict[str, Any]]:
        """Check RDS database status."""
        rds = self.session.client('rds')
        response = rds.describe_db_instances()

        databases = []
        for db in response['DBInstances']:
            databases.append({
                'id': db['DBInstanceIdentifier'],
                'engine': f"{db['Engine']} {db['EngineVersion']}",
                'status': db['DBInstanceStatus'],
                'class': db['DBInstanceClass'],
                'storage_gb': db['AllocatedStorage'],
                'multi_az': db['MultiAZ'],
                'endpoint': db.get('Endpoint', {}).get('Address')
            })
        return databases

    def check_s3_buckets(self) -> List[Dict[str, Any]]:
        """Check S3 bucket information."""
        s3 = self.session.client('s3')
        response = s3.list_buckets()

        buckets = []
        for bucket in response['Buckets']:
            try:
                location = s3.get_bucket_location(Bucket=bucket['Name'])
                versioning = s3.get_bucket_versioning(Bucket=bucket['Name'])
                encryption = s3.get_bucket_encryption(Bucket=bucket['Name'])
                encrypted = True
            except Exception:
                encrypted = False
                versioning = {}

            buckets.append({
                'name': bucket['Name'],
                'created': bucket['CreationDate'].isoformat(),
                'region': location.get('LocationConstraint', 'us-east-1'),
                'versioning': versioning.get('Status', 'Disabled'),
                'encrypted': encrypted
            })
        return buckets

    def check_lambda_functions(self) -> List[Dict[str, Any]]:
        """Check Lambda function status."""
        lambda_client = self.session.client('lambda')
        response = lambda_client.list_functions()

        functions = []
        for func in response['Functions']:
            functions.append({
                'name': func['FunctionName'],
                'runtime': func['Runtime'],
                'memory_mb': func['MemorySize'],
                'timeout_sec': func['Timeout'],
                'code_size_mb': round(func['CodeSize'] / (1024 * 1024), 2),
                'last_modified': func['LastModified']
            })
        return functions

    def check_cloudwatch_alarms(self) -> List[Dict[str, Any]]:
        """Check CloudWatch alarm status."""
        cloudwatch = self.session.client('cloudwatch')
        response = cloudwatch.describe_alarms()

        alarms = []
        for alarm in response['MetricAlarms']:
            alarms.append({
                'name': alarm['AlarmName'],
                'state': alarm['StateValue'],
                'metric': alarm['MetricName'],
                'threshold': alarm['Threshold'],
                'comparison': alarm['ComparisonOperator'],
                'actions_enabled': alarm['ActionsEnabled']
            })
        return alarms

    def get_cost_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get cost summary for the last N days."""
        ce = self.session.client('ce')

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        response = ce.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )

        costs = {}
        for result in response['ResultsByTime']:
            for group in result['Groups']:
                service = group['Keys'][0]
                amount = float(group['Metrics']['UnblendedCost']['Amount'])
                costs[service] = costs.get(service, 0) + amount

        return {
            'period': f"{start_date} to {end_date}",
            'total': sum(costs.values()),
            'by_service': dict(sorted(costs.items(), key=lambda x: x[1], reverse=True)[:10])
        }

    def full_health_check(self) -> Dict[str, Any]:
        """Run complete health check on all resources."""
        results = {
            'timestamp': datetime.now().isoformat(),
            'region': self.region,
            'resources': {}
        }

        checks = {
            'ec2': self.check_ec2_instances,
            'rds': self.check_rds_instances,
            's3': self.check_s3_buckets,
            'lambda': self.check_lambda_functions,
            'cloudwatch_alarms': self.check_cloudwatch_alarms
        }

        for resource, check_func in checks.items():
            try:
                results['resources'][resource] = {
                    'status': 'success',
                    'data': check_func()
                }
            except Exception as e:
                results['resources'][resource] = {
                    'status': 'error',
                    'error': str(e)
                }

        return results


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='AWS Resource Health Checker')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--resource', choices=['ec2', 'rds', 's3', 'lambda', 'alarms', 'costs', 'all'],
                        default='all', help='Resource type to check')
    parser.add_argument('--output', choices=['json', 'table'], default='json', help='Output format')
    args = parser.parse_args()

    checker = AWSResourceChecker(region=args.region)

    if args.resource == 'all':
        result = checker.full_health_check()
    elif args.resource == 'ec2':
        result = checker.check_ec2_instances()
    elif args.resource == 'rds':
        result = checker.check_rds_instances()
    elif args.resource == 's3':
        result = checker.check_s3_buckets()
    elif args.resource == 'lambda':
        result = checker.check_lambda_functions()
    elif args.resource == 'alarms':
        result = checker.check_cloudwatch_alarms()
    elif args.resource == 'costs':
        result = checker.get_cost_summary()

    print(json.dumps(result, indent=2, default=str))


if __name__ == '__main__':
    main()
