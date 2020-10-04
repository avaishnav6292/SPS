from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
# from get_number import get_plate_number #ToDo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datadive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String())
    entry_time = db.Column(db.DateTime, default=datetime.utcnow)
    exit_time = db.Column(db.DateTime, default=None)
    duration = db.Column(db.Integer, default=None)
    charges = db.Column(db.Integer) 

@app.route('/')
def index():
    return render_template('index.html', vehicles=Vehicles.query.all())


@app.route('/detect', methods=['POST'])
def detection():
    filename = request.form['filename']
    if filename == "":
        filename = request.form['file']

    #detected_number = get_plate_number('images/' + filename) #Todo
    detected_number = "RJ19ZZ4504"  #Todo Comment
    vehicles = Vehicles(
        number=detected_number,
        entry_time = datetime.now()
        )
    try:
        db.session.add(vehicles)
        db.session.commit()
        return redirect('/')
    except:
        return "Something went wrong!"

@app.route('/update', methods=['POST'])
def update():  
    filename = request.form['filename']
    if filename == "":
        filename = request.form['file']

    #detected_number = get_plate_number('images/' + filename)
    detected_number = "RJ19BB1554" #Todo Comment

    id =  Vehicles.query.filter_by(number=detected_number).one().id
    vehicle = Vehicles.query.get_or_404(id)
    vehicle.exit_time = datetime.now()
    if (vehicle.exit_time - vehicle.entry_time).seconds/3600 < 1:
        vehicle.duration = str(int((vehicle.exit_time - vehicle.entry_time).seconds/60)) + ' mins'
    else:
        vehicle.duration = str(int((vehicle.exit_time - vehicle.entry_time).seconds/3600)) + ' hrs'
    vehicle.charges = calculate_charges(vehicle.duration)
    try:
        db.session.commit()
        return redirect('/')
    except:
        return "Something went wrong!"
    

def calculate_charges(duration):
    if duration.split(' ')[1] == 'mins':
        return 20
    else:
        hrs = int(duration.split(' ')[0])
        return 25 * hrs