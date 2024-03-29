from flask import Flask
from application.REST.admin import admins_blueprint
from application.REST.report import reports_blueprint
from application.REST.company import companies_blueprint
from application.REST.customer import customers_blueprint


app = Flask(__name__)

app.register_blueprint(admins_blueprint)
app.register_blueprint(reports_blueprint)
app.register_blueprint(companies_blueprint)
app.register_blueprint(customers_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
