"""
Fabric Retail Sample Data Generator
Generates enhanced sample data for Microsoft Fabric lakehouse implementation
Following retail industry data model patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import uuid

fake = Faker()

class FabricRetailDataGenerator:
    def __init__(self):
        self.customers_df = None
        self.products_df = None
        self.orders_df = None
        
    def load_existing_data(self):
        """Load existing sample data as base"""
        try:
            self.customers_df = pd.read_csv('infra/data/customers.csv')
            self.products_df = pd.read_csv('infra/data/products.csv')
            self.orders_df = pd.read_csv('infra/data/orders.csv')
            print("✅ Existing data loaded successfully")
        except Exception as e:
            print(f"❌ Error loading existing data: {e}")
            
    def enhance_customers_for_fabric(self):
        """Enhance customer data with Fabric retail model fields"""
        if self.customers_df is None:
            return
            
        # Add Fabric retail industry model fields
        enhanced_customers = self.customers_df.copy()
        
        # Add customer insights fields
        enhanced_customers['customer_key'] = enhanced_customers['id'].apply(lambda x: f"CUST_{x:06d}")
        enhanced_customers['registration_date'] = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365, len(enhanced_customers)), unit='D')
        enhanced_customers['preferred_contact_method'] = np.random.choice(['email', 'phone', 'sms'], len(enhanced_customers))
        enhanced_customers['marketing_consent'] = np.random.choice([True, False], len(enhanced_customers), p=[0.7, 0.3])
        enhanced_customers['loyalty_points'] = np.random.randint(0, 5000, len(enhanced_customers))
        enhanced_customers['customer_segment'] = enhanced_customers['membership'].map({
            'Base': 'Standard',
            'Gold': 'Premium', 
            'Platinum': 'VIP'
        })
        
        # Add geographic and demographic enrichment
        enhanced_customers['city'] = enhanced_customers['post_address'].str.extract(r', ([^,]+),')[0]
        enhanced_customers['state'] = enhanced_customers['post_address'].str.extract(r', ([A-Z]{2}) ')[0]
        enhanced_customers['postal_code'] = enhanced_customers['post_address'].str.extract(r' (\d{5})')[0]
        enhanced_customers['customer_lifetime_value'] = np.random.uniform(100, 5000, len(enhanced_customers)).round(2)
        
        # Add temporal fields for analytics
        enhanced_customers['created_date'] = datetime.now().isoformat()
        enhanced_customers['modified_date'] = datetime.now().isoformat()
        enhanced_customers['is_active'] = np.random.choice([True, False], len(enhanced_customers), p=[0.85, 0.15])
        
        return enhanced_customers
        
    def enhance_products_for_fabric(self):
        """Enhance product data with Fabric retail model fields"""
        if self.products_df is None:
            return
            
        enhanced_products = self.products_df.copy()
        
        # Add Fabric retail industry model fields
        enhanced_products['product_key'] = enhanced_products['id'].apply(lambda x: f"PROD_{x:06d}")
        enhanced_products['sku'] = enhanced_products['id'].apply(lambda x: f"SKU{x:06d}")
        enhanced_products['barcode'] = enhanced_products['id'].apply(lambda x: f"{random.randint(100000000000, 999999999999)}")
        enhanced_products['cost_price'] = (enhanced_products['price'] * np.random.uniform(0.4, 0.7, len(enhanced_products))).round(2)
        enhanced_products['margin_percent'] = ((enhanced_products['price'] - enhanced_products['cost_price']) / enhanced_products['price'] * 100).round(2)
        
        # Inventory and operational fields
        enhanced_products['stock_quantity'] = np.random.randint(0, 500, len(enhanced_products))
        enhanced_products['reorder_level'] = np.random.randint(10, 50, len(enhanced_products))
        enhanced_products['supplier_id'] = np.random.randint(1, 10, len(enhanced_products))
        enhanced_products['weight_kg'] = np.random.uniform(0.1, 10.0, len(enhanced_products)).round(2)
        enhanced_products['length_cm'] = np.random.uniform(5, 100, len(enhanced_products)).round(1)
        enhanced_products['width_cm'] = np.random.uniform(5, 50, len(enhanced_products)).round(1)
        enhanced_products['height_cm'] = np.random.uniform(5, 30, len(enhanced_products)).round(1)
        
        # Product lifecycle fields
        enhanced_products['launch_date'] = pd.to_datetime('2022-01-01') + pd.to_timedelta(np.random.randint(0, 730, len(enhanced_products)), unit='D')
        enhanced_products['is_active'] = np.random.choice([True, False], len(enhanced_products), p=[0.9, 0.1])
        enhanced_products['seasonal_indicator'] = np.random.choice(['Spring', 'Summer', 'Fall', 'Winter', 'All Season'], len(enhanced_products))
        
        # Rating and review fields for analytics
        enhanced_products['avg_rating'] = np.random.uniform(3.0, 5.0, len(enhanced_products)).round(1)
        enhanced_products['review_count'] = np.random.randint(0, 500, len(enhanced_products))
        
        # Temporal audit fields
        enhanced_products['created_date'] = datetime.now().isoformat()
        enhanced_products['modified_date'] = datetime.now().isoformat()
        
        return enhanced_products
        
    def enhance_orders_for_fabric(self):
        """Enhance order data with Fabric retail model fields"""
        if self.orders_df is None:
            return
            
        enhanced_orders = self.orders_df.copy()
        
        # Add Fabric retail industry model fields
        enhanced_orders['order_key'] = enhanced_orders['id'].apply(lambda x: f"ORD_{x:08d}")
        enhanced_orders['order_number'] = enhanced_orders['id'].apply(lambda x: f"ON{x:08d}")
        enhanced_orders['order_datetime'] = pd.to_datetime(enhanced_orders['order_date'])
        enhanced_orders['order_status'] = np.random.choice(['Completed', 'Shipped', 'Processing', 'Cancelled'], len(enhanced_orders), p=[0.7, 0.2, 0.08, 0.02])
        
        # Financial fields
        enhanced_orders['tax_amount'] = (enhanced_orders['total'].astype(float) * 0.08).round(2)
        enhanced_orders['shipping_cost'] = np.random.choice([0, 5.99, 9.99, 15.99], len(enhanced_orders), p=[0.3, 0.4, 0.2, 0.1])
        enhanced_orders['discount_amount'] = np.random.choice([0, 10, 25, 50], len(enhanced_orders), p=[0.6, 0.2, 0.15, 0.05])
        enhanced_orders['order_total'] = (enhanced_orders['total'].astype(float) + enhanced_orders['tax_amount'] + enhanced_orders['shipping_cost'] - enhanced_orders['discount_amount']).round(2)
        
        # Channel and fulfillment
        enhanced_orders['sales_channel'] = np.random.choice(['Online', 'In-Store', 'Mobile App', 'Phone'], len(enhanced_orders), p=[0.5, 0.3, 0.15, 0.05])
        enhanced_orders['fulfillment_method'] = np.random.choice(['Ship to Home', 'Store Pickup', 'Curbside'], len(enhanced_orders), p=[0.7, 0.2, 0.1])
        enhanced_orders['payment_method'] = np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash'], len(enhanced_orders), p=[0.5, 0.2, 0.2, 0.1])
        
        # Geographic and timing
        enhanced_orders['store_id'] = np.random.randint(1, 20, len(enhanced_orders))
        enhanced_orders['region'] = np.random.choice(['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West'], len(enhanced_orders))
        enhanced_orders['order_hour'] = pd.to_datetime(enhanced_orders['order_date']).dt.hour
        enhanced_orders['order_day_of_week'] = pd.to_datetime(enhanced_orders['order_date']).dt.day_name()
        enhanced_orders['order_month'] = pd.to_datetime(enhanced_orders['order_date']).dt.month
        enhanced_orders['order_quarter'] = pd.to_datetime(enhanced_orders['order_date']).dt.quarter
        enhanced_orders['order_year'] = pd.to_datetime(enhanced_orders['order_date']).dt.year
        
        # Customer analytics fields
        enhanced_orders['is_first_order'] = np.random.choice([True, False], len(enhanced_orders), p=[0.2, 0.8])
        enhanced_orders['customer_segment_at_order'] = enhanced_orders['customer_gender'].map({'Male': 'M', 'Female': 'F'}) + '_' + pd.cut(enhanced_orders['customer_age'], bins=[0, 25, 35, 50, 100], labels=['Young', 'Adult', 'MiddleAge', 'Senior']).astype(str)
        
        # Temporal audit fields
        enhanced_orders['created_date'] = datetime.now().isoformat()
        enhanced_orders['modified_date'] = datetime.now().isoformat()
        
        return enhanced_orders
        
    def generate_additional_sample_data(self, scale_factor=2):
        """Generate additional sample data based on existing patterns"""
        if self.customers_df is None:
            print("❌ Load existing data first")
            return
            
        # Generate additional customers
        additional_customers = []
        base_customer_count = len(self.customers_df)
        
        for i in range(scale_factor * base_customer_count):
            customer = {
                'id': base_customer_count + i + 1,
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'gender': random.choice(['Male', 'Female']),
                'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%-m/%-d/%Y'),
                'age': random.randint(18, 80),
                'email': fake.email(),
                'phone': fake.phone_number()[:14],
                'post_address': f"{random.randint(100, 9999)} {fake.street_name()}, {fake.city()}, {fake.state_abbr()} {fake.zipcode()}",
                'membership': random.choice(['Base', 'Gold', 'Platinum'])
            }
            customer['age'] = 2024 - int(customer['date_of_birth'].split('/')[-1])
            additional_customers.append(customer)
            
        return pd.DataFrame(additional_customers)
        
    def create_analytics_tables(self):
        """Create pre-aggregated analytics tables for Gold layer"""
        analytics_tables = {}
        
        if self.customers_df is not None and self.orders_df is not None:
            # Customer Analytics
            customer_analytics = self.orders_df.groupby('customer_id').agg({
                'total': ['count', 'sum', 'mean'],
                'order_date': ['min', 'max']
            }).round(2)
            customer_analytics.columns = ['order_count', 'total_spent', 'avg_order_value', 'first_order_date', 'last_order_date']
            customer_analytics = customer_analytics.reset_index()
            analytics_tables['customer_analytics'] = customer_analytics
            
            # Product Analytics
            if self.products_df is not None:
                product_analytics = self.orders_df.groupby('product_id').agg({
                    'quantity': 'sum',
                    'total': 'sum',
                    'id': 'count'
                }).round(2)
                product_analytics.columns = ['total_quantity_sold', 'total_revenue', 'total_orders']
                product_analytics = product_analytics.reset_index()
                analytics_tables['product_analytics'] = product_analytics
                
            # Monthly Sales Analytics
            monthly_sales = self.orders_df.copy()
            monthly_sales['order_date'] = pd.to_datetime(monthly_sales['order_date'])
            monthly_sales['year_month'] = monthly_sales['order_date'].dt.to_period('M')
            monthly_analytics = monthly_sales.groupby('year_month').agg({
                'total': 'sum',
                'id': 'count',
                'customer_id': 'nunique'
            }).round(2)
            monthly_analytics.columns = ['total_revenue', 'total_orders', 'unique_customers']
            monthly_analytics = monthly_analytics.reset_index()
            monthly_analytics['year_month'] = monthly_analytics['year_month'].astype(str)
            analytics_tables['monthly_sales_analytics'] = monthly_analytics
            
        return analytics_tables
        
    def save_enhanced_data(self, output_dir='fabric_enhanced_data'):
        """Save all enhanced data for Fabric ingestion"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Enhanced core tables
        enhanced_customers = self.enhance_customers_for_fabric()
        enhanced_products = self.enhance_products_for_fabric()
        enhanced_orders = self.enhance_orders_for_fabric()
        
        if enhanced_customers is not None:
            enhanced_customers.to_csv(f'{output_dir}/customers_enhanced.csv', index=False)
            enhanced_customers.to_parquet(f'{output_dir}/customers_enhanced.parquet', index=False)
            
        if enhanced_products is not None:
            enhanced_products.to_csv(f'{output_dir}/products_enhanced.csv', index=False)
            enhanced_products.to_parquet(f'{output_dir}/products_enhanced.parquet', index=False)
            
        if enhanced_orders is not None:
            enhanced_orders.to_csv(f'{output_dir}/orders_enhanced.csv', index=False)
            enhanced_orders.to_parquet(f'{output_dir}/orders_enhanced.parquet', index=False)
            
        # Analytics tables
        analytics_tables = self.create_analytics_tables()
        for table_name, df in analytics_tables.items():
            df.to_csv(f'{output_dir}/{table_name}.csv', index=False)
            df.to_parquet(f'{output_dir}/{table_name}.parquet', index=False)
            
        # Additional sample data
        additional_customers = self.generate_additional_sample_data()
        if additional_customers is not None:
            additional_customers.to_csv(f'{output_dir}/additional_customers.csv', index=False)
            
        print(f"✅ Enhanced data saved to {output_dir}/")
        
        # Create data dictionary
        self.create_data_dictionary(output_dir)
        
    def create_data_dictionary(self, output_dir):
        """Create data dictionary for Fabric implementation"""
        data_dictionary = {
            'customers_enhanced': {
                'description': 'Enhanced customer master data with Fabric retail industry model fields',
                'key_fields': ['customer_key', 'id'],
                'business_purpose': 'Customer analytics, segmentation, personalization'
            },
            'products_enhanced': {
                'description': 'Enhanced product master data with inventory and operational fields',
                'key_fields': ['product_key', 'sku', 'id'],
                'business_purpose': 'Product analytics, inventory management, pricing optimization'
            },
            'orders_enhanced': {
                'description': 'Enhanced transaction data with channel, fulfillment, and analytics fields',
                'key_fields': ['order_key', 'order_number', 'id'],
                'business_purpose': 'Sales analytics, customer journey analysis, operational reporting'
            },
            'customer_analytics': {
                'description': 'Pre-aggregated customer behavior metrics',
                'key_fields': ['customer_id'],
                'business_purpose': 'Customer lifetime value, RFM analysis, churn prediction'
            },
            'product_analytics': {
                'description': 'Pre-aggregated product performance metrics',
                'key_fields': ['product_id'],
                'business_purpose': 'Product performance, inventory planning, merchandising'
            },
            'monthly_sales_analytics': {
                'description': 'Time-series sales performance metrics',
                'key_fields': ['year_month'],
                'business_purpose': 'Trend analysis, forecasting, executive reporting'
            }
        }
        
        import json
        with open(f'{output_dir}/data_dictionary.json', 'w') as f:
            json.dump(data_dictionary, f, indent=2)
            
        print(f"✅ Data dictionary saved to {output_dir}/data_dictionary.json")

if __name__ == "__main__":
    # Initialize generator
    generator = FabricRetailDataGenerator()
    
    # Load existing data
    generator.load_existing_data()
    
    # Generate enhanced data for Fabric
    generator.save_enhanced_data()
    
    print("\n🎯 Fabric Retail Data Generation Complete!")
    print("\nNext Steps:")
    print("1. Upload data to Fabric Lakehouse Bronze layer")
    print("2. Create data pipelines for Silver layer transformations")
    print("3. Build Gold layer analytics tables")
    print("4. Implement Fabric retail industry data model patterns")
