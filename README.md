# CRUD Table Booking with sqlite
## CRUD (flask-sqlalchemy)

- [flask](https://github.com/aky20/Flask)
- jinja
- flask-sqlalchemy

### create database
```
from flask_sqlalchemy import SQLAlchemy

db_name = "table_booking.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
```

### create table
```
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    total_consumers = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    
db.create_all()
```

### read data
```
# jinja
{% if not bookings: %}
    <h1 class="header">No Booking Today</h1>
    {% else %}
        <table class="table_1">
        <tr>
            <th>Id</th>
            <th>Name</th>
            <th class="extra">Phone number</th>
            <th class="extra">Total Consumers</th>
            <th class="extra">Floor</th>
            <th class="extra">Time</th>
            <th class="table_more_column">More</th>
            <th>Edit</th>
        </tr>
        {% for booking in bookings %}
        <tr>
            <td>{{ booking['id'] }}</td>
            <td>{{ booking['name'] }}</td>
            <td class="extra">{{ booking['phone_number'] }}</td>
            <td class="extra">{{ booking['total_consumers'] }}</td>
            <td class="extra">{{ booking['floor'] }}</td>
            <td class="extra">{{ booking['time'] }}</td>
            <td class="table_more_column">
                <p><span>Phone number : </span>{{ booking['phone_number'] }}</p>
                <p><span>Total Consumers : </span>{{ booking['total_consumers'] }}</p>
                <p><span>Floor : </span>{{ booking['floor'] }}</p>
                <p><span>Time : </span>{{ booking['time'] }}</p>
            </td>
            <td>
                <a class="scale_icon_btn" href="{{ url_for( 'update', id=booking['id'] ) }}">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 update" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                </a>
                <a class="scale_icon_btn" href="{{ url_for('delete', id=booking['id']) }}">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 delete" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </a>
            </td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}


#flask
@app.route("/")
def home():
    # get all data in Booking table
    all_bookings = Booking.query.all()

    return render_template("home.html", bookings=all_bookings)
```

### create data
```
#jinja
  <form class="form_4" method="POST" action="{{ url_for('book') }}">
      <div class="input_fields">
          <h1>Table Booking</h1>
          <input type="text" name="name" id="name" placeholder="Name" required>
          <input type="tel" name="phone_number" id="phone_number" placeholder="Phone number" required>
          <input type="number" name="total_consumers" id="total_consumers" placeholder="Total consumers" min="1" max="25" required>
          <div class="radio_container">
              <label><input type="radio" name="floor" value="floor1" id="floor_1" required>Floor 1</label>
              <label><input type="radio" name="floor" value="floor2" id="floor_2" required>Floor 2</label>
          </div>
          <input type="time" name="time" id="time" placeholder="Time" required>
      </div>
  <button class="sink_md_btn"  type="submit">
      book
  </button>
  </form>

#flask 
@app.route("/book", methods=['GET', 'POST'])
def book():
    if not os.path.isfile(db_name):
        db.create_all()
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
```

### update data
```
#jinja
    <form class="form_4" method="POST" action="{{ url_for('update', id=update_booking.id) }}">
        <div class="input_fields">
            <h1>Update Booking</h1>
            <input type="text" name="name" id="name" placeholder="Name" value="{{ update_booking.name }}" required>
            <input
                    type="tel"
                    name="phone_number"
                    id="phone_number"
                    placeholder="Phone number"
                    value="{{ update_booking.phone_number }}"
                    required
            >
            <input
                    type="number"
                    name="total_consumers"
                    id="total_consumers"
                    placeholder="Total consumers"
                    min="1"
                    max="25"
                    value="{{ update_booking.total_consumers }}"
                    required
            >
            <div class="radio_container">
                {% if update_booking.floor == "floor1" %}
                <label><input type="radio" name="floor" value="floor1" checked>Floor 1</label>
                <label><input type="radio" name="floor" value="floor2">Floor 2</label>
                {% else %}
                <label><input type="radio" name="floor" value="floor1">Floor 1</label>
                <label><input type="radio" name="floor" value="floor2" checked>Floor 2</label>
                {% endif %}
            </div>
            <input type="time" name="time" id="time" placeholder="Time" value="{{update_booking.time}}" required>
        </div>
        <button class="sink_md_btn" type="submit">
            Update
        </button>
    </form>

#flask
@app.route("/update", methods=['GET', 'POST'])
def update():
    update_booking = Booking.query.get(request.args['id'])
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
```

Or

```
@app.route("/update", methods=['GET', 'POST'])
def update():
    update_booking = Booking.query.get(request.args['id'])
    if request.method == 'POST':
        # update only phone-number data to database
        update_booking.phone_number=request.form['phone_number']
        db.session.commit()
        return redirect(url_for("home"))

    # pass the current data to update form
    print(update_booking)
    return render_template("update.html", update_booking=update_booking)
```


### delete data
```
# flask
@app.route("/delete", methods=['GET', 'POST'])
def delete():
    # find by id
    delete_booking = Booking.query.get(request.args['id'])

    # delete row
    db.session.delete(delete_booking)
    db.session.commit()
    return redirect(url_for("home"))
```
-------------------------------------
# One to Many Relationship 

### Create Database
```
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///student.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
```

### Create Table
- One class has Many students
```
# One
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    students = db.relationship('Student', backref='classroom')

# Many
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
```
- backref (backreference make Student class to have classroom column and you have to initialize an object to classroom property)
- db.ForeignKey (primarykey of Parent Table)

### Create rows to Class Table
```
B = Class(name='Class_C')
db.session.add(B)
db.session.commit()
```

### Create rows to Student Table
```
A = Class.query.get(3)
emma = Student(name='Cho', classroom=A)
db.session.add(emma)
db.session.commit()
```
- initialize A to classroom property and then class_id of student emma become A.id

### Use Data
#### Get all students attends in Class B
```
class_B = Class.query.filter_by(name='Class_B').first()
print(class_B.students)
```

#### Get the id of Jo classroom
```
classroom_id = Student.query.filter_by(name='Jo').first().class_id
print(classroom_id)
```
