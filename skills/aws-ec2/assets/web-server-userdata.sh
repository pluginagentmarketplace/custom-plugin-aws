#!/bin/bash
# EC2 User Data - Web Server Setup
# Amazon Linux 2023 / AL2

set -e

# Update system
yum update -y

# Install web server
yum install -y httpd

# Start and enable Apache
systemctl start httpd
systemctl enable httpd

# Configure firewall
# (Security group should already allow HTTP/HTTPS)

# Create sample page
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Welcome to EC2</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { color: #232f3e; }
    </style>
</head>
<body>
    <h1>Hello from AWS EC2!</h1>
    <p>Instance ID: $(curl -s http://169.254.169.254/latest/meta-data/instance-id)</p>
    <p>Availability Zone: $(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)</p>
</body>
</html>
EOF

# Install CloudWatch agent (optional)
# yum install -y amazon-cloudwatch-agent

echo "Web server setup complete!"
