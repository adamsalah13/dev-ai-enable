"""
Utility functions for the fintech AI package.
"""

import os
import logging
from typing import Dict, Any, TYPE_CHECKING
from pathlib import Path

# Optional imports
try:
    import yaml
except ImportError:
    yaml = None

if TYPE_CHECKING:
    import pandas as pd


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    if yaml is None:
        raise ImportError("PyYAML is required for configuration loading")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config


def setup_logging(level: str = "INFO", log_file: str = None) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        
    Returns:
        Configured logger
    """
    log_level = getattr(logging, level.upper())
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Root logger configuration
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def create_sample_data(n_samples: int = 1000, save_path: str = None) -> dict:
    """
    Create sample financial data for testing and examples.
    
    Args:
        n_samples: Number of samples to generate
        save_path: Optional path to save the data
        
    Returns:
        Dictionary containing sample data
    """
    try:
        import pandas as pd
        import numpy as np
    except ImportError:
        raise ImportError("pandas and numpy are required for sample data generation")
    
    from datetime import datetime, timedelta
    
    # Generate date range
    start_date = datetime.now() - timedelta(days=n_samples)
    dates = pd.date_range(start=start_date, periods=n_samples, freq='D')
    
    # Generate sample price data
    np.random.seed(42)
    
    # Starting price
    initial_price = 100.0
    
    # Generate price movements (random walk with trend)
    returns = np.random.normal(0.001, 0.02, n_samples)  # Small positive trend with volatility
    prices = [initial_price]
    
    for i in range(1, n_samples):
        new_price = prices[i-1] * (1 + returns[i])
        prices.append(max(new_price, 0.01))  # Ensure price stays positive
    
    # Generate OHLCV data
    data = {
        'Date': dates,
        'Open': [],
        'High': [],
        'Low': [],
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, n_samples)
    }
    
    # Generate Open, High, Low based on Close
    for i, close_price in enumerate(prices):
        daily_volatility = np.random.uniform(0.005, 0.03)
        open_price = close_price * (1 + np.random.normal(0, daily_volatility))
        
        high_price = max(open_price, close_price) * (1 + np.random.uniform(0, daily_volatility))
        low_price = min(open_price, close_price) * (1 - np.random.uniform(0, daily_volatility))
        
        data['Open'].append(max(open_price, 0.01))
        data['High'].append(max(high_price, 0.01))
        data['Low'].append(max(low_price, 0.01))
    
    df = pd.DataFrame(data)
    
    # Save if requested
    if save_path:
        df.to_csv(save_path, index=False)
        print(f"Sample data saved to {save_path}")
    
    return {
        'dataframe': df,
        'summary': {
            'n_samples': n_samples,
            'date_range': f"{dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}",
            'price_range': f"${df['Low'].min():.2f} - ${df['High'].max():.2f}",
            'avg_volume': f"{df['Volume'].mean():,.0f}"
        }
    }


def validate_data(df, required_columns: list = None) -> Dict[str, Any]:
    """
    Validate financial data structure and quality.
    
    Args:
        df: DataFrame to validate (requires pandas)
        required_columns: List of required column names
        
    Returns:
        Validation results dictionary
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required for data validation")
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
    if required_columns is None:
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    results = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }
    
    # Check required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        results['valid'] = False
        results['errors'].append(f"Missing required columns: {missing_columns}")
    
    # Check for empty data
    if df.empty:
        results['valid'] = False
        results['errors'].append("DataFrame is empty")
        return results
    
    # Check for negative prices
    price_columns = ['Open', 'High', 'Low', 'Close']
    for col in price_columns:
        if col in df.columns and (df[col] < 0).any():
            results['warnings'].append(f"Negative values found in {col}")
    
    # Check OHLC logic
    if all(col in df.columns for col in price_columns):
        invalid_ohlc = (
            (df['High'] < df['Low']) |
            (df['High'] < df['Open']) |
            (df['High'] < df['Close']) |
            (df['Low'] > df['Open']) |
            (df['Low'] > df['Close'])
        ).any()
        
        if invalid_ohlc:
            results['warnings'].append("Invalid OHLC relationships detected")
    
    # Data quality info
    results['info'] = {
        'rows': len(df),
        'columns': len(df.columns),
        'null_values': df.isnull().sum().to_dict(),
        'data_types': df.dtypes.to_dict()
    }
    
    return results