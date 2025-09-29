#!/usr/bin/env python3
"""
Simple demo that works without external dependencies.
This demonstrates the basic project structure and organization.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Simple demo function."""
    print("🚀 Fintech AI Enable Labs - Simple Demo")
    print("=" * 50)
    
    try:
        # Test basic imports
        print("✅ Testing basic project structure...")
        from fintech_ai import __version__, __author__
        print(f"   Package version: {__version__}")
        print(f"   Author: {__author__}")
        
        # Test configuration loading
        print("✅ Testing configuration system...")
        try:
            from fintech_ai.utils import load_config
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
            if os.path.exists(config_path):
                config = load_config(config_path)
                print(f"   Configuration loaded: {len(config)} sections")
                print(f"   Default model: {config.get('models', {}).get('default_model', 'N/A')}")
            else:
                print("   Configuration file not found (this is OK for demo)")
        except ImportError as e:
            print(f"   Configuration loading requires PyYAML: {e}")
        
        # Test basic functionality
        print("✅ Testing core classes...")
        try:
            from fintech_ai.core import FinanceDataProcessor, ModelTrainer
            
            # Create instances
            processor = FinanceDataProcessor()
            trainer = ModelTrainer()
            
            print("   FinanceDataProcessor: instantiated successfully")
            print("   ModelTrainer: instantiated successfully")
        except ImportError as e:
            print(f"   Core classes require additional dependencies: {e}")
            print("   (This is expected without pandas/scikit-learn installed)")
        
        # Test data validation utility
        print("✅ Testing utility functions...")
        try:
            from fintech_ai.utils import validate_data
            print("   Data validation function imported successfully")
        except ImportError as e:
            print(f"   Some utilities require pandas: {e}")
        
        # Test project structure
        print("✅ Testing project structure...")
        project_root = os.path.join(os.path.dirname(__file__), '..')
        
        expected_dirs = {
            'src': 'Source code directory',
            'config': 'Configuration files',
            'examples': 'Usage examples',
            'notebooks': 'Jupyter notebooks',
            'tests': 'Test suite',
            'docs': 'Documentation (future)'
        }
        
        for dir_name, description in expected_dirs.items():
            dir_path = os.path.join(project_root, dir_name)
            if os.path.exists(dir_path):
                print(f"   ✓ {dir_name}/: {description}")
            else:
                print(f"   - {dir_name}/: {description} (not found)")
        
        # Test essential files
        print("✅ Testing essential files...")
        essential_files = {
            'README.md': 'Project documentation',
            'LICENSE': 'MIT License',
            'requirements.txt': 'Python dependencies',
            'setup.py': 'Package setup script',
            '.gitignore': 'Git ignore rules',
            'Makefile': 'Development commands'
        }
        
        for file_name, description in essential_files.items():
            file_path = os.path.join(project_root, file_name)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"   ✓ {file_name}: {description} ({size} bytes)")
            else:
                print(f"   - {file_name}: {description} (not found)")
        
        print()
        print("🎉 Demo completed successfully!")
        print()
        print("📚 Next Steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Run full example: python examples/basic_usage.py")
        print("   3. Start Jupyter: jupyter notebook notebooks/getting_started.ipynb")
        print("   4. Run tests: python -m pytest tests/")
        print("   5. Check documentation: cat README.md")
        
    except Exception as e:
        print(f"❌ Error in demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())