import sys
import os

# Add parent directory to path so we can import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main Flask app
from app import app

# Vercel handler
def handler(request):
    return app

# For local testing
if __name__ == "__main__":
    app.run(debug=True)