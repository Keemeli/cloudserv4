# Configuration file for MySQL database and application settings
# Eemeli Karjalainen - CSC VM Data Analysis Pipeline

import os

# MySQL Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'electric_data'),
    'user': os.getenv('DB_USER', 'eemeli'),
    'password': os.getenv('DB_PASSWORD', 'SecurePassword123!'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'charset': 'utf8mb4',
    'autocommit': True
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    'host': '0.0.0.0',
    'port': 8501,
    'title': 'Electric Prices Analysis - Eemeli Karjalainen'
}

# Data Configuration
DATA_CONFIG = {
    'csv_file': 'data/Electric_prices.csv',
    'table_name': 'electric_prices',
    'date_column': 'date',
    'price_column': 'price_eur_mwh'
}

# Application Information
APP_INFO = {
    'author': 'Eemeli Karjalainen',
    'email': 'eekarjal24@students.oamk.fi',
    'university': 'OAMK - Oulu University of Applied Sciences',
    'course': 'Cloud Services',
    'assignment': 'CSC VM Data Analysis Pipeline'
}
