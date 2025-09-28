-- Database initialization script for Electric Prices Analysis
-- Eemeli Karjalainen - eekarjal24@students.oamk.fi
-- OAMK - Cloud Services Assignment

-- Create database
CREATE DATABASE IF NOT EXISTS electric_data 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE electric_data;

-- Create electric_prices table
CREATE TABLE IF NOT EXISTS electric_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    price_eur_mwh DECIMAL(10,2) NOT NULL,
    area VARCHAR(50) DEFAULT 'Finland',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for performance
    INDEX idx_date (date),
    INDEX idx_price (price_eur_mwh),
    INDEX idx_area (area),
    
    -- Constraints
    UNIQUE KEY unique_date_area (date, area),
    CHECK (price_eur_mwh >= 0)
) ENGINE=InnoDB;

-- Create user for application
CREATE USER IF NOT EXISTS 'eemeli'@'localhost' IDENTIFIED BY 'SecurePassword123!';
GRANT SELECT, INSERT, UPDATE, DELETE ON electric_data.* TO 'eemeli'@'localhost';
FLUSH PRIVILEGES;

-- Create a view for easy data access
CREATE OR REPLACE VIEW price_summary AS
SELECT 
    DATE_FORMAT(date, '%Y-%m') as month,
    COUNT(*) as records,
    AVG(price_eur_mwh) as avg_price,
    MIN(price_eur_mwh) as min_price,
    MAX(price_eur_mwh) as max_price,
    STDDEV(price_eur_mwh) as std_price
FROM electric_prices 
GROUP BY DATE_FORMAT(date, '%Y-%m')
ORDER BY month DESC;

-- Insert sample data if table is empty
INSERT IGNORE INTO electric_prices (date, price_eur_mwh, area) VALUES
('2024-01-01', 65.50, 'Finland'),
('2024-01-02', 72.30, 'Finland'),
('2024-01-03', 58.90, 'Finland'),
('2024-01-04', 81.20, 'Finland'),
('2024-01-05', 69.75, 'Finland'),
('2024-01-06', 55.40, 'Finland'),
('2024-01-07', 62.10, 'Finland'),
('2024-01-08', 78.65, 'Finland'),
('2024-01-09', 71.25, 'Finland'),
('2024-01-10', 66.80, 'Finland');

-- Show table structure
DESCRIBE electric_prices;

-- Show sample data
SELECT 'Sample data from electric_prices table:' as info;
SELECT * FROM electric_prices LIMIT 10;
