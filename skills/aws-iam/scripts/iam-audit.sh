#!/bin/bash
# IAM Security Audit Script

echo "🔐 AWS IAM Security Audit"
echo "========================="
echo ""

# Check for root access keys
echo "1. Checking root account access keys..."
ROOT_KEYS=$(aws iam get-account-summary --query 'SummaryMap.AccountAccessKeysPresent' --output text)
if [ "$ROOT_KEYS" -gt 0 ]; then
    echo "   ⚠️  WARNING: Root account has access keys!"
else
    echo "   ✅ No root access keys found"
fi

# Check MFA on root
echo ""
echo "2. Checking root account MFA..."
ROOT_MFA=$(aws iam get-account-summary --query 'SummaryMap.AccountMFAEnabled' --output text)
if [ "$ROOT_MFA" -eq 1 ]; then
    echo "   ✅ Root account MFA is enabled"
else
    echo "   ❌ CRITICAL: Root account MFA is NOT enabled!"
fi

# Check password policy
echo ""
echo "3. Checking password policy..."
aws iam get-account-password-policy 2>/dev/null || echo "   ⚠️  No password policy configured!"

# List users without MFA
echo ""
echo "4. Users without MFA:"
aws iam list-users --query 'Users[].UserName' --output text | tr '\t' '\n' | while read user; do
    MFA=$(aws iam list-mfa-devices --user-name "$user" --query 'MFADevices' --output text)
    if [ -z "$MFA" ]; then
        echo "   ⚠️  $user - No MFA"
    fi
done

# List unused access keys
echo ""
echo "5. Access keys older than 90 days:"
aws iam list-users --query 'Users[].UserName' --output text | tr '\t' '\n' | while read user; do
    aws iam list-access-keys --user-name "$user" --query 'AccessKeyMetadata[?CreateDate<=`'"$(date -v-90d +%Y-%m-%d)"'`].[AccessKeyId,CreateDate]' --output text 2>/dev/null | while read key; do
        if [ -n "$key" ]; then
            echo "   ⚠️  $user: $key"
        fi
    done
done

echo ""
echo "🔍 Audit complete!"
