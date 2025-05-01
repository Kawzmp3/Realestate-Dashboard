# US Real Estate Market Analysis Dashboard

## Overview
This Streamlit-powered dashboard provides comprehensive analysis and insights into the US real estate market. The application offers interactive visualizations, dynamic filtering, and automated market insights to help users make data-driven decisions in real estate.

## Application Flow

```mermaid
graph TD
    A[User Access] --> B[Load Application]
    B --> C[Initialize Data]
    C --> D[Apply Filters]
    D --> E[Generate Visualizations]
    E --> F[Update Insights]
    F --> D
    
    subgraph Filters
    D1[Price Range] --> D
    D2[Property Type] --> D
    D3[Location] --> D
    end
    
    subgraph Visualizations
    E1[Price Analysis] --> E
    E2[Property Distribution] --> E
    E3[Geographic Maps] --> E
    E4[Market Trends] --> E
    end
```

## Data Processing Architecture

```mermaid
flowchart LR
    A[Raw Data] --> B[Data Processing]
    B --> C[Filtered Dataset]
    C --> D[Visualizations]
    C --> E[Analytics]
    
    subgraph Processing
    B1[Clean Data] --> B
    B2[Transform] --> B
    B3[Validate] --> B
    end
    
    subgraph Analytics Engine
    E1[Statistical Analysis]
    E2[Market Insights]
    E3[Trend Detection]
    end
    
    E --> E1
    E --> E2
    E --> E3
```

## Component Architecture

```mermaid
graph TD
    A[Main App] --> B[Config Module]
    A --> C[Graphs Module]
    A --> D[Dynamic Insights]
    
    B --> B1[File Paths]
    B --> B2[Parameters]
    B --> B3[Column Definitions]
    
    C --> C1[Price Analysis]
    C --> C2[Property Analysis]
    C --> C3[Location Analysis]
    C --> C4[Market Trends]
    
    D --> D1[Market Insights]
    D --> D2[Statistical Analysis]
    D --> D3[Trend Detection]
```

## Features

### 1. Interactive Filtering
- Price range selection
- Property type filtering
- Geographic filtering (State and City level)
- Real-time visualization updates

### 2. Market Overview
- Median Property Price
- Median Price per Square Foot
- Active Listings Count
- Market Trend Indicators

### 3. Data Analysis Components

#### Price Analysis
- Price distribution histograms
- Price range distribution
- Price per square foot analysis

#### Property Analysis
- Property type distribution
- Bedroom/bathroom configurations
- Square footage analysis
- Amenities impact analysis

#### Location Analysis
- State-level price choropleth map
- Geographic price distribution
- Regional market trends

#### Market Dynamics
- Price trends over time
- Days on market analysis
- Property status distribution

### 4. Dynamic Insights Engine
- Automated market insights
- Trend identification
- Comparative analysis
- Market opportunity detection

## Data Structure

### Property Information
- List price
- Price per square foot
- HOA fees
- Property tax
- Monthly costs

### Property Characteristics
- Square footage
- Bedrooms/bathrooms
- Year built
- Property type
- Lot size

### Location Data
- State
- City
- ZIP code
- Neighborhood type

### Additional Metrics
- Energy ratings
- School information
- Walk/transit scores
- Crime rate percentiles

## Technical Stack

```mermaid
graph LR
    A[Frontend] --> B[Streamlit]
    A --> C[Plotly]
    
    D[Backend] --> E[Python]
    D --> F[Pandas/Polars]
    D --> G[NumPy]
    
    H[Visualization] --> I[Plotly Express]
    H --> J[Graph Objects]
    
    K[Data Storage] --> L[CSV]
    K --> M[Configuration Files]
```

## Use Cases

### Market Research
- Track price trends
- Identify market opportunities
- Analyze regional variations

### Property Comparison
- Compare property types
- Analyze price/sqft metrics
- Evaluate amenity impact

### Investment Analysis
- Monitor market dynamics
- Identify high-value areas
- Analyze price-to-feature relationships

### Market Intelligence
- Access automated insights
- Track market changes
- Identify patterns

## Getting Started

1. Install dependencies:
```bash
pipenv install
```

2. Run the application:
```bash
pipenv run streamlit run app.py
```

## Dependencies
- streamlit>=1.27.0
- pandas>=2.0.0
- numpy>=1.24.0
- plotly-express>=0.4.1
- plotly>=5.17.0
- polars==0.20.5
- matplotlib
- seaborn

## Configuration
The application uses a configuration module for managing:
- File paths
- Data column definitions
- Visualization parameters
- Analysis settings

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request. 