from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# connect to table
db_name = "table_booking.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create Booking Table
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    total_consumers = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
db.create_all()

@app.route("/")
def home():
    # get all data in Booking table
    all_bookings = Booking.query.all()

    return render_template("home.html", bookings=all_bookings)


@app.route("/book", methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        # add to Booking table
        new_booking = Booking(
            name=request.form['name'],
            phone_number=request.form['phone_number'],
            total_consumers=request.form['total_consumers'],
            floor=request.form['floor'],
            time=request.form['time']
        )
        db.session.add(new_booking)
        db.session.commit()

        # check with phone_number
        if Booking.query.filter_by(phone_number=request.form['phone_number']).first():
            print("successfully added")

        # redirect to home
        return redirect(url_for("home"))

    return render_template("book.html")


@app.route("/update", methods=['GET', 'POST'])
def update():
    update_booking = Booking.query.filter_by(id=request.args['id']).first()
    if request.method == 'POST':
        # update booking data to database
        update_booking.name = request.form['name']
        update_booking.phone_number=request.form['phone_number']
        update_booking.total_consumers=request.form['total_consumers']
        update_booking.floor = request.form['floor']
        update_booking.time = request.form['time']
        db.session.add(update_booking)
        db.session.commit()
        return redirect(url_for("home"))

    # pass the current data to update form
    print(update_booking)
    return render_template("update.html", update_booking=update_booking)


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    # find by id
    delete_booking = Booking.query.filter_by(id=request.args['id']).first()

    # delete row
    db.session.delete(delete_booking)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()