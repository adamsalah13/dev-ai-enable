# Fintech AI Enable Labs

A comprehensive Python toolkit for financial technology and artificial intelligence integration. This project provides tools and frameworks for processing financial data, implementing machine learning models, and building AI-powered fintech applications.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

## 🚀 Features

- **Financial Data Processing**: Load, validate, and process financial datasets
- **Technical Indicators**: Calculate common technical analysis indicators (SMA, RSI, volatility, etc.)
- **Machine Learning**: Train and evaluate ML models for financial predictions
- **Data Validation**: Comprehensive data quality checks and validation
- **Sample Data Generation**: Create realistic financial datasets for testing and development
- **Jupyter Integration**: Ready-to-use notebooks for interactive analysis
- **Configuration Management**: Flexible YAML-based configuration system

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/adamsalah13/dev-ai-enable.git
cd dev-ai-enable

# Install required packages
pip install -r requirements.txt
```

### Verify Installation

```bash
# Run tests to verify everything works
python -m pytest tests/

# Or run the basic example
python examples/basic_usage.py
```

## 🎯 Quick Start

### Basic Usage

```python
from fintech_ai import FinanceDataProcessor, ModelTrainer
from fintech_ai.utils import create_sample_data

# Generate sample data
sample_data = create_sample_data(n_samples=365)
df = sample_data['dataframe']

# Process financial data
processor = FinanceDataProcessor()
processor.load_data(df)
processor.calculate_technical_indicators()

# Prepare features for ML
feature_columns = ['SMA_20', 'SMA_50', 'RSI', 'Volatility', 'Volume']
target_column = 'Close'
processor.prepare_features(feature_columns, target_column)

# Train a machine learning model
clean_data = processor.data.dropna()
X = clean_data[feature_columns]
y = clean_data[target_column]

trainer = ModelTrainer()
results = trainer.train_model(X, y, model_type="random_forest")

# Make predictions
predictions = trainer.predict(X)
```

### Interactive Analysis

Launch the Jupyter notebook for interactive exploration:

```bash
jupyter notebook notebooks/getting_started.ipynb
```

## 📁 Project Structure

```
dev-ai-enable/
├── src/fintech_ai/          # Main package source code
│   ├── __init__.py          # Package initialization
│   ├── core.py              # Core functionality (data processing, ML)
│   └── utils.py             # Utility functions
├── config/                  # Configuration files
│   └── config.yaml          # Main configuration
├── examples/                # Usage examples
│   └── basic_usage.py       # Basic usage example
├── notebooks/               # Jupyter notebooks
│   └── getting_started.ipynb # Interactive tutorial
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_core.py         # Core functionality tests
├── docs/                    # Documentation (future)
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
└── README.md              # This file
```

## 🛠 API Reference

### FinanceDataProcessor

Main class for processing financial data:

- `load_data(data)`: Load data from file or DataFrame
- `calculate_technical_indicators()`: Calculate SMA, RSI, volatility, etc.
- `prepare_features(feature_columns, target_column)`: Prepare data for ML

### ModelTrainer

Machine learning model training and evaluation:

- `train_model(X, y, model_type)`: Train ML models (Random Forest, etc.)
- `predict(X)`: Make predictions with trained model
- `get_feature_importance()`: Get feature importance scores

### Utility Functions

- `create_sample_data(n_samples)`: Generate realistic financial datasets
- `validate_data(df)`: Comprehensive data validation
- `load_config(config_path)`: Load YAML configuration
- `setup_logging(level, log_file)`: Configure logging

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_core.py
```

## 📊 Examples

### Technical Analysis Example

```python
from fintech_ai import FinanceDataProcessor
from fintech_ai.utils import create_sample_data
import matplotlib.pyplot as plt

# Create and process data
data = create_sample_data(n_samples=500)['dataframe']
processor = FinanceDataProcessor()
processor.load_data(data)
processed_data = processor.calculate_technical_indicators()

# Plot price with moving averages
plt.figure(figsize=(12, 6))
plt.plot(processed_data['Date'], processed_data['Close'], label='Close')
plt.plot(processed_data['Date'], processed_data['SMA_20'], label='SMA 20')
plt.plot(processed_data['Date'], processed_data['SMA_50'], label='SMA 50')
plt.legend()
plt.show()
```

### Machine Learning Example

```python
from fintech_ai import ModelTrainer
from sklearn.metrics import mean_absolute_error

# Assuming you have X (features) and y (target) prepared
trainer = ModelTrainer()
results = trainer.train_model(X, y, model_type="random_forest")

print(f"Training R²: {results['train_score']:.4f}")
print(f"Test R²: {results['test_score']:.4f}")

# Make predictions and calculate error
predictions = trainer.predict(X)
mae = mean_absolute_error(y, predictions)
print(f"Mean Absolute Error: ${mae:.2f}")
```

## ⚙️ Configuration

Customize the behavior using the configuration file at `config/config.yaml`:

```yaml
# Model settings
models:
  default_model: "random_forest"
  validation_split: 0.2
  random_seed: 42

# Features
features:
  technical_indicators:
    - SMA_20
    - SMA_50
    - RSI
    - Volatility

# Logging
logging:
  level: "INFO"
  file: "logs/fintech_ai.log"
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests before submitting
python -m pytest tests/

# Format code
black src/ tests/ examples/

# Check code style
flake8 src/ tests/ examples/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Adam Salah**
- GitHub: [@adamsalah13](https://github.com/adamsalah13)

## 🙏 Acknowledgments

- Built with Python and the scientific computing ecosystem
- Inspired by the need for accessible fintech AI tools
- Thanks to the open-source community for amazing libraries

## 📈 Roadmap

- [ ] Real-time data integration (Yahoo Finance, Alpha Vantage)
- [ ] Advanced ML models (XGBoost, Neural Networks)
- [ ] Backtesting framework
- [ ] Portfolio optimization tools
- [ ] Risk management metrics
- [ ] Web dashboard interface
- [ ] Docker containerization
- [ ] Cloud deployment guides

## 🐛 Issues & Support

If you encounter any issues or have questions:

1. Check the [documentation](README.md) and [examples](examples/)
2. Search existing [issues](https://github.com/adamsalah13/dev-ai-enable/issues)
3. Create a new issue with detailed information

## 📚 Resources

- [Getting Started Notebook](notebooks/getting_started.ipynb)
- [Basic Usage Example](examples/basic_usage.py)
- [Configuration Guide](config/config.yaml)
- [Test Examples](tests/test_core.py)
