"""
This is the main flask app module
    - templates directory contains html pages
    - static directory contains needed JS and CSS files
    - loaded_data directory contains CSV for plots and analysys
    - routes.py contains all view functions for flask app
    - app.py is used to avoid cyclic imports
"""

from app.routes import app
