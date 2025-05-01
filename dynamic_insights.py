import numpy as np
import polars as pl
import pandas as pd
from process_data import ProcessData
import calendar
from typing import Dict, List, Tuple


class CreateInsights:

    def __init__(self):
        self.process = ProcessData()
        self.insight_container_style = """
                                        <style>
                                        .insight-container {
                                            padding: 10px;
                                            margin: 5px 0;
                                            border-left: 5px solid #4CAF50;
                                            background-color: #f8f9fa;
                                            animation: fadeIn 1s linear;
                                        }
                                        @keyframes fadeIn {
                                                from { opacity: 0; }
                                                to { opacity: 1; }
                                            }
                                            
                                        
                                        </style>
                                        """

    @staticmethod
    def generate_histogram_insights(df, column_name, currency=False):
        column_map = {
            "baseRent": "'Base Rent'",
            "yearConstructed": "'Year of Construction'",
        }
        # Calculate basic statistics
        most_common_bin = df[column_name].mode()[0]
        average_value = int(df[column_name].mean())
        median_value = int(df[column_name].median())
        max_value = int(df[column_name].max())
        min_value = int(df[column_name].min())

        # Format currency if specified
        currency_symbol = "€" if currency else ""

        # Construct insights text
        insights_text = (
            f"The most common {column_map[column_name]} range is around {currency_symbol}{most_common_bin}. "
            f"The average {column_map[column_name]} is {currency_symbol}{average_value}, "
            f"with a median of {currency_symbol}{median_value}. "
            f"The maximum {column_map[column_name]} found in the dataset is {currency_symbol}{max_value}, "
            f"while the minimum is {currency_symbol}{min_value}."
        )

        return insights_text

    @staticmethod
    def extract_insights_average_rent_over_time(aggregated_df: pl.DataFrame) -> str:
        insight_text = ""
        # Calculate changes in rent over the period
        rent_increase_base = (
            aggregated_df["Average Base Rent"][-1]
            - aggregated_df["Average Base Rent"][0]
        )
        rent_increase_total = (
            aggregated_df["Average Total Rent"][-1]
            - aggregated_df["Average Total Rent"][0]
        )

        # Calculate the percentage change for base and total rent
        percentage_increase_base = (
            rent_increase_base / aggregated_df["Average Base Rent"][0]
        ) * 100
        percentage_increase_total = (
            rent_increase_total / aggregated_df["Average Total Rent"][0]
        ) * 100

        # Identify the period covered by the data
        period_start = aggregated_df["date"][0]
        period_end = aggregated_df["date"][-1]

        # Format dates for display (convert to string if necessary)
        period_start_str = period_start.isoformat()
        period_end_str = period_end.isoformat()

        insight_text += (
            f"<strong>Period covered:</strong>  {period_start_str} to {period_end_str} <br>"
            f"Average base rent increased by {float(rent_increase_base):.2f}€ "
            f"({float(percentage_increase_base):.2f}%) over the period."
            f"Average total rent increased by {float(rent_increase_total):.2f}€ "
            f"({float(percentage_increase_total):.2f}%) over the period."
        )

        # Further analysis or storytelling based on the data
        if percentage_increase_base > 10:
            insight_text += (
                f"<strong>Significant Increase in Base Rent</strong>"
                f"The base rent has seen a significant increase, suggesting a tightening rental market."
            )

        elif percentage_increase_base < -10:

            insight_text += (
                f"<strong>Significant Decrease in Base Rent</strong>"
                f"A notable decrease in base rent could indicate a shift towards a renter's market."
            )

        else:
            insight_text += (
                f"<br><strong>🔄 Stable Rent Prices </strong>"
                f"Rent prices have remained relatively stable, indicating a balanced market condition."
            )

        return insight_text

    def extract_insights_average_rent_over_time_by_type(
        self,
        aggregated_df: pl.DataFrame,
    ) -> str:
        """
        Extract insights from the aggregated DataFrame, now including property types.
        """
        insight_text = ""
        # Ensure the DataFrame is sorted by date
        aggregated_df = aggregated_df.sort(["date", "typeOfFlat"])

        # Get unique property types for analysis
        property_types = self.process.remove_none_from_list(
            list(aggregated_df["typeOfFlat"].unique())
        )

        for property_type in property_types:
            # Filter the DataFrame for each property type
            df_filtered = aggregated_df.filter(pl.col("typeOfFlat") == property_type)

            # Proceed only if df_filtered is not empty
            if not df_filtered.is_empty():
                # Calculate changes in rent over the period for the filtered DataFrame
                rent_increase_base = (
                    df_filtered["Average Base Rent"][-1]
                    - df_filtered["Average Base Rent"][0]
                )
                rent_increase_total = (
                    df_filtered["Average Total Rent"][-1]
                    - df_filtered["Average Total Rent"][0]
                )

                # Calculate the percentage change for base and total rent
                percentage_increase_base = (
                    rent_increase_base / df_filtered["Average Base Rent"][0]
                ) * 100
                percentage_increase_total = (
                    rent_increase_total / df_filtered["Average Total Rent"][0]
                ) * 100

                # Format dates for display
                period_start = df_filtered["date"][0]
                period_end = df_filtered["date"][-1]
                period_start_str = str(
                    period_start
                )  # Ensure conversion to string if necessary
                period_end_str = str(
                    period_end
                )  # Ensure conversion to string if necessary

                # Displaying insights dynamically for each property type
                insight_text += (
                    f"<br><strong>Insights for {property_type} </strong><br>"
                    f"Period covered: {period_start_str} to {period_end_str} "
                    f"Average base rent increased by {float(rent_increase_base):.2f}€ "
                    f"({float(percentage_increase_base):.2f}%) over the period."
                    f"Average total rent increased by {float(rent_increase_total):.2f}€ "
                    f"({float(percentage_increase_total):.2f}%) over the period."
                )

                # Further analysis based on the percentage changes
                # [Your existing analysis logic here]
            else:
                # Handle the case where df_filtered is empty (e.g., log a message or skip)
                insight_text += (
                    f"No data available for property type '{property_type}'."
                )

        return insight_text

    @staticmethod
    def extract_insights_average_rent_by_season(monthly_avg_rent_pd) -> str:
        # Check if the DataFrame is empty
        # Initialize an insight string
        insight_text = ""

        if monthly_avg_rent_pd.empty:
            return "No data available for the selected period."

        # Find months with maximum and minimum average base rent
        max_rent_month = monthly_avg_rent_pd.loc[
            monthly_avg_rent_pd["average_baseRent"].idxmax(), "month"
        ]
        min_rent_month = monthly_avg_rent_pd.loc[
            monthly_avg_rent_pd["average_baseRent"].idxmin(), "month"
        ]

        # Convert month numbers to names
        max_rent_month_name = calendar.month_name[max_rent_month]
        min_rent_month_name = calendar.month_name[min_rent_month]

        # Find the corresponding max and min rent values
        max_rent_value = monthly_avg_rent_pd["average_baseRent"].max()
        min_rent_value = monthly_avg_rent_pd["average_baseRent"].min()

        # Constructing insight text based on analysis
        insight_text += (
            f"The highest average base rent was observed in "
            f"{max_rent_month_name} at €{max_rent_value:.2f}, "
            f"while the lowest was in {min_rent_month_name} at €{min_rent_value:.2f}. "
        )

        if max_rent_month in [6, 7, 8]:
            insight_text += "This peak during the summer months could suggest higher demand for rentals. "
        elif min_rent_month in [12, 1, 2]:
            insight_text += "The decrease in rent prices during winter may indicate a lower demand. "

        return insight_text

    @staticmethod
    def generate_dynamic_insights_impact_prop_on_rental(plot_data: pl.DataFrame) -> str:
        insights_text = ""
        for i in range(
            0, len(plot_data["Feature"]), 2
        ):  # Iterate through each feature pair
            feature = plot_data["Feature"][i]
            p_value = plot_data["P-Value"][i]
            significant = (
                "is statistically significant"
                if p_value < 0.05
                else "is not statistically significant"
            )

            insights_text += (
                f" \n The difference in rent for properties with and without **{feature}** {significant}"
                f" (p-value: {p_value:.3f})."
            )

            if p_value < 0.05:
                condition_with = (
                    "with"
                    if plot_data["Average Base Rent"][i]
                    > plot_data["Average Base Rent"][i + 1]
                    else "Without"
                )
                difference = abs(
                    plot_data["Average Base Rent"][i]
                    - plot_data["Average Base Rent"][i + 1]
                )
                insights_text += (
                    f"\n Properties {condition_with} **{feature}** have an average rent difference "
                    f"of €{difference:.2f} compared to those without.\n"
                )

        return insights_text

    @staticmethod
    def generate_age_heatmap_insights(pivot_df):
        # Find the age group and rent range with the highest number of properties

        max_count_location = np.unravel_index(
            np.argmax(pivot_df.values, axis=None), pivot_df.shape
        )
        max_rent_range = pivot_df.index[max_count_location[0]]
        max_age_group = pivot_df.columns[max_count_location[1]]

        insight_text = (
            f"The highest concentration of properties is found within the rent range {max_rent_range} € "
            f"for properties in the age group of {max_age_group} years. "
            f"This suggests a strong preference or availability in this segment."
        )

        # Optionally, add insights about general trends observed in the heatmap
        general_trends = (
            "The heatmap visualization indicates that newer properties (lower age groups) "
            "tend to have a higher rent price range, highlighting the premium associated "
            "with new constructions. Conversely, older properties show a wider distribution "
            "of rent prices, reflecting a diverse market."
        )

        return insight_text + "\n" + general_trends

    @staticmethod
    def extract_insights_affordability(df):
        if not df.empty:
            # Filter for high ratio regions and extract as a list
            high_ratio_regions = (
                df[df["Average Rent-to-Income Ratio"] > 30]["region"].unique().tolist()
            )

            # Filter for low ratio regions and extract as a list
            low_ratio_regions = (
                df[df["Average Rent-to-Income Ratio"] <= 30]["region"].unique().tolist()
            )

            # Convert lists to formatted strings for display
            high_ratio_text = ", ".join(high_ratio_regions)
            low_ratio_text = ", ".join(low_ratio_regions)

            insights_text = (
                f"In particular, regions such as {high_ratio_text} "
                f"exhibit rent-to-income ratios that might pose affordability challenges. "
                f"On the other hand, regions like {low_ratio_text} appear to offer a more balanced"
                f" economic environment for renters."
            )
            return insights_text

    @staticmethod
    def generate_map_insights(final_df: pd.DataFrame):
        if final_df.empty:
            return "No data available for the selected filters."

            # Finding regions with the highest and lowest median rents
        highest_rent_region = final_df.loc[final_df["MedianRent"].idxmax(), "region"]
        lowest_rent_region = final_df.loc[final_df["MedianRent"].idxmin(), "region"]
        highest_rent_value = final_df["MedianRent"].max()
        lowest_rent_value = final_df["MedianRent"].min()

        # Finding regions with the most and least properties available
        most_properties_region = final_df.loc[
            final_df["CountOfProperties"].idxmax(), "region"
        ]
        least_properties_region = final_df.loc[
            final_df["CountOfProperties"].idxmin(), "region"
        ]
        most_properties_count = final_df["CountOfProperties"].max()
        least_properties_count = final_df["CountOfProperties"].min()

        # Constructing the insight text
        insights_text = (
            f"Regions with the highest and lowest median rents are <strong>{highest_rent_region}</strong> (€{highest_rent_value}) "
            f"and <strong>{lowest_rent_region}</strong> (€{lowest_rent_value}), respectively. "
            f"<strong>{most_properties_region}</strong> stands out with the highest number of "
            f"properties available for rent ({most_properties_count}), "
            f"while <strong>{least_properties_region}</strong> has the least ({least_properties_count})."
        )

        return insights_text

