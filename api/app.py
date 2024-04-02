from flask import Flask
from flask_cors import CORS
from routes.events.event_controller import event_blueprint

app = Flask(__name__)
CORS(app)
app.register_blueprint(event_blueprint, url_prefix='/events')

if __name__ == '__main__':
  app.run(debug=True)