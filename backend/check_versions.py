#!/usr/bin/env python
"""Check installed package versions"""

try:
    import pydantic
    print(f"Pydantic version: {pydantic.__version__}")
except ImportError as e:
    print(f"Pydantic not available: {e}")

try:
    import fastapi
    print(f"FastAPI version: {fastapi.__version__}")
except ImportError as e:
    print(f"FastAPI not available: {e}")

try:
    import sqlmodel
    print(f"SQLModel version: {sqlmodel.__version__}")
except ImportError as e:
    print(f"SQLModel not available: {e}")

try:
    import uvicorn
    print(f"Uvicorn version: {uvicorn.__version__}")
except ImportError as e:
    print(f"Uvicorn not available: {e}")