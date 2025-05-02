from flask import Flask
from flask_cors import CORS
from routes.upload import upload_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": app.config['ALLOWED_ORIGINS']}})
app.register_blueprint(upload_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
