# Dev AI Enable - Comprehensive AI-Driven Development Platform

A comprehensive platform combining AI-driven CI/CD course materials with fintech AI tools and frameworks. This project serves both as an educational resource for development teams and a practical Python toolkit for financial technology applications.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![JavaScript](https://img.shields.io/badge/javascript-es6%2B-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

## 🎯 Project Overview

This platform combines two powerful components:

### 1. AI-Driven CI/CD Course
A comprehensive hands-on course for development teams to learn AI-driven CI/CD processes from Business Analysis to Quality Assurance and Documentation.

### 2. Fintech AI Labs
A Python toolkit for financial technology and artificial intelligence integration, providing tools and frameworks for processing financial data and implementing machine learning models.

## 👥 Target Personas

This platform is designed for:

- **Business Analysts (BA)** - Requirements gathering and user story creation
- **Product Owners** - Feature planning and backlog management  
- **Developers** - Code implementation and testing
- **DevOps Engineers** - CI/CD pipeline management
- **Quality Assurance (QA)** - Testing strategy and automation
- **Technical Writers** - Documentation and knowledge management
- **Data Scientists** - Financial modeling and AI development
- **Fintech Engineers** - Financial application development

## 🏗️ Course Structure

### Module 1: Foundation Setup
- Repository setup and collaboration workflows
- VSCode/Cursor AI agent configuration
- GitHub Copilot integration
- Fork and contribution workflows

### Module 2: Persona-Specific AI Workflows
- BA: AI-assisted requirements analysis
- Developer: AI-powered code generation
- QA: AI-driven test automation
- Documentation: AI-enhanced technical writing

### Module 3: End-to-End Integration
- Connecting AI workflows across personas
- Automated CI/CD with AI assistance
- Quality gates and automated reviews
- Deployment and monitoring

### Module 4: Fintech-Specific Applications
- Compliance and security considerations
- Financial data handling
- Regulatory documentation
- Risk management workflows

## 🚀 Features

### Course Components
- AI-assisted requirements analysis and user story creation
- AI-powered code generation and testing
- Automated CI/CD with AI assistance
- Quality gates and automated reviews
- Fintech-specific compliance and security considerations

### Fintech AI Toolkit
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
- Node.js 16+ (for sample applications)
- Git and GitHub account
- VSCode or Cursor IDE

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/adamsalah13/dev-ai-enable.git
cd dev-ai-enable

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for sample apps)
cd sample-app && npm install && cd ..
```

### Verify Installation

```bash
# Run Python tests
python -m pytest tests/

# Run basic example
python examples/basic_usage.py

# Start sample application (optional)
cd sample-app && npm start
```

## 🎯 Quick Start

### For Course Participants

1. **Fork this repository** to your GitHub account
2. **Clone your fork** locally
3. **Follow the setup guides** in each persona directory
4. **Complete the exercises** in sequence
5. **Submit pull requests** for review

### For Fintech AI Development

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

## 📁 Repository Structure

```
├── personas/                    # Persona-specific guides and exercises
│   ├── business-analyst/       # BA workflows and tools
│   ├── developer/              # Development workflows
│   ├── devops/                 # CI/CD and infrastructure
│   ├── qa/                     # Testing and quality assurance
│   └── documentation/          # Technical writing workflows
├── sample-app/                  # Fintech sample application (Node.js/React)
├── src/fintech_ai/             # Python fintech AI toolkit
│   ├── __init__.py            # Package initialization
│   ├── core.py                # Core functionality (data processing, ML)
│   └── utils.py               # Utility functions
├── templates/                   # AI prompt templates
├── docs/                       # Course and API documentation
├── examples/                   # Usage examples
├── notebooks/                  # Jupyter notebooks
├── tests/                      # Test suite
├── config/                     # Configuration files
└── .github/workflows/          # GitHub Actions CI/CD
```

## 🛠️ Prerequisites

- GitHub account with Copilot access
- Git basics knowledge
- VSCode or Cursor IDE
- Basic understanding of software development lifecycle
- Python 3.8+ for fintech toolkit
- Interest in AI-powered development workflows

## 📚 Learning Outcomes

By the end of this course, participants will be able to:

- ✅ Set up and configure AI development environments
- ✅ Use AI tools effectively for their specific role
- ✅ Collaborate across personas using AI-enhanced workflows
- ✅ Implement end-to-end CI/CD pipelines with AI assistance
- ✅ Apply fintech-specific considerations to AI workflows
- ✅ Create and maintain AI-generated documentation
- ✅ Establish quality gates and automated review processes
- ✅ Build and deploy fintech AI applications
- ✅ Process financial data and implement ML models

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
# Run Python tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_core.py

# Run sample application tests
cd sample-app && npm test
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

## 📈 Roadmap

### Course Enhancements
- [ ] Advanced AI prompt engineering workshops
- [ ] Real-world case studies and scenarios
- [ ] Integration with more AI development tools
- [ ] Certification and assessment framework

### Fintech AI Toolkit
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

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Adam Salah**
- GitHub: [@adamsalah13](https://github.com/adamsalah13)

## 🙏 Acknowledgments

- Built with Python and the scientific computing ecosystem
- Inspired by the need for accessible fintech AI tools
- Thanks to the open-source community for amazing libraries