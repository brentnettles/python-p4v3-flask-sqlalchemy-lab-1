# server/app.py
# !/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

#adding views
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    eq = Earthquake.query.filter(Earthquake.id == id).first()

    if eq is None:
        return make_response({'message': f'Earthquake {id} not found.'}, 404)

    return make_response(eq.to_dict(), 200)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_mag(magnitude):
    eqs = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(eqs)

#mapped each Earthquake obj to dict
    eq_dicts = []
    for eq_obj in eqs:
        eq_dicts.append(eq_obj.to_dict())

    data = {
        'count': count,
        'quakes': eq_dicts
    }

    return make_response(data, 200)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
