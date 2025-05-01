import pandas as pd
import numpy as np
import datetime

# Create sample data
n_samples = 1000

# Generate random data for US real estate market
data = {
    # Price Information
    'list_price': np.random.normal(450000, 150000, n_samples),  # US average home price
    'price_per_sqft': np.random.normal(200, 50, n_samples),
    'hoa_fee': np.random.choice([0] + list(np.random.normal(300, 100, 100)), n_samples),  # HOA fees if applicable
    'property_tax': None,  # Will be calculated as % of price
    'estimated_monthly_cost': None,  # Will be calculated
    
    # Property Characteristics
    'square_feet': np.random.normal(2000, 500, n_samples),
    'bedrooms': np.random.choice([1, 2, 3, 4, 5, 6], n_samples, p=[0.05, 0.15, 0.4, 0.25, 0.1, 0.05]),
    'bathrooms': np.random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4], n_samples),
    'year_built': np.random.randint(1950, 2024, n_samples),
    'property_type': np.random.choice(['Single Family', 'Condo', 'Townhouse', 'Multi-Family', 'Apartment'], n_samples),
    'lot_size': np.random.normal(6000, 2000, n_samples),  # in square feet
    
    # Location
    'state': np.random.choice(['CA', 'NY', 'TX', 'FL', 'IL', 'WA', 'MA', 'CO', 'AZ', 'GA'], n_samples),
    'city': None,  # Will be filled based on state
    'zip_code': np.random.randint(10000, 99999, n_samples),
    'neighborhood_type': np.random.choice(['Urban', 'Suburban', 'Rural'], n_samples),
    
    # Property Features
    'garage_spaces': np.random.choice([0, 1, 2, 3], n_samples),
    'has_pool': np.random.choice([True, False], n_samples, p=[0.2, 0.8]),
    'has_basement': np.random.choice([True, False], n_samples),
    'cooling_system': np.random.choice(['Central', 'Window Units', 'None'], n_samples),
    'heating_system': np.random.choice(['Forced Air', 'Heat Pump', 'Electric', 'Gas', 'Oil'], n_samples),
    
    # Energy and Utilities
    'energy_rating': np.random.choice(['A', 'B', 'C', 'D', 'E'], n_samples),
    'estimated_utility_cost': np.random.normal(200, 50, n_samples),
    'solar_panels': np.random.choice([True, False], n_samples, p=[0.1, 0.9]),
    
    # Market Data
    'days_on_market': np.random.randint(0, 180, n_samples),
    'date_listed': [datetime.date(2023, np.random.randint(1, 13), np.random.randint(1, 28)) for _ in range(n_samples)],
    'price_history': None,  # Will be calculated
    'status': np.random.choice(['Active', 'Pending', 'Sold', 'New'], n_samples),
    
    # School Information
    'elementary_school_rating': np.random.randint(1, 11, n_samples),
    'middle_school_rating': np.random.randint(1, 11, n_samples),
    'high_school_rating': np.random.randint(1, 11, n_samples),
    
    # Neighborhood Data
    'walk_score': np.random.randint(0, 101, n_samples),
    'transit_score': np.random.randint(0, 101, n_samples),
    'crime_rate_percentile': np.random.randint(0, 101, n_samples),
    
    # Additional Details
    'description': ['Beautiful home in prime location' for _ in range(n_samples)],
    'last_sold_price': None,  # Will be calculated
    'last_sold_date': None,  # Will be calculated
}

# Create DataFrame
df = pd.DataFrame(data)

# Add city data based on state
state_cities = {
    'CA': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento'],
    'NY': ['New York City', 'Buffalo', 'Albany', 'Rochester'],
    'TX': ['Houston', 'Austin', 'Dallas', 'San Antonio'],
    'FL': ['Miami', 'Orlando', 'Tampa', 'Jacksonville'],
    'IL': ['Chicago', 'Springfield', 'Naperville', 'Aurora'],
    'WA': ['Seattle', 'Tacoma', 'Spokane', 'Bellevue'],
    'MA': ['Boston', 'Cambridge', 'Worcester', 'Springfield'],
    'CO': ['Denver', 'Boulder', 'Colorado Springs', 'Fort Collins'],
    'AZ': ['Phoenix', 'Tucson', 'Scottsdale', 'Mesa'],
    'GA': ['Atlanta', 'Savannah', 'Augusta', 'Athens']
}

df['city'] = df['state'].apply(lambda x: np.random.choice(state_cities[x]))

# Calculate derived fields
df['property_tax'] = df['list_price'] * np.random.uniform(0.01, 0.03, n_samples)  # 1-3% property tax
df['estimated_monthly_cost'] = (df['list_price'] * 0.06 / 12) + (df['property_tax'] / 12) + df['hoa_fee'] + df['estimated_utility_cost']  # Rough monthly cost

# Generate price history (last 2 years)
df['last_sold_price'] = df['list_price'] * np.random.uniform(0.8, 0.95, n_samples)  # Previous price 80-95% of current
df['last_sold_date'] = [datetime.date(2022, np.random.randint(1, 13), np.random.randint(1, 28)) for _ in range(n_samples)]

# Clean up the data
numeric_columns = ['list_price', 'price_per_sqft', 'hoa_fee', 'property_tax', 'estimated_monthly_cost', 
                  'square_feet', 'lot_size', 'estimated_utility_cost', 'last_sold_price']
for col in numeric_columns:
    df[col] = df[col].round(2).abs()

# Save to CSV
df.to_csv('input/real_estate_data.csv', index=False) 