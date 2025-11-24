"""
Test script for dynamic dataset analysis.

This script tests the DatasetStructureAnalyzer with different breast cancer datasets
to validate that it correctly identifies column types and recommends appropriate visualizations.

Usage:
    python scripts/test_dynamic_analysis.py <path_to_csv>
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Add parent directory to path to import services
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.dataset_structure_analyzer import DatasetStructureAnalyzer


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def test_dataset_analysis(csv_path):
    """
    Test dataset structure analysis.
    
    Args:
        csv_path (str): Path to CSV file to analyze
    """
    print_section("TESTING DYNAMIC DATASET ANALYSIS")
    
    # Check if file exists
    if not os.path.exists(csv_path):
        print(f"❌ Error: File not found: {csv_path}")
        return
    
    print(f"📁 Loading dataset: {csv_path}")
    
    # Load dataset
    try:
        df = pd.read_csv(csv_path)
        print(f"✅ Dataset loaded successfully")
        print(f"   - Rows: {len(df)}")
        print(f"   - Columns: {len(df.columns)}")
        print(f"   - Column names: {', '.join(df.columns.tolist())}")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return
    
    # Initialize analyzer
    print_section("INITIALIZING AI ANALYZER")
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("   Please set OPENAI_API_KEY before running this test")
        return
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    try:
        analyzer = DatasetStructureAnalyzer(api_key=api_key)
        print("✅ Analyzer initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing analyzer: {e}")
        return
    
    # Analyze dataset structure
    print_section("ANALYZING DATASET STRUCTURE")
    
    try:
        result = analyzer.analyze_dataset_structure(df)
        
        if not result.get("success"):
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            return
        
        print("✅ Analysis completed successfully")
        
        analysis = result["analysis"]
        
        # Print column analysis
        print_section("COLUMN ANALYSIS")
        print(f"\n{'Column Name':<30} {'Type':<20} {'Reason'}")
        print("-" * 80)
        
        for col_name, col_info in analysis["column_analysis"].items():
            col_type = col_info.get("type", "unknown")
            reason = col_info.get("reason", "No reason provided")[:40]
            print(f"{col_name:<30} {col_type:<20} {reason}")
        
        # Print key variables
        print_section("KEY VARIABLES")
        
        if "key_variables" in analysis:
            key_vars = analysis["key_variables"]
            
            if "target" in key_vars:
                print(f"\n🎯 Target Variable: {key_vars['target']}")
            
            if "predictors" in key_vars and key_vars["predictors"]:
                print(f"\n📊 Key Predictors:")
                for predictor in key_vars["predictors"]:
                    print(f"   - {predictor}")
        
        # Print recommended analyses
        print_section("RECOMMENDED ANALYSES")
        
        if "recommended_analyses" in analysis:
            for i, rec in enumerate(analysis["recommended_analyses"], 1):
                print(f"\n{i}. {rec.get('type', 'Unknown').upper()}")
                print(f"   Variables: {', '.join(rec.get('variables', []))}")
                print(f"   Reason: {rec.get('reason', 'No reason provided')}")
        
        # Print data quality notes
        print_section("DATA QUALITY NOTES")
        
        if "data_quality_notes" in analysis:
            for note in analysis["data_quality_notes"]:
                print(f"⚠️  {note}")
        
        # Generate visualization config
        print_section("VISUALIZATION CONFIGURATION")
        
        try:
            viz_config = analyzer.generate_visualization_config(analysis)
            
            print(f"\n📈 Summary Cards: {len(viz_config.get('summary_cards', []))}")
            for card in viz_config.get('summary_cards', []):
                print(f"   - {card.get('title', 'Untitled')}: {card.get('type', 'unknown')}")
            
            print(f"\n📊 Charts: {len(viz_config.get('charts', []))}")
            for chart in viz_config.get('charts', []):
                print(f"   - {chart.get('title', 'Untitled')}: {chart.get('type', 'unknown')}")
            
            print("\n✅ Visualization configuration generated successfully")
            
        except Exception as e:
            print(f"❌ Error generating visualization config: {e}")
        
        print_section("TEST COMPLETED SUCCESSFULLY")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_dynamic_analysis.py <path_to_csv>")
        print("\nExample:")
        print("  python scripts/test_dynamic_analysis.py data/breast_cancer.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    test_dataset_analysis(csv_path)

