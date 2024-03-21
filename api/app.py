from flask import Flask
from routes.events.event_controller import event_blueprint

app = Flask(__name__)
app.register_blueprint(event_blueprint, url_prefix='/events')

if __name__ == '__main__':
  app.run(debug=True)