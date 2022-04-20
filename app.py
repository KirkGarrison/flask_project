from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stuff.db'
db = SQLAlchemy(app)

class Stuff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id

@app.route('/stuff', methods=['POST', 'GET'])
def stuff():
    title = "My stuff listing"
    if request.method == "POST":
        stuffs_name = request.form['name']
        new_item = Stuff(name=stuffs_name)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/stuff')
        except: 
            return "There was an error adding your stuff..."
    else:
        stuff = Stuff.query.order_by(Stuff.date_created)
        return render_template("stuff.html", title=title, stuff=stuff)

@app.route('/', methods=['GET'])
def base():
    title = "Home"
    return render_template("base.html", title=title)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    stuff_to_update = Stuff.query.get_or_404(id)
    if request.method == "POST":
        stuff_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/stuff')
        except:
            return "There was a problem with the update"
    else:
        return render_template('update.html', stuff_to_update=stuff_to_update)