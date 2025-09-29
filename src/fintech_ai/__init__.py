"""
Fintech AI Enable Labs
A comprehensive toolkit for financial technology and AI integration.
"""

__version__ = "0.1.0"
__author__ = "Adam Salah"
__email__ = "contact@example.com"

# Optional imports - will be available if dependencies are installed
__all__ = ["__version__", "__author__", "__email__"]

try:
    from .core import FinanceDataProcessor, ModelTrainer
    __all__.extend(["FinanceDataProcessor", "ModelTrainer"])
except ImportError:
    pass

try:
    from .utils import load_config, setup_logging
    __all__.extend(["load_config", "setup_logging"])
except ImportError:
    pass