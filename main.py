"""Google Cloud Platform entry point for snow-flask-whoami."""

import os
import sys

# Add parent directory to path for snow_flask_core imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from snow_flask_core import create_app
from snow_flask_core.logging_config import setup_logging

setup_logging()

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
