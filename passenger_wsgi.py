#!/usr/bin/env python3
"""
WSGI configuration for cPanel hosting
This file is used by Passenger to serve the Flask application on cPanel
"""

import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask application
from main import app as application

# Set up environment variables if not already set
if not os.environ.get('SESSION_SECRET'):
    os.environ['SESSION_SECRET'] = 'your-secret-key-change-this-in-production'

# Configure for production
if __name__ == "__main__":
    # This won't be called in cPanel, but useful for local testing
    application.run(debug=False, host='0.0.0.0', port=5000)