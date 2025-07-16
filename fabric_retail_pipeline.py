"""
Microsoft Fabric Retail Data Pipeline Templates
Bronze -> Silver -> Gold transformations for retail analytics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class FabricRetailDataPipeline:
    """
    Data transformation pipeline for Microsoft Fabric Retail solutions
    Implements Bronze -> Silver -> Gold medallion architecture
    """
    
    def __init__(self):
        self.bronze_data = {}
        self.silver_data = {}
        self.gold_data = {}
        
    # BRONZE LAYER - Raw data ingestion
    def ingest_bronze_data(self, data_source_path):
        """Load raw data into Bronze layer"""
        try:
            # Load raw CSV files
            self.bronze_data['customers'] = pd.read_csv(f"{data_source_path}/customers.csv")
            self.bronze_data['products'] = pd.read_csv(f"{data_source_path}/products.csv")
            self.bronze_data['orders'] = pd.read_csv(f"{data_source_path}/orders.csv")
            
            # Add ingestion metadata
            ingestion_time = datetime.now().isoformat()
            for table_name, df in self.bronze_data.items():
                df['_ingestion_timestamp'] = ingestion_time
                df['_source_file'] = f"{table_name}.csv"
                df['_record_id'] = df.index + 1
                
            print("✅ Bronze layer data ingestion complete")
            return True
        except Exception as e:
            print(f"❌ Bronze ingestion failed: {e}")
            return False
    
    # SILVER LAYER - Cleaned and standardized data
    def transform_to_silver(self):
        """Transform Bronze data to Silver layer with data quality improvements"""
        
        # Transform Customers
        self.silver_data['customers'] = self._clean_customers_data()
        
        # Transform Products  
        self.silver_data['products'] = self._clean_products_data()
        
        # Transform Orders
        self.silver_data['orders'] = self._clean_orders_data()
        
        # Add cross-table validations
        self._validate_silver_data_integrity()
        
        print("✅ Silver layer transformations complete")
        
    def _clean_customers_data(self):
        """Clean and standardize customer data"""
        df = self.bronze_data['customers'].copy()
        
        # Data type conversions
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
        df['age'] = df['age'].astype('Int64')  # Handle NaN values
        
        # Data standardization
        df['gender'] = df['gender'].str.upper()
        df['membership'] = df['membership'].str.upper()
        df['email'] = df['email'].str.lower().str.strip()
        df['phone'] = df['phone'].str.replace(r'[^\d-]', '', regex=True)
        
        # Address parsing
        df['full_address'] = df['post_address']
        address_parts = df['post_address'].str.extract(r'(.+),\s*(.+),\s*([A-Z]{2})\s+(\d{5})')
        df['street_address'] = address_parts[0]
        df['city'] = address_parts[1]
        df['state'] = address_parts[2]
        df['postal_code'] = address_parts[3]
        
        # Data quality flags
        df['email_valid'] = df['email'].str.contains(r'^[^@]+@[^@]+\.[^@]+$', na=False)
        df['phone_valid'] = df['phone'].str.len() >= 10
        df['address_complete'] = df[['street_address', 'city', 'state', 'postal_code']].notna().all(axis=1)
        
        # Business rules
        df['is_adult'] = df['age'] >= 18
        df['age_group'] = pd.cut(df['age'], 
                                bins=[0, 25, 35, 50, 65, 100], 
                                labels=['18-25', '26-35', '36-50', '51-65', '65+'])
        
        # Calculated fields
        df['customer_since_days'] = (datetime.now() - df['date_of_birth']).dt.days
        df['membership_tier_numeric'] = df['membership'].map({'BASE': 1, 'GOLD': 2, 'PLATINUM': 3})
        
        # Add audit fields
        df['silver_processed_timestamp'] = datetime.now().isoformat()
        df['data_quality_score'] = (df[['email_valid', 'phone_valid', 'address_complete']].sum(axis=1) / 3 * 100).round(1)
        
        return df
        
    def _clean_products_data(self):
        """Clean and standardize product data"""
        df = self.bronze_data['products'].copy()
        
        # Data type conversions
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Text standardization
        df['product_name'] = df['product_name'].str.strip()
        df['category'] = df['category'].str.strip().str.title()
        df['brand'] = df['brand'].str.strip()
        
        # Category hierarchy
        category_mapping = {
            'Tents': {'parent': 'Camping Gear', 'level': 'Shelter'},
            'Backpacks': {'parent': 'Hiking Gear', 'level': 'Carry'},
            'Hiking Clothing': {'parent': 'Apparel', 'level': 'Outdoor Wear'},
            'Hiking Footwear': {'parent': 'Footwear', 'level': 'Outdoor Shoes'},
            'Camping Tables': {'parent': 'Camping Gear', 'level': 'Furniture'},
            'Camping Stoves': {'parent': 'Camping Gear', 'level': 'Cooking'},
            'Sleeping Bags': {'parent': 'Camping Gear', 'level': 'Sleep'}
        }
        
        df['category_parent'] = df['category'].map(lambda x: category_mapping.get(x, {}).get('parent', 'Other'))
        df['category_level'] = df['category'].map(lambda x: category_mapping.get(x, {}).get('level', 'Other'))
        
        # Price analysis
        df['price_tier'] = pd.cut(df['price'], 
                                 bins=[0, 75, 150, 300, float('inf')], 
                                 labels=['Budget', 'Mid-Range', 'Premium', 'Luxury'])
        
        # Text analysis for descriptions
        df['description_length'] = df['product_description'].str.len()
        df['description_word_count'] = df['product_description'].str.split().str.len()
        
        # Product attributes extraction
        df['is_waterproof'] = df['product_description'].str.contains('water', case=False)
        df['is_lightweight'] = df['product_description'].str.contains('lightweight|light weight', case=False)
        df['is_durable'] = df['product_description'].str.contains('durable|durability', case=False)
        
        # Business calculations
        df['estimated_margin'] = df['price'] * 0.3  # Assume 30% margin
        df['weight_category'] = pd.cut(df.get('weight_kg', pd.Series([1]*len(df))), 
                                      bins=[0, 1, 5, 10, float('inf')], 
                                      labels=['Light', 'Medium', 'Heavy', 'Very Heavy'])
        
        # Add audit fields
        df['silver_processed_timestamp'] = datetime.now().isoformat()
        df['data_completeness_score'] = ((df[['product_name', 'price', 'category', 'brand']].notna().sum(axis=1) / 4) * 100).round(1)
        
        return df
        
    def _clean_orders_data(self):
        """Clean and standardize order data"""
        df = self.bronze_data['orders'].copy()
        
        # Data type conversions
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
        df['total'] = pd.to_numeric(df['total'], errors='coerce')
        df['customer_age'] = pd.to_numeric(df['customer_age'], errors='coerce')
        
        # Business validation
        df['calculated_total'] = (df['quantity'] * df['unit_price']).round(2)
        df['total_matches'] = abs(df['total'] - df['calculated_total']) < 0.01
        
        # Temporal features
        df['order_year'] = df['order_date'].dt.year
        df['order_month'] = df['order_date'].dt.month
        df['order_quarter'] = df['order_date'].dt.quarter
        df['order_day_of_week'] = df['order_date'].dt.day_name()
        df['order_day_of_month'] = df['order_date'].dt.day
        df['is_weekend'] = df['order_date'].dt.weekday >= 5
        df['is_month_end'] = df['order_date'].dt.day >= 25
        
        # Customer segmentation at order time
        df['customer_age_group'] = pd.cut(df['customer_age'], 
                                         bins=[0, 25, 35, 50, 65, 100], 
                                         labels=['18-25', '26-35', '36-50', '51-65', '65+'])
        df['customer_segment'] = df['customer_gender'] + '_' + df['customer_age_group'].astype(str)
        
        # Order size categorization
        df['order_size'] = pd.cut(df['total'], 
                                 bins=[0, 50, 150, 500, float('inf')], 
                                 labels=['Small', 'Medium', 'Large', 'XLarge'])
        
        # Return analysis
        df['return_status'] = df['return_status'].fillna(False)
        df['is_returned'] = df['return_status']
        
        # Seasonal analysis
        df['season'] = df['order_month'].map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        })
        
        # Days since order
        df['days_since_order'] = (datetime.now() - df['order_date']).dt.days
        df['is_recent_order'] = df['days_since_order'] <= 30
        
        # Add audit fields
        df['silver_processed_timestamp'] = datetime.now().isoformat()
        df['data_quality_score'] = ((df[['customer_id', 'product_id', 'order_date', 'total']].notna().sum(axis=1) / 4) * 100).round(1)
        
        return df
        
    def _validate_silver_data_integrity(self):
        """Validate data integrity across tables"""
        validations = {}
        
        # Check customer references in orders
        orders_customers = set(self.silver_data['orders']['customer_id'].unique())
        master_customers = set(self.silver_data['customers']['id'].unique())
        validations['orphaned_customers_in_orders'] = orders_customers - master_customers
        
        # Check product references in orders
        orders_products = set(self.silver_data['orders']['product_id'].unique())
        master_products = set(self.silver_data['products']['id'].unique())
        validations['orphaned_products_in_orders'] = orders_products - master_products
        
        # Date range validations
        min_order_date = self.silver_data['orders']['order_date'].min()
        max_order_date = self.silver_data['orders']['order_date'].max()
        validations['order_date_range'] = f"{min_order_date} to {max_order_date}"
        
        # Save validation results
        with open('silver_data_validation.json', 'w') as f:
            json.dump(validations, f, indent=2, default=str)
            
        print("✅ Data integrity validation complete")
    
    # GOLD LAYER - Business-ready analytics tables
    def transform_to_gold(self):
        """Create Gold layer analytics tables"""
        
        # Customer analytics
        self.gold_data['customer_analytics'] = self._create_customer_analytics()
        
        # Product analytics
        self.gold_data['product_analytics'] = self._create_product_analytics()
        
        # Sales analytics
        self.gold_data['sales_analytics'] = self._create_sales_analytics()
        
        # Cross-selling analytics
        self.gold_data['cross_sell_analytics'] = self._create_cross_sell_analytics()
        
        # Time series analytics
        self.gold_data['time_series_analytics'] = self._create_time_series_analytics()
        
        print("✅ Gold layer analytics tables created")
        
    def _create_customer_analytics(self):
        """Create customer analytics table (RFM, CLV, segmentation)"""
        customers = self.silver_data['customers']
        orders = self.silver_data['orders']
        
        # Customer order aggregations
        customer_metrics = orders.groupby('customer_id').agg({
            'order_date': ['count', 'min', 'max'],
            'total': ['sum', 'mean', 'median'],
            'quantity': 'sum',
            'is_returned': 'sum'
        }).round(2)
        
        customer_metrics.columns = [
            'order_count', 'first_order_date', 'last_order_date',
            'total_spent', 'avg_order_value', 'median_order_value',
            'total_items_purchased', 'total_returns'
        ]
        customer_metrics = customer_metrics.reset_index()
        
        # RFM Analysis
        current_date = datetime.now()
        customer_metrics['recency_days'] = (current_date - customer_metrics['last_order_date']).dt.days
        customer_metrics['frequency'] = customer_metrics['order_count']
        customer_metrics['monetary'] = customer_metrics['total_spent']
        
        # RFM Scoring (1-5 scale)
        customer_metrics['recency_score'] = pd.qcut(customer_metrics['recency_days'], 5, labels=[5,4,3,2,1])
        customer_metrics['frequency_score'] = pd.qcut(customer_metrics['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
        customer_metrics['monetary_score'] = pd.qcut(customer_metrics['monetary'], 5, labels=[1,2,3,4,5])
        
        # Customer Lifetime Value (simplified)
        customer_metrics['avg_days_between_orders'] = customer_metrics.apply(
            lambda x: (x['last_order_date'] - x['first_order_date']).days / max(x['order_count'] - 1, 1) if x['order_count'] > 1 else 0, axis=1
        )
        customer_metrics['predicted_lifetime_orders'] = customer_metrics.apply(
            lambda x: max(365 / x['avg_days_between_orders'], x['order_count']) if x['avg_days_between_orders'] > 0 else x['order_count'], axis=1
        )
        customer_metrics['customer_lifetime_value'] = (customer_metrics['predicted_lifetime_orders'] * customer_metrics['avg_order_value']).round(2)
        
        # Customer Segmentation
        def segment_customer(row):
            if row['recency_score'] >= 4 and row['frequency_score'] >= 4 and row['monetary_score'] >= 4:
                return 'Champions'
            elif row['recency_score'] >= 3 and row['frequency_score'] >= 3:
                return 'Loyal Customers'
            elif row['recency_score'] >= 4 and row['frequency_score'] <= 2:
                return 'New Customers'
            elif row['recency_score'] <= 2 and row['frequency_score'] >= 3:
                return 'At Risk'
            elif row['recency_score'] <= 2 and row['frequency_score'] <= 2:
                return 'Lost Customers'
            else:
                return 'Potential Loyalists'
                
        customer_metrics['customer_segment'] = customer_metrics.apply(segment_customer, axis=1)
        
        # Return rate
        customer_metrics['return_rate'] = (customer_metrics['total_returns'] / customer_metrics['order_count'] * 100).round(1)
        
        # Join with customer master data
        result = customers[['id', 'first_name', 'last_name', 'email', 'membership', 'age_group']].merge(
            customer_metrics, left_on='id', right_on='customer_id', how='left'
        )
        
        result['gold_processed_timestamp'] = datetime.now().isoformat()
        
        return result
        
    def _create_product_analytics(self):
        """Create product performance analytics"""
        products = self.silver_data['products']
        orders = self.silver_data['orders']
        
        # Product performance metrics
        product_metrics = orders.groupby('product_id').agg({
            'id': 'count',
            'quantity': 'sum',
            'total': 'sum',
            'customer_id': 'nunique',
            'is_returned': 'sum',
            'order_date': ['min', 'max']
        }).round(2)
        
        product_metrics.columns = [
            'total_orders', 'total_quantity_sold', 'total_revenue',
            'unique_customers', 'total_returns', 'first_sale_date', 'last_sale_date'
        ]
        product_metrics = product_metrics.reset_index()
        
        # Performance calculations
        product_metrics['avg_quantity_per_order'] = (product_metrics['total_quantity_sold'] / product_metrics['total_orders']).round(2)
        product_metrics['avg_revenue_per_order'] = (product_metrics['total_revenue'] / product_metrics['total_orders']).round(2)
        product_metrics['return_rate'] = (product_metrics['total_returns'] / product_metrics['total_orders'] * 100).round(1)
        product_metrics['customer_repeat_rate'] = ((product_metrics['total_orders'] - product_metrics['unique_customers']) / product_metrics['unique_customers'] * 100).round(1)
        
        # Sales velocity (orders per day)
        product_metrics['days_on_sale'] = (product_metrics['last_sale_date'] - product_metrics['first_sale_date']).dt.days + 1
        product_metrics['sales_velocity'] = (product_metrics['total_orders'] / product_metrics['days_on_sale']).round(3)
        
        # Join with product master data
        result = products[['id', 'product_name', 'price', 'category', 'brand', 'price_tier']].merge(
            product_metrics, left_on='id', right_on='product_id', how='left'
        )
        
        # Performance ranking
        result['revenue_rank'] = result['total_revenue'].rank(ascending=False, method='dense')
        result['quantity_rank'] = result['total_quantity_sold'].rank(ascending=False, method='dense')
        result['popularity_rank'] = result['total_orders'].rank(ascending=False, method='dense')
        
        # Performance categories
        result['performance_category'] = pd.cut(
            result['revenue_rank'], 
            bins=[0, 5, 10, 15, float('inf')], 
            labels=['Top Performer', 'Good Performer', 'Average Performer', 'Poor Performer']
        )
        
        result['gold_processed_timestamp'] = datetime.now().isoformat()
        
        return result
        
    def _create_sales_analytics(self):
        """Create sales performance analytics by various dimensions"""
        orders = self.silver_data['orders']
        
        # Monthly sales analytics
        monthly_sales = orders.groupby(['order_year', 'order_month']).agg({
            'total': ['sum', 'count', 'mean'],
            'customer_id': 'nunique',
            'product_id': 'nunique',
            'quantity': 'sum',
            'is_returned': 'sum'
        }).round(2)
        
        monthly_sales.columns = [
            'total_revenue', 'total_orders', 'avg_order_value',
            'unique_customers', 'unique_products', 'total_items', 'total_returns'
        ]
        monthly_sales = monthly_sales.reset_index()
        monthly_sales['year_month'] = monthly_sales['order_year'].astype(str) + '-' + monthly_sales['order_month'].astype(str).str.zfill(2)
        
        # Growth calculations
        monthly_sales = monthly_sales.sort_values(['order_year', 'order_month'])
        monthly_sales['revenue_growth'] = monthly_sales['total_revenue'].pct_change() * 100
        monthly_sales['order_growth'] = monthly_sales['total_orders'].pct_change() * 100
        monthly_sales['customer_growth'] = monthly_sales['unique_customers'].pct_change() * 100
        
        # Category performance
        category_sales = orders.groupby('category').agg({
            'total': ['sum', 'count', 'mean'],
            'customer_id': 'nunique',
            'quantity': 'sum'
        }).round(2)
        
        category_sales.columns = ['total_revenue', 'total_orders', 'avg_order_value', 'unique_customers', 'total_items']
        category_sales = category_sales.reset_index()
        category_sales['revenue_share'] = (category_sales['total_revenue'] / category_sales['total_revenue'].sum() * 100).round(1)
        
        # Customer segment performance
        segment_sales = orders.groupby('customer_segment').agg({
            'total': ['sum', 'count', 'mean'],
            'customer_id': 'nunique'
        }).round(2)
        
        segment_sales.columns = ['total_revenue', 'total_orders', 'avg_order_value', 'unique_customers']
        segment_sales = segment_sales.reset_index()
        
        result = {
            'monthly_sales': monthly_sales,
            'category_performance': category_sales,
            'customer_segment_performance': segment_sales
        }
        
        return result
        
    def _create_cross_sell_analytics(self):
        """Create cross-selling and market basket analytics"""
        orders = self.silver_data['orders']
        
        # Products frequently bought together
        # Group by customer and order date to find items in same transaction
        basket_analysis = orders.groupby(['customer_id', 'order_date'])['product_id'].apply(list).reset_index()
        basket_analysis = basket_analysis[basket_analysis['product_id'].apply(len) > 1]  # Only multi-item baskets
        
        # Create product pairs
        from itertools import combinations
        product_pairs = []
        for basket in basket_analysis['product_id']:
            for pair in combinations(sorted(basket), 2):
                product_pairs.append(pair)
        
        if product_pairs:
            pairs_df = pd.DataFrame(product_pairs, columns=['product_a', 'product_b'])
            pair_counts = pairs_df.groupby(['product_a', 'product_b']).size().reset_index(name='frequency')
            pair_counts = pair_counts.sort_values('frequency', ascending=False)
            
            # Add product names
            products = self.silver_data['products'][['id', 'product_name', 'category']]
            pair_counts = pair_counts.merge(products, left_on='product_a', right_on='id', suffixes=['', '_a'])
            pair_counts = pair_counts.merge(products, left_on='product_b', right_on='id', suffixes=['_a', '_b'])
            
            # Calculate confidence (A -> B) and lift
            product_sales = orders.groupby('product_id').size()
            pair_counts['product_a_sales'] = pair_counts['product_a'].map(product_sales)
            pair_counts['product_b_sales'] = pair_counts['product_b'].map(product_sales)
            
            total_transactions = len(basket_analysis)
            pair_counts['support'] = pair_counts['frequency'] / total_transactions
            pair_counts['confidence_a_to_b'] = pair_counts['frequency'] / pair_counts['product_a_sales']
            pair_counts['confidence_b_to_a'] = pair_counts['frequency'] / pair_counts['product_b_sales']
            
            return pair_counts.head(20)  # Top 20 pairs
        else:
            return pd.DataFrame()  # Empty if no multi-item baskets
            
    def _create_time_series_analytics(self):
        """Create time series analytics for forecasting"""
        orders = self.silver_data['orders']
        
        # Daily sales aggregation
        daily_sales = orders.groupby('order_date').agg({
            'total': 'sum',
            'id': 'count',
            'customer_id': 'nunique'
        }).round(2)
        
        daily_sales.columns = ['daily_revenue', 'daily_orders', 'daily_customers']
        daily_sales = daily_sales.reset_index()
        
        # Add time features
        daily_sales['day_of_week'] = daily_sales['order_date'].dt.day_name()
        daily_sales['day_of_month'] = daily_sales['order_date'].dt.day
        daily_sales['month'] = daily_sales['order_date'].dt.month
        daily_sales['quarter'] = daily_sales['order_date'].dt.quarter
        daily_sales['is_weekend'] = daily_sales['order_date'].dt.weekday >= 5
        daily_sales['is_month_start'] = daily_sales['order_date'].dt.day <= 7
        daily_sales['is_month_end'] = daily_sales['order_date'].dt.day >= 25
        
        # Moving averages
        daily_sales['revenue_7day_ma'] = daily_sales['daily_revenue'].rolling(window=7, min_periods=1).mean().round(2)
        daily_sales['revenue_30day_ma'] = daily_sales['daily_revenue'].rolling(window=30, min_periods=1).mean().round(2)
        
        # Growth rates
        daily_sales['revenue_day_over_day'] = daily_sales['daily_revenue'].pct_change() * 100
        daily_sales['orders_day_over_day'] = daily_sales['daily_orders'].pct_change() * 100
        
        return daily_sales
        
    def save_all_layers(self, output_directory='fabric_data_output'):
        """Save all Bronze, Silver, and Gold data"""
        import os
        
        # Create output directories
        for layer in ['bronze', 'silver', 'gold']:
            os.makedirs(f"{output_directory}/{layer}", exist_ok=True)
            
        # Save Bronze layer
        for table_name, df in self.bronze_data.items():
            df.to_parquet(f"{output_directory}/bronze/{table_name}.parquet", index=False)
            df.to_csv(f"{output_directory}/bronze/{table_name}.csv", index=False)
            
        # Save Silver layer
        for table_name, df in self.silver_data.items():
            df.to_parquet(f"{output_directory}/silver/{table_name}.parquet", index=False)
            df.to_csv(f"{output_directory}/silver/{table_name}.csv", index=False)
            
        # Save Gold layer
        for table_name, df in self.gold_data.items():
            if isinstance(df, dict):
                # Handle nested dictionaries (like sales_analytics)
                for sub_table, sub_df in df.items():
                    sub_df.to_parquet(f"{output_directory}/gold/{table_name}_{sub_table}.parquet", index=False)
                    sub_df.to_csv(f"{output_directory}/gold/{table_name}_{sub_table}.csv", index=False)
            else:
                df.to_parquet(f"{output_directory}/gold/{table_name}.parquet", index=False)
                df.to_csv(f"{output_directory}/gold/{table_name}.csv", index=False)
                
        print(f"✅ All data layers saved to {output_directory}/")
        
        # Create pipeline documentation
        self._create_pipeline_documentation(output_directory)
        
    def _create_pipeline_documentation(self, output_directory):
        """Create documentation for the data pipeline"""
        documentation = {
            "pipeline_overview": {
                "name": "Microsoft Fabric Retail Data Pipeline",
                "architecture": "Bronze-Silver-Gold Medallion",
                "description": "End-to-end data pipeline for retail analytics",
                "processed_timestamp": datetime.now().isoformat()
            },
            "bronze_layer": {
                "description": "Raw data ingestion with minimal processing",
                "tables": list(self.bronze_data.keys()),
                "transformations": [
                    "Added ingestion timestamps",
                    "Added source file metadata",
                    "Added record identifiers"
                ]
            },
            "silver_layer": {
                "description": "Cleaned and standardized data",
                "tables": list(self.silver_data.keys()),
                "transformations": [
                    "Data type conversions",
                    "Data standardization",
                    "Address parsing", 
                    "Data quality scoring",
                    "Business rule validation",
                    "Cross-table integrity checks"
                ]
            },
            "gold_layer": {
                "description": "Business-ready analytics tables",
                "tables": list(self.gold_data.keys()),
                "analytics": [
                    "Customer RFM analysis",
                    "Customer lifetime value",
                    "Product performance metrics",
                    "Sales trend analysis",
                    "Cross-selling analytics",
                    "Time series forecasting data"
                ]
            },
            "business_value": {
                "customer_insights": "RFM segmentation, CLV, churn risk",
                "product_insights": "Performance ranking, cross-sell opportunities",
                "sales_insights": "Trend analysis, growth metrics, forecasting",
                "operational_insights": "Data quality monitoring, pipeline health"
            }
        }
        
        with open(f"{output_directory}/pipeline_documentation.json", 'w') as f:
            json.dump(documentation, f, indent=2)
            
        print(f"✅ Pipeline documentation saved to {output_directory}/pipeline_documentation.json")

if __name__ == "__main__":
    # Initialize pipeline
    pipeline = FabricRetailDataPipeline()
    
    # Run Bronze -> Silver -> Gold transformations
    if pipeline.ingest_bronze_data("infra/data"):
        pipeline.transform_to_silver()
        pipeline.transform_to_gold()
        pipeline.save_all_layers()
        
        print("\n🎯 Microsoft Fabric Retail Data Pipeline Complete!")
        print("\nOutput includes:")
        print("📊 Bronze layer: Raw data with ingestion metadata") 
        print("🔧 Silver layer: Cleaned and standardized data")
        print("💎 Gold layer: Business-ready analytics tables")
        print("📚 Pipeline documentation and data lineage")
