from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from routes.events.event_controller import event_blueprint

app = Flask(__name__)
class APIConfig:
  API_TITLE = "Events API"
  API_VERSION = "V1"
  OPENAPI_VERSION = "3.0.2"
  OPENAPI_URL_PREFIX = "/"
  OPENAPI_SWAGGER_UI_PATH = "/docs"
  OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  OPENAPI_REDOC_PATH = "/redoc"
  OPENAPI_REDOC_UI_URL = "https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"
app.config.from_object(APIConfig)
api = Api(app)
CORS(app)
app.register_blueprint(event_blueprint, url_prefix='/events')

if __name__ == '__main__':
  app.run(debug=True)