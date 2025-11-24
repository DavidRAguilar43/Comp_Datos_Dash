"""
Test script to verify filter functionality.

This script tests the apply_filters method with different filter combinations
to identify which filters are causing issues.
"""

import sys
import os
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.data_processor import DataProcessor

def test_filters():
    """Test all filters with the CubanDataset."""
    
    # Load the dataset
    processor = DataProcessor()
    
    # Load CSV file (it's in the root of ProyectoFinal, not in Comp_Datos_Dash)
    csv_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'CubanDataset.csv')
    
    with open(csv_path, 'rb') as f:
        file_bytes = f.read()
    
    result = processor.load_from_bytes(file_bytes, 'CubanDataset.csv')
    print(f"✅ Loaded {result['rows']} records")
    
    # Clean data
    clean_result = processor.clean_data()
    print(f"✅ Data cleaned: {len(processor.df)} records remaining")
    
    # Check unique values for problematic columns
    print("\n" + "="*60)
    print("COLUMN VALUES ANALYSIS")
    print("="*60)
    
    print("\n1. CANCER column:")
    print(f"   Unique values: {processor.df['cancer'].unique()}")
    print(f"   Value counts:\n{processor.df['cancer'].value_counts()}")
    
    print("\n2. MENOPAUSE column:")
    print(f"   Data type: {processor.df['menopause'].dtype}")
    print(f"   Unique values (first 20): {processor.df['menopause'].unique()[:20]}")
    print(f"   Value counts (top 10):\n{processor.df['menopause'].value_counts().head(10)}")
    
    print("\n3. BIRADS column:")
    print(f"   Data type: {processor.df['birads'].dtype}")
    print(f"   Unique values: {sorted(processor.df['birads'].unique())}")
    print(f"   Value counts:\n{processor.df['birads'].value_counts()}")
    
    print("\n4. BREASTFEEDING column:")
    print(f"   Data type: {processor.df['breastfeeding'].dtype}")
    print(f"   Unique values: {processor.df['breastfeeding'].unique()}")
    print(f"   Value counts:\n{processor.df['breastfeeding'].value_counts()}")
    
    # Test each filter individually
    print("\n" + "="*60)
    print("TESTING FILTERS INDIVIDUALLY")
    print("="*60)
    
    # Test 1: Diagnosis filter - Benigno
    print("\n📊 Test 1: Diagnosis = Benigno")
    filters = {'diagnosis': 'Benigno'}
    filtered_df = processor.apply_filters(filters)
    print(f"   Result: {len(filtered_df)} records")
    
    # Test 2: Diagnosis filter - Maligno
    print("\n📊 Test 2: Diagnosis = Maligno")
    filters = {'diagnosis': 'Maligno'}
    filtered_df = processor.apply_filters(filters)
    print(f"   Result: {len(filtered_df)} records")
    
    # Test 3: Menopause filter - Premenopáusica
    print("\n📊 Test 3: Menopause = Premenopáusica")
    filters = {'menopause': 'Premenopáusica'}
    filtered_df = processor.apply_filters(filters)
    print(f"   Result: {len(filtered_df)} records")
    
    # Test 4: Menopause filter - Posmenopáusica
    print("\n📊 Test 4: Menopause = Posmenopáusica")
    filters = {'menopause': 'Posmenopáusica'}
    filtered_df = processor.apply_filters(filters)
    print(f"   Result: {len(filtered_df)} records")
    
    # Test 5: BIRADS filter - 3
    print("\n📊 Test 5: BIRADS = 3")
    filters = {'birads': '3'}
    filtered_df = processor.apply_filters(filters)
    print(f"   Result: {len(filtered_df)} records")
    
    # Test 6: BIRADS filter - 4
    print("\n📊 Test 6: BIRADS = 4")
    filters = {'birads': '4'}
    filtered_df = processor.apply_filters(filters)
    print(f"   Result: {len(filtered_df)} records")
    
    # Test 7: BIRADS filter - 5
    print("\n📊 Test 7: BIRADS = 5")
    filters = {'birads': '5'}
    filtered_df = processor.apply_filters(filters)
    print(f"   Result: {len(filtered_df)} records")
    
    # Test 8: Breastfeeding filter - Sí
    print("\n📊 Test 8: Breastfeeding = Sí")
    filters = {'breastfeeding': 'Sí'}
    filtered_df = processor.apply_filters(filters)
    print(f"   Result: {len(filtered_df)} records")
    
    # Test 9: Breastfeeding filter - No
    print("\n📊 Test 9: Breastfeeding = No")
    filters = {'breastfeeding': 'No'}
    filtered_df = processor.apply_filters(filters)
    print(f"   Result: {len(filtered_df)} records")
    
    # Test 10: Combined filters
    print("\n📊 Test 10: Combined - Diagnosis=Maligno + Menopause=Posmenopáusica")
    filters = {
        'diagnosis': 'Maligno',
        'menopause': 'Posmenopáusica'
    }
    filtered_df = processor.apply_filters(filters)
    print(f"   Result: {len(filtered_df)} records")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60)

if __name__ == "__main__":
    test_filters()

