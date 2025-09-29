#!/usr/bin/env python3
"""
Basic usage example for Fintech AI Enable Labs.

This example demonstrates how to:
1. Load and process financial data
2. Calculate technical indicators
3. Train a machine learning model
4. Make predictions
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pandas as pd
from fintech_ai import FinanceDataProcessor, ModelTrainer, load_config, setup_logging
from fintech_ai.utils import create_sample_data, validate_data


def main():
    """Main example function."""
    
    # Setup logging
    logger = setup_logging(level="INFO")
    logger.info("Starting Fintech AI basic usage example")
    
    try:
        # Load configuration
        # config = load_config("../config/config.yaml")
        # For this example, we'll use defaults since config might not be accessible
        
        # Step 1: Create sample data (in real use, you'd load your own data)
        logger.info("Creating sample financial data...")
        sample_data = create_sample_data(n_samples=500)
        df = sample_data['dataframe']
        
        print("Sample Data Summary:")
        print(f"- {sample_data['summary']['n_samples']} data points")
        print(f"- Date range: {sample_data['summary']['date_range']}")
        print(f"- Price range: {sample_data['summary']['price_range']}")
        print(f"- Average volume: {sample_data['summary']['avg_volume']}")
        print()
        
        # Step 2: Validate data
        logger.info("Validating data...")
        validation_results = validate_data(df)
        if not validation_results['valid']:
            print("Data validation failed:")
            for error in validation_results['errors']:
                print(f"  ERROR: {error}")
            return
        
        print("Data validation passed!")
        if validation_results['warnings']:
            for warning in validation_results['warnings']:
                print(f"  WARNING: {warning}")
        print()
        
        # Step 3: Process data and calculate technical indicators
        logger.info("Processing financial data...")
        processor = FinanceDataProcessor()
        processor.load_data(df)
        processor.calculate_technical_indicators()
        
        print("Technical indicators calculated:")
        print(f"- Dataset shape: {processor.data.shape}")
        print(f"- Available columns: {list(processor.data.columns)}")
        print()
        
        # Step 4: Prepare features for machine learning
        logger.info("Preparing features...")
        feature_columns = ['SMA_20', 'SMA_50', 'RSI', 'Volatility', 'Volume']
        target_column = 'Close'
        
        processor.prepare_features(feature_columns, target_column)
        
        # Get clean data (no NaN values)
        clean_data = processor.data.dropna()
        X = clean_data[feature_columns]
        y = clean_data[target_column]
        
        print(f"Features prepared:")
        print(f"- Feature columns: {feature_columns}")
        print(f"- Target column: {target_column}")
        print(f"- Clean samples: {len(clean_data)}")
        print()
        
        # Step 5: Train machine learning model
        logger.info("Training machine learning model...")
        trainer = ModelTrainer()
        results = trainer.train_model(X, y, model_type="random_forest")
        
        print("Model training results:")
        print(f"- Model type: {results['model_type']}")
        print(f"- Training R²: {results['train_score']:.4f}")
        print(f"- Test R²: {results['test_score']:.4f}")
        print(f"- Features used: {results['n_features']}")
        print(f"- Training samples: {results['n_samples']}")
        print()
        
        # Step 6: Make predictions on recent data
        logger.info("Making predictions...")
        recent_data = X.tail(10)  # Last 10 data points
        predictions = trainer.predict(recent_data)
        actual_values = y.tail(10).values
        
        print("Recent predictions vs actual values:")
        for i, (pred, actual) in enumerate(zip(predictions, actual_values)):
            print(f"  Sample {i+1}: Predicted=${pred:.2f}, Actual=${actual:.2f}, "
                  f"Error={abs(pred-actual):.2f}")
        print()
        
        # Step 7: Feature importance (if available)
        try:
            importance = trainer.get_feature_importance()
            print("Feature importance:")
            for i, (feature, score) in enumerate(zip(feature_columns, importance)):
                print(f"  {feature}: {score:.4f}")
        except ValueError as e:
            print(f"Feature importance not available: {e}")
        
        logger.info("Example completed successfully!")
        
    except Exception as e:
        logger.error(f"Example failed with error: {e}")
        raise


if __name__ == "__main__":
    main()