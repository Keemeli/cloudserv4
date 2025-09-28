#!/bin/bash

# CSC VM Setup Script for Data Analysis Pipeline
# Eemeli Karjalainen - eekarjal24@students.oamk.fi
# OAMK - Cloud Services Assignment

set -e

echo "🚀 Starting CSC VM setup for Electric Prices Data Analysis Pipeline"
echo "========================================================================="
echo "Author: Eemeli Karjalainen (eekarjal24@students.oamk.fi)"
echo "University: OAMK - Oulu University of Applied Sciences"
echo "========================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   print_error "This script must be run as root (use sudo)"
   exit 1
fi

# Update system
print_info "Updating system packages..."
apt update && apt upgrade -y
print_status "System updated successfully"

# Install Python 3 and pip
print_info "Installing Python 3 and pip..."
apt install -y python3 python3-pip python3-venv
print_status "Python 3 and pip installed"

# Install MySQL Server
print_info "Installing MySQL Server..."
export DEBIAN_FRONTEND=noninteractive
apt install -y mysql-server

# Start and enable MySQL
systemctl start mysql
systemctl enable mysql
print_status "MySQL Server installed and started"

# Secure MySQL installation
print_info "Configuring MySQL..."
mysql -e "CREATE DATABASE IF NOT EXISTS electric_data;"
mysql -e "CREATE USER IF NOT EXISTS 'eemeli'@'localhost' IDENTIFIED BY 'SecurePassword123!';"
mysql -e "GRANT ALL PRIVILEGES ON electric_data.* TO 'eemeli'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"
print_status "MySQL configured successfully"

# Install system dependencies
print_info "Installing system dependencies..."
apt install -y build-essential pkg-config default-libmysqlclient-dev
print_status "System dependencies installed"

# Create application user
print_info "Creating application user..."
if ! id "eemeli" &>/dev/null; then
    useradd -m -s /bin/bash eemeli
    print_status "User 'eemeli' created"
else
    print_info "User 'eemeli' already exists"
fi

# Set up application directory
APP_DIR="/home/eemeli/data-analysis-pipeline"
print_info "Setting up application directory: $APP_DIR"

# Create directory structure
mkdir -p $APP_DIR/data
mkdir -p $APP_DIR/sql
mkdir -p $APP_DIR/logs

# Copy application files (assuming they're in current directory)
if [ -f "app.py" ]; then
    cp app.py $APP_DIR/
    cp data_processor.py $APP_DIR/
    cp config.py $APP_DIR/
    cp requirements.txt $APP_DIR/
    print_status "Application files copied"
else
    print_warning "Application files not found in current directory"
    print_info "You'll need to upload app.py, data_processor.py, config.py, and requirements.txt"
fi

# Set ownership
chown -R eemeli:eemeli $APP_DIR
print_status "Directory ownership set"

# Install Python dependencies as the application user
print_info "Installing Python dependencies..."
sudo -u eemeli python3 -m pip install --user -r $APP_DIR/requirements.txt
print_status "Python dependencies installed"

# Create systemd service for Streamlit
print_info "Creating Streamlit service..."
cat > /etc/systemd/system/streamlit-electric-prices.service << EOF
[Unit]
Description=Streamlit Electric Prices Analysis - Eemeli Karjalainen
After=network.target mysql.service

[Service]
Type=exec
User=eemeli
Group=eemeli
WorkingDirectory=$APP_DIR
Environment=PATH=/home/eemeli/.local/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/home/eemeli/.local/bin/streamlit run app.py --server.address 0.0.0.0 --server.port 8501
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable streamlit-electric-prices.service
print_status "Streamlit service created and enabled"

# Configure firewall
print_info "Configuring firewall..."
ufw allow 8501/tcp
ufw allow 22/tcp
ufw --force enable
print_status "Firewall configured (port 8501 open for Streamlit)"

# Initialize database with sample data
print_info "Initializing database with sample data..."
sudo -u eemeli bash -c "cd $APP_DIR && python3 data_processor.py"
print_status "Database initialized"

# Start Streamlit service
print_info "Starting Streamlit service..."
systemctl start streamlit-electric-prices.service
sleep 5

# Check service status
if systemctl is-active --quiet streamlit-electric-prices.service; then
    print_status "Streamlit service is running"
else
    print_warning "Streamlit service may have issues"
    systemctl status streamlit-electric-prices.service
fi

# Get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com/ || curl -s http://ipecho.net/plain || echo "Unable to determine")

echo ""
echo "🎉 Setup completed successfully!"
echo "========================================================================="
echo -e "${GREEN}✅ Your Electric Prices Analysis Dashboard is ready!${NC}"
echo ""
echo -e "${BLUE}📱 Application URL: http://$PUBLIC_IP:8501${NC}"
echo -e "${BLUE}📊 Database: MySQL (electric_data)${NC}"
echo -e "${BLUE}🔧 Service: streamlit-electric-prices${NC}"
echo ""
echo -e "${YELLOW}📋 Important Notes:${NC}"
echo "1. Make sure CSC VM security group allows inbound traffic on port 8501"
echo "2. The application automatically generates sample data if Electric_prices.csv is not found"
echo "3. Upload your own Electric_prices.csv to /home/eemeli/data-analysis-pipeline/data/"
echo ""
echo -e "${BLUE}🔧 Service Commands:${NC}"
echo "• Check status: systemctl status streamlit-electric-prices"
echo "• Restart: systemctl restart streamlit-electric-prices"
echo "• View logs: journalctl -u streamlit-electric-prices -f"
echo ""
echo -e "${GREEN}👨‍💻 Created by: Eemeli Karjalainen (eekarjal24@students.oamk.fi)${NC}"
echo -e "${GREEN}🎓 OAMK - Oulu University of Applied Sciences${NC}"
echo "========================================================================="
