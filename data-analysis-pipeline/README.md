# Data Analysis Pipeline - Eemeli Karjalainen
# CSC VM Deployment with MySQL and Streamlit

A comprehensive data analysis pipeline deployed on CSC VM featuring:
- **Streamlit Dashboard**: Interactive web interface for data visualization
- **MySQL Database**: Data storage and management
- **Finnish Open Data**: Electric prices analysis from opendata.fi
- **Real-time Analytics**: Dynamic charts and statistics

## 🎯 Assignment Features

- ✅ **Data Pipeline**: Automated data ingestion and processing
- ✅ **MySQL Integration**: Database storage for processed data
- ✅ **Streamlit Web App**: Interactive dashboard accessible via web
- ✅ **Finnish Open Data**: Using real electric prices data
- ✅ **CSC VM Deployment**: Hosted on CSC cloud infrastructure
- ✅ **Security Groups**: Properly exposed ports for public access

## 📊 Data Source

Using Finnish electric prices data from opendata.fi:
- **Dataset**: Electric_prices.csv
- **Source**: https://www.opendata.fi/en
- **Content**: Historical electricity pricing data for Finland
- **Analysis**: Price trends, statistical summaries, forecasting

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Ingestion │───▶│  MySQL Database │───▶│ Streamlit App   │
│   (CSV Processing)│    │  (Data Storage) │    │ (Web Interface) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────▼───────────────────────┘
                    CSC VM (Ubuntu 20.04/22.04)
                    Public IP: [To be assigned]
                    Port 8501: Streamlit App
```

## 📁 Project Structure

```
data-analysis-pipeline/
├── app.py                 # Main Streamlit application
├── data_processor.py      # Data processing and MySQL integration
├── requirements.txt       # Python dependencies
├── setup.sh              # CSC VM setup script
├── config.py             # Configuration settings
├── data/                 # Data directory
│   └── Electric_prices.csv
├── sql/                  # SQL scripts
│   └── init_database.sql
└── README.md             # This file
```

## 🚀 Deployment Instructions

### 1. CSC VM Setup

1. **Create CSC VM**:
   - Log into CSC cloud portal
   - Create Ubuntu 20.04/22.04 instance
   - Configure security groups to allow port 8501

2. **Security Group Rules**:
   ```
   Port 8501 (TCP) - 0.0.0.0/0 (Streamlit App)
   Port 22 (SSH) - Your IP
   Port 3306 (MySQL) - Internal only
   ```

### 2. Installation

```bash
# SSH to your CSC VM
ssh ubuntu@YOUR_VM_IP

# Clone repository
git clone https://github.com/Keemeli/cloudserv4.git
cd cloudserv4/data-analysis-pipeline

# Run setup script
chmod +x setup.sh
sudo ./setup.sh

# Start the application
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### 3. Access Application

- **Web Interface**: http://YOUR_VM_IP:8501
- **Data Dashboard**: Interactive charts and analysis
- **Database Admin**: MySQL data exploration

## 📊 Features

### Data Analysis
- **Price Trends**: Historical electricity price analysis
- **Statistical Summary**: Mean, median, standard deviation
- **Time Series**: Price changes over time
- **Forecasting**: Simple trend predictions

### Interactive Dashboard
- **Real-time Charts**: Dynamic price visualizations
- **Filter Options**: Date range and price filters  
- **Export Data**: Download processed results
- **Database Stats**: MySQL table information

## 🔧 Technical Stack

- **Frontend**: Streamlit (Python web framework)
- **Database**: MySQL 8.0
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **Deployment**: CSC VM (Ubuntu)
- **Data Source**: Finnish Open Data Portal

## 👨‍💻 Author

**Eemeli Karjalainen**  
Student ID: eekarjal24@students.oamk.fi  
OAMK - Oulu University of Applied Sciences  
Cloud Services Course Assignment

## 📄 License

Educational project for CSC VM and data analysis demonstration.
