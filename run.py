import os
from app import create_app

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

from app.api import bp as api_bp
from app.api.health_controller import bp as health_bp
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(health_bp, url_prefix='/')
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)