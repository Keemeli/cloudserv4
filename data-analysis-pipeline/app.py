import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import numpy as np
from data_processor import DataProcessor
import config

# Configure Streamlit page
st.set_page_config(
    page_title="Electric Prices Analysis - Eemeli Karjalainen",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .author-info {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

class ElectricPriceAnalyzer:
    def __init__(self):
        self.data_processor = DataProcessor()
        
    def load_data(self):
        """Load data from MySQL database"""
        try:
            connection = mysql.connector.connect(**config.DB_CONFIG)
            if connection.is_connected():
                query = """
                SELECT date, price_eur_mwh, area, timestamp 
                FROM electric_prices 
                ORDER BY date DESC
                """
                df = pd.read_sql(query, connection)
                connection.close()
                return df
        except Error as e:
            st.error(f"Database connection error: {e}")
            # Fallback to CSV if database not available
            return self.load_csv_fallback()
        
    def load_csv_fallback(self):
        """Fallback to load CSV if database not available"""
        try:
            df = pd.read_csv('data/Electric_prices.csv')
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def get_database_stats(self):
        """Get database statistics"""
        try:
            connection = mysql.connector.connect(**config.DB_CONFIG)
            if connection.is_connected():
                cursor = connection.cursor()
                
                # Get table info
                cursor.execute("SELECT COUNT(*) FROM electric_prices")
                total_records = cursor.fetchone()[0]
                
                cursor.execute("SELECT MIN(date), MAX(date) FROM electric_prices")
                date_range = cursor.fetchone()
                
                cursor.execute("SELECT AVG(price_eur_mwh) FROM electric_prices")
                avg_price = cursor.fetchone()[0]
                
                connection.close()
                
                return {
                    'total_records': total_records,
                    'date_range': date_range,
                    'avg_price': avg_price
                }
        except Error:
            return None

def main():
    # Header
    st.markdown('<h1 class="main-header">⚡ Finnish Electric Prices Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">CSC VM Data Pipeline by Eemeli Karjalainen</p>', unsafe_allow_html=True)
    
    # Initialize analyzer
    analyzer = ElectricPriceAnalyzer()
    
    # Sidebar
    st.sidebar.title("📊 Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Load data
    with st.spinner("Loading data from MySQL database..."):
        df = analyzer.load_data()
    
    if df.empty:
        st.error("No data available. Please check database connection or upload Electric_prices.csv file.")
        return
    
    # Data preprocessing
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        df = df.sort_values('date')
    
    # Sidebar filters
    st.sidebar.subheader("🔍 Data Filters")
    
    if not df.empty and 'date' in df.columns:
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
    
    # Price range filter
    if 'price_eur_mwh' in df.columns:
        price_min = float(df['price_eur_mwh'].min())
        price_max = float(df['price_eur_mwh'].max())
        
        price_range = st.sidebar.slider(
            "Price Range (EUR/MWh)",
            min_value=price_min,
            max_value=price_max,
            value=(price_min, price_max),
            step=0.1
        )
        
        df = df[(df['price_eur_mwh'] >= price_range[0]) & (df['price_eur_mwh'] <= price_range[1])]
    
    # Main dashboard
    if not df.empty:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_price = df['price_eur_mwh'].mean()
            st.metric("Average Price", f"{avg_price:.2f} EUR/MWh")
        
        with col2:
            max_price = df['price_eur_mwh'].max()
            st.metric("Max Price", f"{max_price:.2f} EUR/MWh")
        
        with col3:
            min_price = df['price_eur_mwh'].min()
            st.metric("Min Price", f"{min_price:.2f} EUR/MWh")
        
        with col4:
            total_records = len(df)
            st.metric("Data Points", f"{total_records:,}")
        
        st.markdown("---")
        
        # Charts
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Time Series", "📊 Statistics", "💾 Database Info", "🔧 Data Processing"])
        
        with tab1:
            st.subheader("Electric Prices Over Time")
            
            if 'date' in df.columns and 'price_eur_mwh' in df.columns:
                fig = px.line(
                    df, 
                    x='date', 
                    y='price_eur_mwh',
                    title="Electric Prices Trend",
                    labels={'date': 'Date', 'price_eur_mwh': 'Price (EUR/MWh)'}
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Price distribution
                st.subheader("Price Distribution")
                fig_hist = px.histogram(
                    df, 
                    x='price_eur_mwh', 
                    nbins=50,
                    title="Price Distribution",
                    labels={'price_eur_mwh': 'Price (EUR/MWh)', 'count': 'Frequency'}
                )
                st.plotly_chart(fig_hist, use_container_width=True)
        
        with tab2:
            st.subheader("Statistical Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Descriptive Statistics")
                stats = df['price_eur_mwh'].describe()
                stats_df = pd.DataFrame({
                    'Statistic': ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max'],
                    'Value': [
                        f"{stats['count']:.0f}",
                        f"{stats['mean']:.2f}",
                        f"{stats['std']:.2f}",
                        f"{stats['min']:.2f}",
                        f"{stats['25%']:.2f}",
                        f"{stats['50%']:.2f}",
                        f"{stats['75%']:.2f}",
                        f"{stats['max']:.2f}"
                    ]
                })
                st.dataframe(stats_df, use_container_width=True)
            
            with col2:
                st.markdown("### 📈 Box Plot")
                fig_box = px.box(
                    df, 
                    y='price_eur_mwh',
                    title="Price Distribution Box Plot"
                )
                st.plotly_chart(fig_box, use_container_width=True)
                
                # Monthly analysis if date available
                if 'date' in df.columns:
                    df['month'] = df['date'].dt.strftime('%Y-%m')
                    monthly_avg = df.groupby('month')['price_eur_mwh'].mean().reset_index()
                    
                    fig_monthly = px.bar(
                        monthly_avg.tail(12), 
                        x='month', 
                        y='price_eur_mwh',
                        title="Monthly Average Prices (Last 12 Months)"
                    )
                    st.plotly_chart(fig_monthly, use_container_width=True)
        
        with tab3:
            st.subheader("Database Information")
            
            # Database stats
            db_stats = analyzer.get_database_stats()
            
            if db_stats:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 💾 MySQL Database Stats")
                    st.info(f"**Total Records:** {db_stats['total_records']:,}")
                    st.info(f"**Date Range:** {db_stats['date_range'][0]} to {db_stats['date_range'][1]}")
                    st.info(f"**Average Price:** {db_stats['avg_price']:.2f} EUR/MWh")
                
                with col2:
                    st.markdown("### 🔧 Connection Info")
                    st.success("✅ MySQL Connection: Active")
                    st.info(f"**Database:** {config.DB_CONFIG['database']}")
                    st.info(f"**Host:** {config.DB_CONFIG['host']}")
                    st.info(f"**Table:** electric_prices")
            else:
                st.warning("Database connection not available. Using CSV fallback.")
            
            # Raw data sample
            st.markdown("### 📋 Data Sample")
            st.dataframe(df.head(100), use_container_width=True)
        
        with tab4:
            st.subheader("Data Processing Pipeline")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🔄 Data Pipeline Status")
                if st.button("🔄 Refresh Data from Source"):
                    with st.spinner("Processing data..."):
                        success = analyzer.data_processor.process_electric_prices()
                        if success:
                            st.success("✅ Data refreshed successfully!")
                            st.experimental_rerun()
                        else:
                            st.error("❌ Data refresh failed.")
                
                st.markdown("### 📊 Pipeline Info")
                st.info("**Source:** Electric_prices.csv")
                st.info("**Processing:** Pandas + MySQL")
                st.info("**Visualization:** Plotly + Streamlit")
            
            with col2:
                st.markdown("### 📈 Data Quality")
                
                # Data quality metrics
                total_rows = len(df)
                missing_values = df.isnull().sum().sum()
                quality_score = ((total_rows * len(df.columns) - missing_values) / (total_rows * len(df.columns))) * 100
                
                st.metric("Data Quality Score", f"{quality_score:.1f}%")
                st.metric("Missing Values", f"{missing_values}")
                st.metric("Complete Records", f"{total_rows - missing_values}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="author-info">
        <h4>👨‍💻 Created by Eemeli Karjalainen</h4>
        <p>
            📧 <strong>Email:</strong> eekarjal24@students.oamk.fi<br>
            🎓 <strong>University:</strong> OAMK - Oulu University of Applied Sciences<br>
            📚 <strong>Course:</strong> Cloud Services<br>
            🌐 <strong>Deployment:</strong> CSC VM with MySQL + Streamlit<br>
            📊 <strong>Data Source:</strong> Finnish Open Data (opendata.fi)
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
