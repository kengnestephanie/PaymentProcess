"""Docstring for file."""
from flasgger import LazyJSONEncoder, LazyString, Swagger
from flask import Flask, request
from flask_app.config import DATABASES
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
uri = "postgresql://" + DATABASES['USER'] + ":" + DATABASES['PASSWORD'] + \
      "@" + DATABASES['HOST'] + ":" + DATABASES['PORT'] + \
      "/" + DATABASES['NAME']
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 2}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

template = dict(
    swaggerUiPrefix=LazyString(
        lambda: request.environ.get("HTTP_X_SCRIPT_NAME", ""))
)

app.json_encoder = LazyJSONEncoder
swagger = Swagger(app, config=swagger_config, template=template)
