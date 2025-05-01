from dataclasses import dataclass
from pathlib import Path


# define project configurations
@dataclass
class Config:
    project_path: Path = Path(__file__).parent.resolve()
    input_path: Path = project_path.joinpath("input")
    img_path: Path = project_path.joinpath("img")
    csv_file_name = "real_estate_data.csv"

    # Create directories if they don't exist
    input_path.mkdir(exist_ok=True)
    img_path.mkdir(exist_ok=True)

    ignore_columns = [
        "price_history",
    ]

    column_order = [
        "city",
        "state",
        "list_price",
        "price_per_sqft",
        "square_feet",
        "bedrooms",
        "bathrooms",
        "property_type",
        "year_built",
        "days_on_market",
        "status",
        "neighborhood_type",
        "walk_score",
        "transit_score"
    ]

    location_details = {
        "city": "City where the property is located",
        "state": "State where the property is located",
        "zip_code": "ZIP code of the property",
        "neighborhood_type": "Type of neighborhood (Urban, Suburban, Rural)",
        "walk_score": "Walkability score (0-100)",
        "transit_score": "Public transit accessibility score (0-100)",
        "crime_rate_percentile": "Crime rate percentile (lower is better)"
    }

    property_features = {
        "square_feet": "Total living area in square feet",
        "bedrooms": "Number of bedrooms",
        "bathrooms": "Number of bathrooms",
        "year_built": "Year the property was constructed",
        "property_type": "Type of property (Single Family, Condo, etc.)",
        "lot_size": "Total lot size in square feet"
    }

    amenities = {
        "garage_spaces": "Number of garage parking spaces",
        "has_pool": "Whether the property has a pool",
        "has_basement": "Whether the property has a basement",
        "cooling_system": "Type of cooling system",
        "heating_system": "Type of heating system"
    }

    financial_details = {
        "list_price": "Current listing price",
        "price_per_sqft": "Price per square foot",
        "hoa_fee": "Monthly HOA fees if applicable",
        "property_tax": "Annual property tax",
        "estimated_monthly_cost": "Estimated total monthly cost including mortgage, taxes, and fees",
        "last_sold_price": "Previous sale price",
        "last_sold_date": "Date of previous sale"
    }

    construction_and_efficiency = {
        "year_built": "Year of construction",
        "energy_rating": "Energy efficiency rating (A-E)",
        "estimated_utility_cost": "Estimated monthly utility costs",
        "solar_panels": "Whether the property has solar panels"
    }

    additional_descriptions = {
        "days_on_market": "Number of days the property has been listed",
        "status": "Current listing status (Active, Pending, Sold, New)",
        "description": "Detailed property description",
        "elementary_school_rating": "Rating of nearest elementary school (1-10)",
        "middle_school_rating": "Rating of nearest middle school (1-10)",
        "high_school_rating": "Rating of nearest high school (1-10)"
    }

    replace_dict = {
        "apt": "apartment",
        "condo": "condominium",
        "sfh": "single family home",
        "th": "townhouse",
        "mf": "multi-family"
    }
