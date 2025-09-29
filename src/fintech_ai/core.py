"""
Core fintech AI functionality.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import logging

logger = logging.getLogger(__name__)


class FinanceDataProcessor:
    """
    A class for processing and analyzing financial data.
    """
    
    def __init__(self):
        self.data = None
        self.features = []
        self.target = None
    
    def load_data(self, data: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Load financial data from file or DataFrame.
        
        Args:
            data: File path or pandas DataFrame
            
        Returns:
            Loaded DataFrame
        """
        if isinstance(data, str):
            if data.endswith('.csv'):
                self.data = pd.read_csv(data)
            elif data.endswith('.json'):
                self.data = pd.read_json(data)
            else:
                raise ValueError("Unsupported file format")
        else:
            self.data = data.copy()
        
        logger.info(f"Loaded data with shape: {self.data.shape}")
        return self.data
    
    def calculate_technical_indicators(self) -> pd.DataFrame:
        """
        Calculate basic technical indicators for financial data.
        Assumes data has OHLCV columns.
        
        Returns:
            DataFrame with technical indicators
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Basic moving averages
        self.data['SMA_20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA_50'] = self.data['Close'].rolling(window=50).mean()
        
        # Volatility
        self.data['Volatility'] = self.data['Close'].rolling(window=20).std()
        
        # Price change
        self.data['Price_Change'] = self.data['Close'].pct_change()
        
        # RSI (simplified version)
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        
        logger.info("Technical indicators calculated")
        return self.data
    
    def prepare_features(self, feature_columns: List[str], target_column: str):
        """
        Prepare features and target for machine learning.
        
        Args:
            feature_columns: List of column names to use as features
            target_column: Name of target column
        """
        self.features = feature_columns
        self.target = target_column
        
        # Remove rows with NaN values
        self.data = self.data.dropna()
        
        logger.info(f"Prepared {len(self.features)} features for {len(self.data)} samples")


class ModelTrainer:
    """
    A class for training machine learning models on financial data.
    """
    
    def __init__(self):
        self.model = None
        self.is_trained = False
    
    def train_model(self, X: pd.DataFrame, y: pd.Series, 
                   model_type: str = "random_forest") -> Dict:
        """
        Train a machine learning model.
        
        Args:
            X: Feature DataFrame
            y: Target Series
            model_type: Type of model to train
            
        Returns:
            Training results dictionary
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        if model_type == "random_forest":
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Calculate metrics
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        results = {
            "model_type": model_type,
            "train_score": train_score,
            "test_score": test_score,
            "n_features": X.shape[1],
            "n_samples": X.shape[0]
        }
        
        logger.info(f"Model trained - Train R²: {train_score:.4f}, Test R²: {test_score:.4f}")
        return results
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions using the trained model.
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Predictions array
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train_model() first.")
        
        return self.model.predict(X)
    
    def get_feature_importance(self) -> pd.Series:
        """
        Get feature importance from the trained model.
        
        Returns:
            Series with feature names and importance scores
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train_model() first.")
        
        if hasattr(self.model, 'feature_importances_'):
            return pd.Series(
                self.model.feature_importances_,
                index=range(len(self.model.feature_importances_))
            )
        else:
            raise ValueError("Model does not support feature importance")