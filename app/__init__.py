import config
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(config)



db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return jsonify(error="Not found"), 404




from app.restless import page
app.register_blueprint(page)

# Create the database
db.create_all()


