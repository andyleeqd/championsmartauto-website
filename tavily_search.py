#!/usr/bin/env python3
import json
import urllib.request
import urllib.error

API_KEY = "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"

url = "https://api.tavily.com/search"

payload = json.dumps({
    "api_key": API_KEY,
    "query": "Israel Iran conflict latest news March 2026",
    "search_depth": "advanced",
    "max_results": 10,
    "include_answer": True
}).encode('utf-8')

headers = {
    "Content-Type": "application/json"
}

try:
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")