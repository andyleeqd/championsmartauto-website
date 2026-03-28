#!/usr/bin/env python3
"""
Test script for Tavily skill configuration
"""

import sys
import os

# Add the skills directory to Python path
sys.path.append('/home/lijia/.npm-global/lib/node_modules/openclaw/skills/tavily')

try:
    from tavily import TavilySearch
    
    print("✅ Tavily module imported successfully")
    
    # Test search functionality
    searcher = TavilySearch()
    
    print("\n🔍 Testing basic search...")
    try:
        results = searcher.search("OpenClaw AI assistant", depth="basic", max_results=3)
        print("✅ Basic search successful")
        
        if "error" not in results:
            print(f"   Found {len(results.get('results', []))} results")
            if 'answer' in results and results['answer']:
                print(f"   Answer extracted: {results['answer'][:50]}...")
                
    except Exception as e:
        print(f"❌ Basic search failed: {e}")
    
    print("\n🧪 Testing advanced search...")
    try:
        results = searcher.search("AI research 2026", depth="advanced", max_results=2, include_answer=True)
        print("✅ Advanced search successful")
        
    except Exception as e:
        print(f"❌ Advanced search failed: {e}")
    
    print("\n✅ Tavily skill configuration test completed")
    
except ImportError as e:
    print(f"❌ Failed to import Tavily module: {e}")
    print("Please ensure the tavily.py file is in the correct location")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")