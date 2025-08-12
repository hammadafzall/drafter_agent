#!/usr/bin/env python3
"""
Test script for Drafter Agent

This script tests the basic functionality of the agent without making API calls.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import agent
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_tools():
    """Test the tool functions."""
    try:
        from agent import update, save, document_content
        
        # Test update tool
        test_content = "This is a test document."
        result = update(test_content)
        assert "successfully" in result.lower()
        assert test_content in result
        print("✅ Update tool works correctly")
        
        # Test save tool
        test_filename = "test_document"
        result = save(test_filename)
        assert "successfully" in result.lower()
        print("✅ Save tool works correctly")
        
        # Check if file was created
        test_file = Path("test_document.txt")
        if test_file.exists():
            test_file.unlink()  # Clean up
            print("✅ File creation works correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Tool test error: {e}")
        return False

def test_environment():
    """Test environment setup."""
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    # Check if .env exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file exists")
    else:
        print("⚠️  .env file not found (create one with OPENAI_API_KEY)")
    
    # Check if requirements are installed
    try:
        import langchain_core
        import langchain_openai
        import langgraph
        import dotenv
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Drafter Agent...")
    print("=" * 40)
    
    tests = [
        ("Environment Setup", test_environment),
        ("Module Imports", test_imports),
        ("Tool Functions", test_tools),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The agent is ready to use.")
        print("\nTo run the agent:")
        print("python agent.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the agent.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
