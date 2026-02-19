"""
DuckDB Data Warehouse Builder
Creates star schema for hospital analytics
"""

import duckdb
import pandas as pd
import os


class WarehouseBuilder:
    """Builds DuckDB data warehouse with star schema"""
    
    def __init__(self, db_path='backend/data/hospital_warehouse.db'):
        """
        Initialize warehouse builder
        
        Args:
            db_path: Path to DuckDB database file
        """
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to DuckDB database"""
        self.conn = duckdb.connect(self.db_path)
        print(f"✅ Connected to DuckDB at {self.db_path}")
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")
    
    def create_dimension_tables(self, df_patients, df_visits):
        """Create dimension tables for star schema"""
        print("\n🔄 Creating dimension tables...")
        
        # Dimension: Patient
        dim_patient = df_patients[[
            'patient_id', 'age', 'gender', 'bmi', 
            'smoking_status', 'chronic_conditions', 
            'chronic_condition_count', 'registration_date'
        ]].copy()
        
        self.conn.execute("DROP TABLE IF EXISTS dim_patient")
        self.conn.register('dim_patient_temp', dim_patient)
        self.conn.execute("CREATE TABLE dim_patient AS SELECT * FROM dim_patient_temp")
        print(f"  ✅ dim_patient: {len(dim_patient):,} records")
        
        # Dimension: Department
        departments = df_visits['department'].unique()
        dim_department = pd.DataFrame({
            'department_id': range(1, len(departments) + 1),
            'department_name': sorted(departments)
        })
        
        self.conn.execute("DROP TABLE IF EXISTS dim_department")
        self.conn.register('dim_department_temp', dim_department)
        self.conn.execute("CREATE TABLE dim_department AS SELECT * FROM dim_department_temp")
        print(f"  ✅ dim_department: {len(dim_department):,} records")
        
        # Dimension: Date
        dates = pd.date_range(
            start=df_visits['visit_date'].min(),
            end=df_visits['visit_date'].max(),
            freq='D'
        )
        
        dim_date = pd.DataFrame({
            'date_id': range(1, len(dates) + 1),
            'full_date': dates,
            'year': dates.year,
            'month': dates.month,
            'day': dates.day,
            'quarter': dates.quarter,
            'day_of_week': dates.dayofweek,
            'day_name': dates.day_name(),
            'month_name': dates.month_name(),
            'is_weekend': dates.dayofweek.isin([5, 6]).astype(int)
        })
        
        self.conn.execute("DROP TABLE IF EXISTS dim_date")
        self.conn.register('dim_date_temp', dim_date)
        self.conn.execute("CREATE TABLE dim_date AS SELECT * FROM dim_date_temp")
        print(f"  ✅ dim_date: {len(dim_date):,} records")
        
        return dim_patient, dim_department, dim_date
    
    def create_fact_table(self, df_visits, dim_department, dim_date):
        """Create fact table for visits"""
        print("\n🔄 Creating fact table...")
        
        # Prepare fact table
        fact_visits = df_visits.copy()
        
        # Add department_id
        dept_mapping = dict(zip(dim_department['department_name'], dim_department['department_id']))
        fact_visits['department_id'] = fact_visits['department'].map(dept_mapping)
        
        # Add date_id
        date_mapping = dict(zip(
            dim_date['full_date'].dt.date, 
            dim_date['date_id']
        ))
        fact_visits['date_id'] = fact_visits['visit_date'].dt.date.map(date_mapping)
        
        # Select relevant columns
        fact_visits = fact_visits[[
            'visit_id', 'patient_id', 'date_id', 'department_id',
            'visit_type', 'wait_time_minutes', 'is_admitted',
            'length_of_stay_days', 'readmitted_30d_flag', 'satisfaction_score'
        ]]
        
        self.conn.execute("DROP TABLE IF EXISTS fact_visits")
        self.conn.register('fact_visits_temp', fact_visits)
        self.conn.execute("CREATE TABLE fact_visits AS SELECT * FROM fact_visits_temp")
        print(f"  ✅ fact_visits: {len(fact_visits):,} records")
        
        return fact_visits
    
    def create_indexes(self):
        """Create indexes for performance optimization"""
        print("\n🔄 Creating indexes...")
        
        # Index on fact table
        self.conn.execute("CREATE INDEX idx_fact_patient ON fact_visits(patient_id)")
        self.conn.execute("CREATE INDEX idx_fact_date ON fact_visits(date_id)")
        self.conn.execute("CREATE INDEX idx_fact_dept ON fact_visits(department_id)")
        
        print("  ✅ Indexes created")
    
    def build_warehouse(self, df_patients, df_visits):
        """Build complete data warehouse"""
        print("\n" + "="*60)
        print("🏗️  BUILDING DATA WAREHOUSE")
        print("="*60)
        
        self.connect()
        
        # Create schema
        dim_patient, dim_department, dim_date = self.create_dimension_tables(df_patients, df_visits)
        fact_visits = self.create_fact_table(df_visits, dim_department, dim_date)
        
        # Create indexes
        self.create_indexes()
        
        print("\n" + "="*60)
        print("✅ DATA WAREHOUSE BUILD COMPLETE")
        print("="*60)
        
        # Show summary
        print("\n📊 Warehouse Summary:")
        print(f"  • dim_patient: {len(dim_patient):,} records")
        print(f"  • dim_department: {len(dim_department):,} records")
        print(f"  • dim_date: {len(dim_date):,} records")
        print(f"  • fact_visits: {len(fact_visits):,} records")
        print(f"\n📁 Database: {self.db_path}\n")
        
        return self.conn
    
    def run_sample_queries(self):
        """Run sample analytical queries"""
        print("\n" + "="*60)
        print("📊 SAMPLE ANALYTICAL QUERIES")
        print("="*60 + "\n")
        
        # Query 1: Department statistics
        print("1️⃣ Department Statistics:")
        result = self.conn.execute("""
            SELECT 
                dd.department_name,
                COUNT(*) as total_visits,
                AVG(fv.wait_time_minutes) as avg_wait_time,
                SUM(fv.is_admitted) as total_admissions
            FROM fact_visits fv
            JOIN dim_department dd ON fv.department_id = dd.department_id
            GROUP BY dd.department_name
            ORDER BY total_visits DESC
            LIMIT 5
        """).df()
        print(result.to_string(index=False))
        
        # Query 2: Monthly trends
        print("\n2️⃣ Monthly Visit Trends:")
        result = self.conn.execute("""
            SELECT 
                d.year,
                d.month,
                d.month_name,
                COUNT(*) as total_visits,
                AVG(fv.satisfaction_score) as avg_satisfaction
            FROM fact_visits fv
            JOIN dim_date d ON fv.date_id = d.date_id
            GROUP BY d.year, d.month, d.month_name
            ORDER BY d.year DESC, d.month DESC
            LIMIT 6
        """).df()
        print(result.to_string(index=False))
        
        # Query 3: High-risk patients
        print("\n3️⃣ High-Risk Patients (Multiple Chronic Conditions):")
        result = self.conn.execute("""
            SELECT 
                dp.patient_id,
                dp.age,
                dp.chronic_condition_count,
                COUNT(fv.visit_id) as visit_count,
                SUM(fv.is_admitted) as admission_count
            FROM dim_patient dp
            JOIN fact_visits fv ON dp.patient_id = fv.patient_id
            WHERE dp.chronic_condition_count >= 2
            GROUP BY dp.patient_id, dp.age, dp.chronic_condition_count
            ORDER BY visit_count DESC
            LIMIT 5
        """).df()
        print(result.to_string(index=False))
        print()


if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from analytics.data_loader import DataLoader
    
    # Load processed data
    loader = DataLoader(data_dir='backend/data/processed')
    patients, visits, admissions = loader.load_all()
    
    # Build warehouse
    warehouse = WarehouseBuilder()
    warehouse.build_warehouse(patients, visits)
    
    # Run sample queries
    warehouse.run_sample_queries()
    
    warehouse.close()
