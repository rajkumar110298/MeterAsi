from flask import Flask,request,jsonify
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
api = Api(app)

@dataclass()
class Meters(db.Model):
    id: int
    label: str
    __tablename__ = 'meters'
    id = db.Column(db.Integer,primary_key=True)
    label = db.Column(db.String(50))

@dataclass()
class MeterData(db.Model):
    id: int
    meter_id: int
    timestamp: str
    value: int
    __tablename__ = 'meter_data'
    id = db.Column(db.Integer,primary_key=True)
    meter_id = db.Column(db.Integer,db.ForeignKey('meters.id'),nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Integer)


class ShowMetersList(Resource):
    def get(self):
        data = Meters.query.all()
        APIs = {}
        for i in data:
            APIs[f'{i.label}'] = f"http://127.0.0.1:5000/meters/{i.id}"

        return APIs

    def post(self):
        data = request.json
        meter = Meters(label=data['label'])
        db.session.add(meter)
        db.session.commit()
        return "<h1> Your Data is Save </h1>"

class ShowMeters(Resource):
    def get(self,meter_id):
        data = MeterData.query.filter_by(meter_id=meter_id).order_by(MeterData.timestamp.desc()).all()
        new_data = jsonify(data)

        return new_data

    def post(self,meter_id):
        data = request.json
        meter_data = MeterData(meter_id=meter_id,timestamp=datetime.datetime.now(),value=data['value'])
        db.session.add(meter_data)
        db.session.commit()
        return "<h1> Your Data is Save </h1>"

api.add_resource(ShowMetersList,'/meters')
api.add_resource(ShowMeters,'/meters/<int:meter_id>')

if __name__ == '__main__':
    app.run(debug=True)

