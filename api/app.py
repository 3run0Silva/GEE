from flask import Flask, render_template
from flask_cors import CORS
from routes.events.event_controller import event_blueprint
import os
print("Templates folder:", os.path.abspath('/frontend/templates'))

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
@app.route('/app/')
def serve_index():
    return render_template('index.html')

CORS(app)
app.register_blueprint(event_blueprint, url_prefix='/events')

if __name__ == '__main__':
  app.run(debug=True)