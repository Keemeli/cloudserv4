import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import config

class DataProcessor:
    def __init__(self):
        self.data_file = 'data/Electric_prices.csv'
        
    def connect_database(self):
        """Connect to MySQL database"""
        try:
            connection = mysql.connector.connect(**config.DB_CONFIG)
            return connection
        except Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def create_table(self):
        """Create electric_prices table if it doesn't exist"""
        connection = self.connect_database()
        if connection:
            try:
                cursor = connection.cursor()
                create_table_query = """
                CREATE TABLE IF NOT EXISTS electric_prices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    price_eur_mwh DECIMAL(10,2) NOT NULL,
                    area VARCHAR(50),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_date (date),
                    INDEX idx_price (price_eur_mwh)
                )
                """
                cursor.execute(create_table_query)
                connection.commit()
                print("✅ Table created successfully")
                return True
            except Error as e:
                print(f"❌ Error creating table: {e}")
                return False
            finally:
                connection.close()
        return False
    
    def load_csv_data(self):
        """Load data from CSV file"""
        try:
            if os.path.exists(self.data_file):
                df = pd.read_csv(self.data_file)
                print(f"✅ Loaded {len(df)} records from CSV")
                return df
            else:
                print(f"❌ CSV file not found: {self.data_file}")
                return None
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return None
    
    def clean_data(self, df):
        """Clean and prepare data"""
        if df is None or df.empty:
            return None
            
        # Clean column names
        df.columns = df.columns.str.strip().str.lower()
        
        # Handle different possible column names
        date_cols = ['date', 'datetime', 'timestamp', 'time']
        price_cols = ['price', 'price_eur_mwh', 'price_eur', 'eur_mwh']
        
        date_col = None
        price_col = None
        
        for col in df.columns:
            if any(d in col.lower() for d in date_cols):
                date_col = col
            if any(p in col.lower() for p in price_cols):
                price_col = col
        
        if not date_col or not price_col:
            print("❌ Required columns (date, price) not found")
            return None
        
        # Standardize column names
        df = df.rename(columns={
            date_col: 'date',
            price_col: 'price_eur_mwh'
        })
        
        # Convert date
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date', 'price_eur_mwh'])
        
        # Convert price to numeric
        df['price_eur_mwh'] = pd.to_numeric(df['price_eur_mwh'], errors='coerce')
        df = df.dropna(subset=['price_eur_mwh'])
        
        # Add area column if not exists
        if 'area' not in df.columns:
            df['area'] = 'Finland'
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['date', 'price_eur_mwh'])
        
        print(f"✅ Cleaned data: {len(df)} records")
        return df
    
    def insert_data_to_db(self, df):
        """Insert data into MySQL database"""
        connection = self.connect_database()
        if connection and df is not None:
            try:
                cursor = connection.cursor()
                
                # Clear existing data
                cursor.execute("DELETE FROM electric_prices")
                
                # Insert new data
                insert_query = """
                INSERT INTO electric_prices (date, price_eur_mwh, area)
                VALUES (%s, %s, %s)
                """
                
                data_tuples = [
                    (row['date'].date(), float(row['price_eur_mwh']), row.get('area', 'Finland'))
                    for _, row in df.iterrows()
                ]
                
                cursor.executemany(insert_query, data_tuples)
                connection.commit()
                
                print(f"✅ Inserted {len(data_tuples)} records into database")
                return True
                
            except Error as e:
                print(f"❌ Error inserting data: {e}")
                return False
            finally:
                connection.close()
        return False
    
    def process_electric_prices(self):
        """Complete data processing pipeline"""
        print("🔄 Starting data processing pipeline...")
        
        # Step 1: Create table
        if not self.create_table():
            return False
        
        # Step 2: Load CSV data
        df = self.load_csv_data()
        if df is None:
            return False
        
        # Step 3: Clean data
        cleaned_df = self.clean_data(df)
        if cleaned_df is None:
            return False
        
        # Step 4: Insert into database
        if not self.insert_data_to_db(cleaned_df):
            return False
        
        print("✅ Data processing pipeline completed successfully!")
        return True
    
    def get_sample_data(self):
        """Generate sample data if CSV not available"""
        print("🔧 Generating sample electric prices data...")
        
        import numpy as np
        from datetime import datetime, timedelta
        
        # Generate 365 days of sample data
        start_date = datetime.now() - timedelta(days=365)
        dates = [start_date + timedelta(days=x) for x in range(365)]
        
        # Generate realistic electric prices (30-150 EUR/MWh with seasonality)
        base_price = 60
        seasonal_variation = [20 * np.sin(2 * np.pi * x / 365) for x in range(365)]
        random_variation = np.random.normal(0, 15, 365)
        prices = [max(10, base_price + seasonal + random) 
                 for seasonal, random in zip(seasonal_variation, random_variation)]
        
        df = pd.DataFrame({
            'date': dates,
            'price_eur_mwh': prices,
            'area': 'Finland'
        })
        
        return df

if __name__ == "__main__":
    processor = DataProcessor()
    
    # If CSV doesn't exist, create sample data
    if not os.path.exists('data/Electric_prices.csv'):
        print("📁 Creating data directory and sample data...")
        os.makedirs('data', exist_ok=True)
        
        sample_df = processor.get_sample_data()
        sample_df.to_csv('data/Electric_prices.csv', index=False)
        print("✅ Sample data created: data/Electric_prices.csv")
    
    # Process the data
    success = processor.process_electric_prices()
    if success:
        print("🎉 Data processing completed successfully!")
    else:
        print("❌ Data processing failed!")
