#!/bin/bash
# AWS Security Audit Script

echo "🔐 AWS Security Audit"
echo "====================="
echo ""

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "Account: $ACCOUNT_ID"
echo ""

# 1. Root Account Checks
echo "1️⃣  Root Account Checks"
echo "------------------------"

ROOT_MFA=$(aws iam get-account-summary --query 'SummaryMap.AccountMFAEnabled' --output text)
if [ "$ROOT_MFA" -eq 1 ]; then
    echo "✅ Root MFA: Enabled"
else
    echo "❌ Root MFA: NOT ENABLED - CRITICAL!"
fi

ROOT_KEYS=$(aws iam get-account-summary --query 'SummaryMap.AccountAccessKeysPresent' --output text)
if [ "$ROOT_KEYS" -eq 0 ]; then
    echo "✅ Root Access Keys: None"
else
    echo "❌ Root Access Keys: PRESENT - CRITICAL!"
fi

# 2. IAM Checks
echo ""
echo "2️⃣  IAM Checks"
echo "---------------"

USERS_WITHOUT_MFA=$(aws iam list-users --query 'Users[].UserName' --output text | tr '\t' '\n' | while read user; do
    MFA=$(aws iam list-mfa-devices --user-name "$user" --query 'MFADevices' --output text 2>/dev/null)
    if [ -z "$MFA" ]; then
        echo "$user"
    fi
done)

if [ -z "$USERS_WITHOUT_MFA" ]; then
    echo "✅ All users have MFA"
else
    echo "⚠️  Users without MFA:"
    echo "$USERS_WITHOUT_MFA" | while read user; do
        echo "   - $user"
    done
fi

# 3. CloudTrail
echo ""
echo "3️⃣  CloudTrail"
echo "---------------"

TRAILS=$(aws cloudtrail describe-trails --query 'trailList[].Name' --output text)
if [ -n "$TRAILS" ]; then
    echo "✅ CloudTrail trails:"
    echo "$TRAILS" | tr '\t' '\n' | while read trail; do
        echo "   - $trail"
    done
else
    echo "❌ No CloudTrail trails configured!"
fi

# 4. S3 Public Access
echo ""
echo "4️⃣  S3 Public Access"
echo "--------------------"

PUBLIC_BUCKETS=$(aws s3api list-buckets --query 'Buckets[].Name' --output text | tr '\t' '\n' | while read bucket; do
    BLOCK=$(aws s3api get-public-access-block --bucket "$bucket" 2>/dev/null | jq -r '.PublicAccessBlockConfiguration.BlockPublicAcls')
    if [ "$BLOCK" != "true" ]; then
        echo "$bucket"
    fi
done 2>/dev/null)

if [ -z "$PUBLIC_BUCKETS" ]; then
    echo "✅ All buckets have public access blocked"
else
    echo "⚠️  Buckets without public access block:"
    echo "$PUBLIC_BUCKETS" | while read bucket; do
        echo "   - $bucket"
    done
fi

# 5. Security Groups
echo ""
echo "5️⃣  Security Groups"
echo "-------------------"

OPEN_SG=$(aws ec2 describe-security-groups \
    --query "SecurityGroups[?IpPermissions[?IpRanges[?CidrIp=='0.0.0.0/0']]].GroupId" \
    --output text)

if [ -n "$OPEN_SG" ]; then
    echo "⚠️  Security groups with 0.0.0.0/0 access:"
    echo "$OPEN_SG" | tr '\t' '\n' | while read sg; do
        echo "   - $sg"
    done
else
    echo "✅ No overly permissive security groups"
fi

# 6. GuardDuty
echo ""
echo "6️⃣  GuardDuty"
echo "--------------"

GD_STATUS=$(aws guardduty list-detectors --query 'DetectorIds[0]' --output text 2>/dev/null)
if [ -n "$GD_STATUS" ] && [ "$GD_STATUS" != "None" ]; then
    echo "✅ GuardDuty: Enabled"
    FINDINGS=$(aws guardduty list-findings --detector-id "$GD_STATUS" --query 'FindingIds | length(@)' --output text)
    echo "   Findings: $FINDINGS"
else
    echo "❌ GuardDuty: NOT ENABLED"
fi

# Summary
echo ""
echo "📊 Audit Complete"
echo "================="
echo "Review any ⚠️ or ❌ items above and take corrective action."
