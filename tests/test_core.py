"""
Tests for the core fintech_ai functionality.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fintech_ai.core import FinanceDataProcessor, ModelTrainer
from fintech_ai.utils import create_sample_data


class TestFinanceDataProcessor:
    """Test cases for FinanceDataProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = FinanceDataProcessor()
        self.sample_data = create_sample_data(n_samples=100)['dataframe']
    
    def test_load_data_from_dataframe(self):
        """Test loading data from DataFrame."""
        result = self.processor.load_data(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 100
        assert self.processor.data is not None
        assert list(result.columns) == list(self.sample_data.columns)
    
    def test_calculate_technical_indicators(self):
        """Test technical indicators calculation."""
        self.processor.load_data(self.sample_data)
        result = self.processor.calculate_technical_indicators()
        
        # Check that new columns are added
        expected_columns = ['SMA_20', 'SMA_50', 'Volatility', 'Price_Change', 'RSI']
        for col in expected_columns:
            assert col in result.columns
        
        # Check that values are reasonable
        assert not result['SMA_20'].dropna().empty
        assert not result['SMA_50'].dropna().empty
        assert (result['RSI'].dropna() >= 0).all()
        assert (result['RSI'].dropna() <= 100).all()
    
    def test_prepare_features(self):
        """Test feature preparation."""
        self.processor.load_data(self.sample_data)
        self.processor.calculate_technical_indicators()
        
        feature_columns = ['SMA_20', 'Volume']
        target_column = 'Close'
        
        self.processor.prepare_features(feature_columns, target_column)
        
        assert self.processor.features == feature_columns
        assert self.processor.target == target_column
        assert self.processor.data is not None
    
    def test_load_data_no_data_error(self):
        """Test error when trying to calculate indicators without data."""
        with pytest.raises(ValueError, match="No data loaded"):
            self.processor.calculate_technical_indicators()


class TestModelTrainer:
    """Test cases for ModelTrainer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.trainer = ModelTrainer()
        
        # Create sample training data
        np.random.seed(42)
        self.X = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100),
            'feature3': np.random.randn(100)
        })
        self.y = pd.Series(self.X['feature1'] * 2 + self.X['feature2'] + np.random.randn(100) * 0.1)
    
    def test_train_model_random_forest(self):
        """Test training random forest model."""
        results = self.trainer.train_model(self.X, self.y, model_type="random_forest")
        
        assert isinstance(results, dict)
        assert 'model_type' in results
        assert 'train_score' in results
        assert 'test_score' in results
        assert results['model_type'] == "random_forest"
        assert self.trainer.is_trained
        assert results['train_score'] > 0  # Should have some predictive power
    
    def test_train_model_unsupported(self):
        """Test error with unsupported model type."""
        with pytest.raises(ValueError, match="Unsupported model type"):
            self.trainer.train_model(self.X, self.y, model_type="unsupported_model")
    
    def test_predict_without_training(self):
        """Test error when predicting without training."""
        with pytest.raises(ValueError, match="Model not trained"):
            self.trainer.predict(self.X)
    
    def test_predict_after_training(self):
        """Test predictions after training."""
        self.trainer.train_model(self.X, self.y)
        predictions = self.trainer.predict(self.X)
        
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(self.X)
        assert predictions.dtype == np.float64
    
    def test_feature_importance(self):
        """Test feature importance extraction."""
        self.trainer.train_model(self.X, self.y)
        importance = self.trainer.get_feature_importance()
        
        assert isinstance(importance, pd.Series)
        assert len(importance) == self.X.shape[1]
        assert (importance >= 0).all()  # Feature importance should be non-negative
    
    def test_feature_importance_without_training(self):
        """Test error when getting feature importance without training."""
        with pytest.raises(ValueError, match="Model not trained"):
            self.trainer.get_feature_importance()


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    def test_complete_workflow(self):
        """Test the complete data processing and model training workflow."""
        # Generate sample data
        sample_data = create_sample_data(n_samples=200)['dataframe']
        
        # Process data
        processor = FinanceDataProcessor()
        processor.load_data(sample_data)
        processor.calculate_technical_indicators()
        
        # Prepare features
        feature_columns = ['SMA_20', 'Volume', 'Volatility']
        target_column = 'Close'
        processor.prepare_features(feature_columns, target_column)
        
        # Get clean data
        clean_data = processor.data.dropna()
        X = clean_data[feature_columns]
        y = clean_data[target_column]
        
        # Train model
        trainer = ModelTrainer()
        results = trainer.train_model(X, y)
        
        # Make predictions
        predictions = trainer.predict(X)
        
        # Assertions
        assert len(predictions) == len(X)
        assert results['train_score'] > 0
        assert results['test_score'] > 0
        assert trainer.is_trained
        
        # Feature importance should work
        importance = trainer.get_feature_importance()
        assert len(importance) == len(feature_columns)


if __name__ == "__main__":
    pytest.main([__file__])