import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from config import Config
from graphs import (
    create_price_distribution_plot,
    create_price_per_sqft_plot,
    create_property_type_distribution,
    create_price_trend_plot,
    create_amenities_comparison,
    create_location_price_map,
    create_correlation_heatmap,
    create_bedroom_bathroom_plot,
    create_price_range_distribution
)
from dynamic_insights import DynamicInsights

# Page configuration
st.set_page_config(
    page_title="US Real Estate Market Insights",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load configuration
config = Config()

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(config.input_path.joinpath(config.csv_file_name))
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")

# Price range filter
price_range = st.sidebar.slider(
    "Price Range",
    min_value=int(df["list_price"].min()),
    max_value=int(df["list_price"].max()),
    value=(int(df["list_price"].min()), int(df["list_price"].max())),
    step=10000,
)

# Property type filter
property_types = st.sidebar.multiselect(
    "Property Type",
    options=sorted(df["property_type"].unique()),
    default=sorted(df["property_type"].unique()),
)

# Location filters
if "state" in df.columns:
    states = st.sidebar.multiselect(
        "State",
        options=sorted(df["state"].unique()),
        default=sorted(df["state"].unique()),
    )

if "city" in df.columns:
    cities = st.sidebar.multiselect(
        "City",
        options=sorted(df["city"].unique()),
        default=sorted(df["city"].unique()),
)

# Apply filters
mask = (
    (df["list_price"].between(price_range[0], price_range[1]))
    & (df["property_type"].isin(property_types))
)

if "state" in df.columns:
    mask &= df["state"].isin(states)
if "city" in df.columns:
    mask &= df["city"].isin(cities)

filtered_df = df[mask]

# Main content
st.title("🏠 US Real Estate Market Insights")
st.markdown("### Interactive dashboard for analyzing the US real estate market")

# Market Overview
st.header("Market Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Median Price",
        f"${filtered_df['list_price'].median():,.0f}",
        delta=f"{((filtered_df['list_price'].median() / df['list_price'].median()) - 1) * 100:.1f}%",
    )

with col2:
    st.metric(
        "Median Price/sqft",
        f"${filtered_df['price_per_sqft'].median():,.2f}",
        delta=f"{((filtered_df['price_per_sqft'].median() / df['price_per_sqft'].median()) - 1) * 100:.1f}%",
    )

with col3:
    st.metric(
        "Active Listings",
        len(filtered_df),
        delta=f"{(len(filtered_df) / len(df) - 1) * 100:.1f}%",
    )

# Dynamic Insights
st.header("Market Insights")
insights = DynamicInsights(filtered_df)
for insight in insights.get_top_insights():
    st.info(insight)

# Price Analysis
st.header("Price Analysis")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        create_price_distribution_plot(filtered_df),
        use_container_width=True,
    )

with col2:
    st.plotly_chart(
        create_price_range_distribution(filtered_df),
        use_container_width=True,
    )

# Property Characteristics
st.header("Property Characteristics")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        create_property_type_distribution(filtered_df),
        use_container_width=True,
    )

with col2:
    st.plotly_chart(
        create_price_per_sqft_plot(filtered_df),
        use_container_width=True,
    )

# Market Dynamics
st.header("Market Dynamics")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        create_price_trend_plot(filtered_df),
        use_container_width=True,
    )

with col2:
    st.plotly_chart(
        create_bedroom_bathroom_plot(filtered_df),
        use_container_width=True,
    )

# Location Analysis
st.header("Location Analysis")
st.plotly_chart(
    create_location_price_map(filtered_df),
    use_container_width=True,
)

# Amenities Analysis
st.header("Amenities Analysis")
st.plotly_chart(
    create_amenities_comparison(filtered_df),
    use_container_width=True,
)

# Correlation Analysis
st.header("Feature Correlations")
numeric_columns = [
    "list_price",
    "square_feet",
    "bedrooms",
    "bathrooms",
    "year_built",
    "days_on_market",
    "price_per_sqft",
]
numeric_columns = [col for col in numeric_columns if col in filtered_df.columns]
st.plotly_chart(
    create_correlation_heatmap(filtered_df, numeric_columns),
    use_container_width=True,
)

# Footer
st.markdown("---")
st.markdown(
    "Data updated daily. All prices in USD. Created with Streamlit by Your Company Name."
    )
