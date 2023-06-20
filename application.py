from app import create_app
from config import FLASK_ENV

if __name__ == "__main__":
    app = create_app(FLASK_ENV)
    app.run(host="0.0.0.0", port=5000)
