from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer ,primary_key = True)
    title = db.Column(db.String(200) ,nullable = False)
    desc = db.Column(db.String(500) ,nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} {self.title}"


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form.get('title')  # Use .get() to avoid KeyError
        desc = request.form.get('desc')
        
        if title and desc:  # Check if both fields are provided
            todo = Todo(title=title, desc=desc)  # Use submitted title and desc


            # print(f"Title: {todo.title}, Description: {todo.desc}")   --> This was just to check weather it acesses the data or not


            db.session.add(todo)
            db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


# @app.route("/" , methods = ['GET','POST'])
# def hello_world():
#     if request.method =='POST':
#         print(request.form['title'])
#     todo = Todo(title = "First Todo", desc = "Getup Code")
#     db.session.add(todo)
#     db.session.commit()
#     allTodo = Todo.query.all()
#     return render_template('index.html', allTodo = allTodo)
    # return "<p>Cult Flask!</p>"

@app.route("/show")                 #This web works even if this piece of code is not written
def hi():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'This is product page'

@app.route("/update/<int:sno>",methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc

        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno = sno).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>") 
def delete(sno):
    specificTodo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(specificTodo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)