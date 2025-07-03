import os
import sys
from pathlib import Path

# Add current directory to Python path for cPanel compatibility
sys.path.insert(0, str(Path(__file__).parent))

from app import app

# cPanel compatibility - set default environment variables
if not os.environ.get('SESSION_SECRET'):
    os.environ['SESSION_SECRET'] = 'change-this-secret-key-for-production'

if not os.environ.get('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'production'

if __name__ == "__main__":
    # For local development only
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)