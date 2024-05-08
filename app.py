from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from application.REST.admin import admins_blueprint
from application.REST.report import reports_blueprint
from application.REST.company import companies_blueprint
from application.REST.customer import customers_blueprint
from utils.error import Error


app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(admins_blueprint)
app.register_blueprint(reports_blueprint)
app.register_blueprint(companies_blueprint)
app.register_blueprint(customers_blueprint)

@app.route('/')
def hello_world():
    """Print 'Hello, world!' as the response body."""
    return 'Hello, world!'

@app.errorhandler(Error)
def invalid_api_usage(e: Error):
    return jsonify(e.to_dict()), e.status_code


if __name__ == '__main__':
    # Development
    app.run(debug=True)
    # Production
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)
