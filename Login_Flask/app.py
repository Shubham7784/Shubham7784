from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:shubham01@localhost/flask_projects"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class user_data(db.Model):
    user_id = db.Column(db.String(100),primary_key = True)
    password = db.Column(db.String(20),nullable = False)
    email_id = db.Column(db.String(30),nullable = False)
    def __repr__(self) -> str:
        return f"{self.user_id}-{self.password}"

@app.route('/',methods = ['GET','POST'])
def main():
    return render_template('login.html')

@app.route('/registration',methods = ["GET","POST"])
def regis():
    if(request.method == "POST"):
        uid = request.form['uid']
        password = request.form['pass']
        email = request.form['eid']
        data = user_data(user_id = uid,password = password,email_id = email)
        db.session.add(data)
        db.session.commit()
    return render_template('registration.html')
@app.route('/login',methods = ["GET","POST"])
def login():
    if(request.method=="POST"):
        uid = request.form['user_id']
        password = request.form['password']
        data = user_data.query.get({"user_id":uid})
        if(data==None):
            return render_template('login.html',data = "User Not Found ! Please SignUp")
        elif(str(data).split("-")[1]==password):
            return redirect(url_for('home',data = data.user_id))
        else:
            return render_template('login.html',data = "Wrong Credentials ! Please try again")
        
@app.route('/home/<data>')
def home(data):

    return render_template('home.html',data = data)

@app.route('/signup',methods=["GET","POST"])
def signup():
    if(request.method=="POST"):
        uid = request.form['userid']
        password = request.form['password']
        email = request.form['email']
        user = user_data.query.get({'user_id':uid})
        if(user == None):
            data = user_data(user_id = uid,password = password ,email_id = email)
            db.session.add(data)
            db.session.commit()
            return redirect('/')
        else:
            return render_template('registration.html',data = "User Name already exist ! Try different one")
        
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)