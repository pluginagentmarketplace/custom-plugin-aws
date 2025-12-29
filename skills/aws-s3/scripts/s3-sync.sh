#!/bin/bash
# S3 Sync Script with common patterns

set -e

echo "📦 S3 Sync Utility"
echo "=================="

usage() {
    echo "Usage: $0 <command> <source> <destination>"
    echo ""
    echo "Commands:"
    echo "  upload    - Upload local directory to S3"
    echo "  download  - Download S3 prefix to local"
    echo "  backup    - Backup with timestamp"
    echo "  website   - Deploy static website"
    echo ""
    echo "Examples:"
    echo "  $0 upload ./dist s3://my-bucket/app/"
    echo "  $0 download s3://my-bucket/data/ ./local-data/"
    echo "  $0 backup ./important s3://my-bucket/backups/"
    echo "  $0 website ./build s3://my-website-bucket"
}

if [ $# -lt 3 ]; then
    usage
    exit 1
fi

COMMAND=$1
SOURCE=$2
DEST=$3

case $COMMAND in
    upload)
        echo "📤 Uploading $SOURCE to $DEST..."
        aws s3 sync "$SOURCE" "$DEST" \
            --delete \
            --exclude ".git/*" \
            --exclude ".DS_Store" \
            --exclude "*.log"
        echo "✅ Upload complete!"
        ;;

    download)
        echo "📥 Downloading $SOURCE to $DEST..."
        aws s3 sync "$SOURCE" "$DEST"
        echo "✅ Download complete!"
        ;;

    backup)
        TIMESTAMP=$(date +%Y%m%d-%H%M%S)
        BACKUP_PATH="${DEST}${TIMESTAMP}/"
        echo "💾 Creating backup at $BACKUP_PATH..."
        aws s3 sync "$SOURCE" "$BACKUP_PATH" \
            --exclude ".git/*"
        echo "✅ Backup created: $BACKUP_PATH"
        ;;

    website)
        echo "🌐 Deploying static website..."

        # Sync with proper content types
        aws s3 sync "$SOURCE" "$DEST" \
            --delete \
            --cache-control "max-age=31536000" \
            --exclude "*.html"

        # HTML files with shorter cache
        aws s3 sync "$SOURCE" "$DEST" \
            --cache-control "max-age=3600" \
            --exclude "*" \
            --include "*.html"

        # Invalidate CloudFront if distribution ID provided
        if [ -n "$CLOUDFRONT_DIST_ID" ]; then
            echo "🔄 Invalidating CloudFront cache..."
            aws cloudfront create-invalidation \
                --distribution-id "$CLOUDFRONT_DIST_ID" \
                --paths "/*"
        fi

        echo "✅ Website deployed!"
        ;;

    *)
        echo "Unknown command: $COMMAND"
        usage
        exit 1
        ;;
esac
