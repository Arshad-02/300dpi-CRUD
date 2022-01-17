from dbm.ndbm import library
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

 
#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    serial_no = db.Column(db.String(100))
    book_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    dop = db.Column(db.String(100))
    description = db.Column(db.String(100))
    no_borrowed = db.Column(db.String(100))
    no_stock = db.Column(db.String(100))


    def __init__(self,serial_no, book_name, author,dop,description,no_borrowed,no_stock):

        self.serial_no = serial_no
        self.book_name = book_name
        self.author = author
        self.dop = dop
        self.description = description
        self.no_borrowed = no_borrowed
        self.no_stock = no_stock





#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", library_manage = all_data)



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        serial_no = request.form['serial_no']
        book_name = request.form['book_name']
        author = request.form['author']


        my_data = Data(serial_no, book_name, author)
        db.session.add(my_data)
        db.session.commit()

        flash("data Inserted Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
#serial_no, book_name, author,dop,description,no_borrowed,no_stock
        my_data.serial_no = request.form['serial_no']
        my_data.book_name = request.form['book_name']
        my_data.author = request.form['author']

        db.session.commit()
        flash("data Updated Successfully")

        return redirect(url_for('Index'))




#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))






if __name__ == "__main__":
    app.run(debug=True)
