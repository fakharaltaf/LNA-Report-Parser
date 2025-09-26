"""
Test script to validate LNA Bot installation and basic functionality.
"""

import sys
from pathlib import Path

# Add src to path for testing
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        from lna_bot.models import LNARecord, TrainingRecommendation, DatasetSummary
        print("✓ Models imported successfully")
        
        from lna_bot.core.decision_engine import LNADecisionEngine
        print("✓ Decision engine imported successfully")
        
        from lna_bot.utils.config_loader import ConfigurationLoader
        print("✓ Configuration loader imported successfully")
        
        from lna_bot.utils.data_processor import DataProcessor
        print("✓ Data processor imported successfully")
        
        from lna_bot import LNABot
        print("✓ Main LNABot class imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from lna_bot.utils.config_loader import ConfigurationLoader
        
        config_dir = Path("config")
        if not config_dir.exists():
            print(f"✗ Configuration directory not found: {config_dir}")
            return False
            
        config_loader = ConfigurationLoader(config_dir)
        
        # Test business rules loading
        try:
            business_rules = config_loader.load_business_rules()
            print("✓ Business rules loaded successfully")
        except Exception as e:
            print(f"✗ Business rules loading failed: {e}")
            return False
        
        # Test skills mapping loading  
        try:
            skills_mapping = config_loader.load_skills_mapping()
            print("✓ Skills mapping loaded successfully")
        except Exception as e:
            print(f"✗ Skills mapping loading failed: {e}")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_basic_functionality():
    """Test basic LNABot functionality."""
    print("\nTesting basic functionality...")
    
    try:
        from lna_bot import LNABot
        
        # Initialize bot
        bot = LNABot()
        print("✓ LNABot initialized successfully")
        
        # Test configuration validation
        issues = bot.validate_configuration()
        if issues:
            print(f"⚠ Configuration issues found: {issues}")
        else:
            print("✓ Configuration validation passed")
        
        # Test business rules info
        config_info = bot.get_business_rules_info()
        print(f"✓ Business rules info retrieved: {len(config_info)} items")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("LNA Bot Installation Test")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test configuration
    if not test_configuration():
        all_passed = False
    
    # Test basic functionality
    if not test_basic_functionality():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ All tests passed! LNA Bot is ready to use.")
        print("\nTo get started:")
        print("1. Run: python main.py --help")
        print("2. Or run: python main.py config")
        print("3. Analyze data: python main.py analyze Testing/LNA_Sample_Data/lna_healthcare_data.csv")
    else:
        print("✗ Some tests failed. Please check the configuration and dependencies.")
        sys.exit(1)

if __name__ == "__main__":
    main()