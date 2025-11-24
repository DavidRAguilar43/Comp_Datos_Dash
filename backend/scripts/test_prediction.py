"""
Test script to verify prediction functionality.

Reason: Debug why predictions are returning the same result.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from services.data_processor import DataProcessor
from services.ml_models import MLModelsService

def main():
    print("="*60)
    print("PREDICTION DEBUGGING TEST")
    print("="*60)
    
    # Load dataset
    dataset_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'CubanDataset.csv')
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at: {dataset_path}")
        return
    
    print(f"\n1. Loading dataset from: {dataset_path}")
    with open(dataset_path, 'rb') as f:
        file_bytes = f.read()
    
    processor = DataProcessor()
    result = processor.load_from_bytes(file_bytes, 'CubanDataset.csv')
    print(f"✅ Loaded {result['rows']} records")
    
    # Clean data
    print("\n2. Cleaning data...")
    processor.clean_data()
    print(f"✅ Data cleaned: {len(processor.df)} records")
    
    # Check what columns are numeric
    print("\n3. Analyzing column types:")
    print(f"   Total columns: {len(processor.df.columns)}")
    numeric_cols = processor.df.select_dtypes(include=['number']).columns.tolist()
    print(f"   Numeric columns ({len(numeric_cols)}): {numeric_cols}")
    
    categorical_cols = processor.df.select_dtypes(exclude=['number']).columns.tolist()
    print(f"   Categorical columns ({len(categorical_cols)}): {categorical_cols}")
    
    # Prepare ML data
    print("\n4. Preparing data for ML...")
    ml_service = MLModelsService()
    prep_result = ml_service.prepare_data(processor.df)
    
    if not prep_result['success']:
        print(f"❌ Error preparing data: {prep_result['error']}")
        return
    
    print(f"✅ Data prepared")
    print(f"   Features used: {ml_service.feature_names}")
    print(f"   Number of features: {len(ml_service.feature_names)}")
    print(f"   Training samples: {len(ml_service.y_train)}")
    print(f"   Test samples: {len(ml_service.y_test)}")
    
    # Train Random Forest
    print("\n5. Training Random Forest model...")
    rf_result = ml_service.train_random_forest()
    
    if not rf_result['success']:
        print(f"❌ Error training model: {rf_result['error']}")
        return
    
    print(f"✅ Model trained")
    print(f"   Accuracy: {rf_result['test_metrics']['accuracy']:.4f}")
    
    # Test predictions with different inputs
    print("\n6. Testing predictions with different inputs:")
    print("="*60)
    
    test_cases = [
        {
            "name": "Low risk case",
            "data": {
                "age": 30,
                "menarche": 13,
                "menopause": 0,
                "agefirst": 25,
                "children": 1,
                "biopsies": 0,
                "imc": 22.0,
                "weight": 60.0,
                "histologicalclass": 1
            }
        },
        {
            "name": "High risk case",
            "data": {
                "age": 60,
                "menarche": 10,
                "menopause": 45,
                "agefirst": 0,
                "children": 0,
                "biopsies": 3,
                "imc": 32.0,
                "weight": 90.0,
                "histologicalclass": 5
            }
        },
        {
            "name": "Medium risk case",
            "data": {
                "age": 45,
                "menarche": 12,
                "menopause": 0,
                "agefirst": 28,
                "children": 2,
                "biopsies": 1,
                "imc": 25.0,
                "weight": 70.0,
                "histologicalclass": 3
            }
        },
        {
            "name": "Minimal data",
            "data": {
                "age": 40,
                "imc": 24.0
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print(f"Input: {test_case['data']}")
        
        result = ml_service.predict_single(test_case['data'], model_name='random_forest')
        
        if result['success']:
            print(f"✅ Prediction successful")
            print(f"   Probability: {result['probability_percentage']}%")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   Prediction: {'Cancer' if result['prediction'] == 1 else 'No Cancer'}")
            
            if 'debug_info' in result:
                print(f"   Features used: {result['debug_info']['features_used']}")
                print(f"   Scaled values: {result['debug_info']['scaled_values'][:5]}...")  # First 5
        else:
            print(f"❌ Prediction failed: {result['error']}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()