class DynamicInsights:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.insights = []

    def generate_all_insights(self) -> List[str]:
        """Generate all available insights from the data."""
        self.insights = []
        
        self._add_price_insights()
        self._add_property_type_insights()
        self._add_location_insights()
        self._add_amenity_insights()
        self._add_market_dynamics_insights()
        
        return self.insights

    def _add_price_insights(self):
        """Add insights related to property prices."""
        median_price = self.df["list_price"].median()
        avg_price = self.df["list_price"].mean()
        price_std = self.df["list_price"].std()
        
        self.insights.append(
            f"The median property price is ${median_price:,.2f}, "
            f"with an average of ${avg_price:,.2f}."
        )
        
        if price_std > avg_price * 0.5:
            self.insights.append(
                "There is significant price variation in the market, "
                "suggesting diverse property options."
            )
            
        # Price per square foot analysis
        median_ppsf = self.df["price_per_sqft"].median()
        self.insights.append(
            f"The median price per square foot is ${median_ppsf:.2f}."
        )
        
        # Price range distribution
        luxury_threshold = self.df["list_price"].quantile(0.9)
        luxury_count = len(self.df[self.df["list_price"] >= luxury_threshold])
        self.insights.append(
            f"There are {luxury_count} luxury properties "
            f"priced above ${luxury_threshold:,.2f}."
        )

    def _add_property_type_insights(self):
        """Add insights related to property types."""
        type_counts = self.df["property_type"].value_counts()
        most_common = type_counts.index[0]
        pct_most_common = (type_counts[most_common] / len(self.df)) * 100
        
        self.insights.append(
            f"{most_common} properties are most common, "
            f"representing {pct_most_common:.1f}% of listings."
        )
        
        # Average price by property type
        avg_price_by_type = self.df.groupby("property_type")["list_price"].mean()
        most_expensive_type = avg_price_by_type.idxmax()
        self.insights.append(
            f"{most_expensive_type} properties have the highest average price "
            f"at ${avg_price_by_type[most_expensive_type]:,.2f}."
        )

    def _add_location_insights(self):
        """Add insights related to property locations."""
        if "city" in self.df.columns:
            city_counts = self.df["city"].value_counts()
            top_city = city_counts.index[0]
            city_avg_price = self.df[self.df["city"] == top_city]["list_price"].mean()
            
            self.insights.append(
                f"{top_city} has the most listings with {city_counts[top_city]} properties "
                f"and an average price of ${city_avg_price:,.2f}."
            )
        
        if "state" in self.df.columns:
            state_avg_price = self.df.groupby("state")["list_price"].mean()
            most_expensive_state = state_avg_price.idxmax()
            self.insights.append(
                f"{most_expensive_state} has the highest average property price "
                f"at ${state_avg_price[most_expensive_state]:,.2f}."
            )

    def _add_amenity_insights(self):
        """Add insights related to property amenities."""
        if "has_pool" in self.df.columns:
            pool_premium = (
                self.df[self.df["has_pool"]]["list_price"].mean()
                - self.df[~self.df["has_pool"]]["list_price"].mean()
            )
            if pool_premium > 0:
                self.insights.append(
                    f"Properties with pools command a premium of ${pool_premium:,.2f} "
                    "on average."
                )
        
        if "has_basement" in self.df.columns:
            basement_premium = (
                self.df[self.df["has_basement"]]["list_price"].mean()
                - self.df[~self.df["has_basement"]]["list_price"].mean()
            )
            if basement_premium > 0:
                self.insights.append(
                    f"Properties with basements command a premium of ${basement_premium:,.2f} "
                    "on average."
                )

    def _add_market_dynamics_insights(self):
        """Add insights related to market dynamics."""
        if "days_on_market" in self.df.columns:
            median_dom = self.df["days_on_market"].median()
            quick_sales = len(self.df[self.df["days_on_market"] <= 7])
            
            self.insights.append(
                f"The median time on market is {median_dom:.0f} days, "
                f"with {quick_sales} properties selling within a week."
            )
        
        if "status" in self.df.columns:
            active_listings = len(self.df[self.df["status"] == "Active"])
            pending_listings = len(self.df[self.df["status"] == "Pending"])
            
            self.insights.append(
                f"There are currently {active_listings} active listings "
                f"and {pending_listings} pending sales."
            )

    def get_top_insights(self, n: int = 5) -> List[str]:
        """Return the top N insights."""
        if not self.insights:
            self.generate_all_insights()
        return self.insights[:n]
