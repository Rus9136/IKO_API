# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run server: `python app.py`
- Run in debug mode: `FLASK_APP=app.py FLASK_DEBUG=1 flask run`
- Install dependencies: `pip install -r requirements.txt`
- Database migrations (SQLAlchemy models to DB): Handled automatically on startup

## Code Style Guidelines
- **Imports**: Group standard library imports first, then third-party packages, then local modules
- **Typing**: Use type hints with `typing` module (Dict, List, Optional, etc.)
- **Naming**: 
  - Classes: PascalCase
  - Functions/variables: snake_case
  - Constants: UPPER_CASE
- **Error handling**: Use try/except blocks with specific exceptions
- **Models**: Define SQLAlchemy models in models/ directory
- **Routes**: Define API endpoints in routes/ directory using Flask Blueprints
- **Services**: Business logic belongs in services/ directory
- **Schemas**: Marshmallow schemas for serialization in schemas/ directory
- **Documentation**: Add docstrings for public functions and classes