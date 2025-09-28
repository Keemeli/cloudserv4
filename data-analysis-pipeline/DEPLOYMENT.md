# CSC VM Deployment Guide
# Electric Prices Data Analysis Pipeline
# Eemeli Karjalainen - eekarjal24@students.oamk.fi

## 🚀 Quick Deployment to CSC VM

### Step 1: Create CSC VM
1. Log into CSC cloud portal (https://pouta.csc.fi/)
2. Create Ubuntu 20.04/22.04 instance
3. Choose flavor with at least 2GB RAM
4. Configure security groups:
   ```
   Port 8501 (TCP) - 0.0.0.0/0 (Streamlit App)
   Port 22 (SSH) - Your IP address
   Port 3306 (MySQL) - Internal only
   ```

### Step 2: Connect to VM
```bash
ssh ubuntu@YOUR_VM_PUBLIC_IP
```

### Step 3: Upload Files
```bash
# Option 1: Clone from GitHub
git clone https://github.com/Keemeli/cloudserv4.git
cd cloudserv4/data-analysis-pipeline

# Option 2: SCP files
scp -r data-analysis-pipeline/ ubuntu@YOUR_VM_IP:~/
```

### Step 4: Run Setup Script
```bash
cd data-analysis-pipeline
sudo ./setup.sh
```

### Step 5: Access Application
```
http://YOUR_VM_PUBLIC_IP:8501
```

## 🔧 Manual Setup (Alternative)

If you prefer manual installation:

### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Dependencies
```bash
sudo apt install -y python3 python3-pip mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 3. Configure MySQL
```bash
sudo mysql -e "CREATE DATABASE electric_data;"
sudo mysql -e "CREATE USER 'eemeli'@'localhost' IDENTIFIED BY 'SecurePassword123!';"
sudo mysql -e "GRANT ALL PRIVILEGES ON electric_data.* TO 'eemeli'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

### 4. Install Python Packages
```bash
pip3 install -r requirements.txt
```

### 5. Initialize Database
```bash
python3 data_processor.py
```

### 6. Start Streamlit
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## 🔍 Troubleshooting

### Service Not Starting
```bash
# Check service status
systemctl status streamlit-electric-prices

# View logs
journalctl -u streamlit-electric-prices -f

# Restart service
sudo systemctl restart streamlit-electric-prices
```

### Database Issues
```bash
# Check MySQL status
sudo systemctl status mysql

# Connect to MySQL
mysql -u eemeli -p electric_data

# Check tables
SHOW TABLES;
SELECT COUNT(*) FROM electric_prices;
```

### Port Access Issues
1. Ensure CSC security group allows port 8501
2. Check if service is running: `sudo netstat -tulnp | grep 8501`
3. Test locally: `curl http://localhost:8501`

## 📊 Application Features

### Data Sources
- **Primary**: Upload your own Electric_prices.csv
- **Fallback**: Auto-generated sample data
- **Format**: CSV with columns: date, price_eur_mwh, area

### Dashboard Sections
1. **Time Series Analysis**: Price trends over time
2. **Statistical Analysis**: Descriptive statistics and distributions
3. **Database Information**: MySQL connection and data stats
4. **Data Processing**: Pipeline controls and data quality metrics

### API Endpoints (via Streamlit)
- Main dashboard: `http://YOUR_VM_IP:8501`
- No REST API (Streamlit web interface only)

## 🎯 Assignment Submission

**Application URL**: http://YOUR_VM_PUBLIC_IP:8501
**Repository**: https://github.com/Keemeli/cloudserv4
**Student**: Eemeli Karjalainen (eekarjal24@students.oamk.fi)
**University**: OAMK - Oulu University of Applied Sciences

## 📋 Checklist

- [ ] CSC VM created with Ubuntu 20.04/22.04
- [ ] Security group allows port 8501 from 0.0.0.0/0
- [ ] MySQL database installed and configured
- [ ] Python dependencies installed
- [ ] Electric_prices.csv uploaded or sample data generated
- [ ] Streamlit service running
- [ ] Application accessible from public IP
- [ ] Database contains electric prices data
- [ ] Dashboard shows interactive charts and analysis

## 🔧 Service Management

```bash
# Start service
sudo systemctl start streamlit-electric-prices

# Stop service
sudo systemctl stop streamlit-electric-prices

# Restart service
sudo systemctl restart streamlit-electric-prices

# Enable auto-start on boot
sudo systemctl enable streamlit-electric-prices

# Check logs
journalctl -u streamlit-electric-prices -f
```
