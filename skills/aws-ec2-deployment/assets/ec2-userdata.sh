#!/bin/bash
# EC2 User Data Script for Application Deployment
yum update -y
yum install -y docker
systemctl start docker
systemctl enable docker
docker pull myapp:latest
docker run -d -p 80:3000 myapp:latest
