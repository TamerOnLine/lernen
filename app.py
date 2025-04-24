from flask import Flask
from routes import main_routes

app = Flask(__name__, template_folder='templates')
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
