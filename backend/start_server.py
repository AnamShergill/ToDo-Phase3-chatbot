#!/usr/bin/env python
"""
Server startup script for Railway deployment
"""

import os
import sys
import uvicorn
from main import app

def main():
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"Starting server on port {port}")

        # Start the server
        uvicorn.run(
            app,  # Pass the app object directly
            host="0.0.0.0",
            port=port,
            reload=False,  # Disable reload in production
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()