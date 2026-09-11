"""
dashboard_ui.py
HTML provider for the AI Retail Decision Intelligence Platform.
Loads index.html from the api or public directory and caches in memory.
"""

import os

_CACHE = None

def get_dashboard_html() -> str:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    
    api_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(api_dir)
    candidates = [
        os.path.join(api_dir, "index.html"),
        os.path.join(root_dir, "public", "index.html"),
        os.path.join(root_dir, "api", "index.html"),
        os.path.join(os.getcwd(), "public", "index.html"),
        os.path.join(os.getcwd(), "api", "index.html"),
        os.path.join(os.getcwd(), "index.html"),
    ]
    for c in candidates:
        if os.path.exists(c):
            with open(c, "r", encoding="utf-8") as f:
                _CACHE = f.read()
                return _CACHE

    return """<!DOCTYPE html><html><head><title>AI Retail Decision Intelligence</title></head><body><h1>AI Retail Decision Intelligence Platform</h1></body></html>"""
