import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples
n_samples = 1000

# Generate sample data
data = {
    'date_listed': pd.date_range(end=datetime.now(), periods=n_samples).tolist(),
    'list_price': np.random.uniform(200000, 2000000, n_samples),
    'bedrooms': np.random.randint(1, 7, n_samples),
    'bathrooms': np.random.randint(1, 5, n_samples),
    'sqft': np.random.uniform(800, 5000, n_samples),
    'price_per_sqft': None,  # Will calculate this
    'year_built': np.random.randint(1950, 2024, n_samples),
    'property_type': np.random.choice(['Single Family', 'Condo', 'Townhouse', 'Multi-Family'], n_samples),
    'location': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Miami', 'San Francisco'], n_samples),
    'hoa_fee': np.random.choice([0] * 7 + list(np.random.uniform(200, 800, 3)), n_samples),
    'parking_spots': np.random.randint(0, 4, n_samples),
    'days_on_market': np.random.randint(1, 180, n_samples),
    'status': np.random.choice(['Active', 'Pending', 'Sold'], n_samples, p=[0.6, 0.2, 0.2])
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate price per square foot
df['price_per_sqft'] = df['list_price'] / df['sqft']

# Format date as string
df['date_listed'] = df['date_listed'].dt.strftime('%Y-%m-%d')

# Ensure output directory exists
os.makedirs('input', exist_ok=True)

# Save to CSV
df.to_csv('input/immo_data.csv', index=False)
print("Sample data generated successfully!") 