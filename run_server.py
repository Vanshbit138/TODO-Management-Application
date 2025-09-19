#!/usr/bin/env python3
"""
Server startup script for TODO Management Application.
This script sets up the Python path and starts the FastAPI server.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(src_path)]
    )
