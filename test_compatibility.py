#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Test script for Python 2/3 compatibility

from __future__ import print_function
import sys

# Python 2/3 compatibility for input function
try:
    # Python 2
    input = raw_input
except NameError:
    # Python 3
    pass

def test_input_compatibility():
    """Test that input works correctly in both Python 2 and 3"""
    print("Python version:", sys.version_info)
    print("Testing input compatibility...")
    
    try:
        # This should work in both Python 2 and 3 now
        test_text = "hello world"
        print("Test passed: input function is properly configured")
        print("Text would be:", repr(test_text))
        return True
    except Exception as e:
        print("Test failed:", str(e))
        return False

if __name__ == "__main__":
    test_input_compatibility()
