from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/employee_dir'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

@app.route('/')
def index():
    all_employees = Employee.query.all()
    
    return render_template('index.html', employees = all_employees)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        my_data = Employee(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
        
        flash("Employee inserted successfully!")
        
        return redirect(url_for('index'))
    
@app.route('/update', methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        employee = Employee.query.get(request.form.get('id'))
        
        employee.name = request.form['name']
        employee.email = request.form['email']
        employee.phone = request.form['phone']
        
        db.session.commit()
        flash("Employee updated successfully!")
        
        return redirect(url_for('index'))
    
@app.route('/delete/<id>', methods = ['GET', 'POST'])
def delete(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    
    flash("Employee deleted successfully!")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()