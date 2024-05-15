from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import date
from sqlalchemy.exc import IntegrityError
app = Flask(__name__,static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:shubham01@localhost/librarymanagement_flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Defining the Database Model
class user(db.Model):
    user_id = db.Column(db.String(100),primary_key = True)
    password = db.Column(db.String(20),nullable = False)
    contact_info = db.Column(db.String(30),nullable = False)
    user_name = db.Column(db.String(30),nullable = False)

    def __repr__(self) -> str:
        return f"{self.user_id}-{self.password}-{self.contact_info}-{self.user_name}"

class admin(db.Model):
    admin_userid = db.Column(db.String(100),primary_key = True)
    admin_password = db.Column(db.String(20),nullable = False)
    admin_name = db.Column(db.String(30),nullable = False)
    contact_info = db.Column(db.String(30),nullable = False)

    def __repr__(self) -> str:
        return f"{self.admin_userid}-{self.admin_password}-{self.admin_name}-{self.contact_info}"
class book(db.Model):
    book_id = db.Column(db.Integer,primary_key = True)
    book_name = db.Column(db.String(50),nullable = False)
    author = db.Column(db.String(30),nullable = False)
    price = db.Column(db.Integer,nullable = False)
    quantity = db.Column(db.Integer,nullable = False)

    def __repr__(self) -> str:
        return f"{self.book_id}-{self.book_name}-{self.author}-{self.price}-{self.quantity}"
class book_borrowed(db.Model):
    book_id = db.Column(db.Integer,primary_key = True)
    borrowed_by = db.Column(db.String(100),nullable = False)
    duration_month = db.Column(db.Integer,nullable = False)
    fine_generated = db.Column(db.Integer)
    date_borrowed_on = db.Column(db.Date,nullable = False)
    quantity  = db.Column(db.Integer,nullable = False)

    def __repr__(self) -> str:
        return f"{self.book_id}-{self.borrowed_by}-{self.duration_month}-{self.fine_generated}-{self.date_borrowed_on}-{self.quantity}"


#HomePage Route
@app.route('/')
def main():
    return render_template("login.html")

@app.route('/login',methods = ["GET","POST"])
def login():
    if(request.method == "POST"):
        uid = request.form['id']
        password = request.form['password']
        query_data = user.query.get({"user_id":uid})
        if(query_data == None):
            return render_template('login.html',data = "Login Failed !! User not found Please Sign In")
        else:
            query_data = str(query_data).split("-")
            if(query_data[1] == password):
                return redirect(url_for("home",data = uid))
            else:
                return render_template("login.html",data = "Failed to Login at this moment!! Try after some time")
        

#User's Side Code Snippet 
@app.route("/home<data>")
def home(data):
    username = user.query.get({"user_id":data})
    username = str(username).split("-")[3]
    books = book.query.all()
    b_count = len(books)
    issued_book = db.session.execute(db.select(book_borrowed).filter_by(borrowed_by=data)).scalars()
    i_count = len(issued_book.fetchall())
    return render_template("home.html",data=username,book_count=b_count,issue_count=i_count,uid = data)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/sign",methods = ["GET","POST"])
def sign():
    if(request.method == "POST"):
        uname = request.form['uname']
        uid = request.form['id']
        password = request.form['password']
        contact = request.form['c_info']
        data = user(user_id = uid , user_name = uname , password = password ,contact_info = contact)
        db.session.add(data)
        db.session.commit()
        return render_template("login.html",data = "Sign Up Successfully !! Please Log In")
    


@app.route("/showbook/<user>")
def showbook(user):
    stmt = text("Select book_id,book_name,author,price from book;")
    tables = db.session.execute(stmt).fetchall()
    count = len(tables)
    return render_template("showbooks.html",tables = tables,count = count,uid = user)

@app.route("/issued_book/<user>")
def show_issued_book(user):
    stmt = text(f"select book_id,duration_month,fine_generated,quantity from book_borrowed where borrowed_by = '{user}';")
    tables = db.session.execute(stmt).fetchall()
    return render_template("issuedbook.html",tables = tables, count = len(tables),uid = user)

@app.route("/issue/<bid>/<uid>")
def issue(bid,uid):
    stmt = text(f"select quantity from book_borrowed where borrowed_by = '{uid}' and book_id = {bid}")
    query = db.session.execute(stmt).fetchall()
    if(len(query)==0):
        stmt = text(f"insert into book_borrowed values({bid},'{uid}',1,0,'{date.today()}',1);")
        db.session.execute(stmt)
        db.session.commit()
    else:
        stmt = text(f"select quantity from book_borrowed where book_id = {bid} and borrowed_by = '{uid}';")
        quantity = db.session.execute(stmt).fetchall()
        quantity = int(quantity[0][0])+1 
        stmt = text(f"update book_borrowed set quantity = {quantity} where book_id = {bid} and borrowed_by = '{uid}';")
        db.session.execute(stmt)
        db.session.commit()
    stmt = text(f"select quantity from book where book_id = {bid};")
    quantity = int(db.session.execute(stmt).fetchall()[0][0])
    quantity -=1
    stmt = text(f"update book set quantity = {quantity} where book_id = {bid};")
    db.session.execute(stmt)
    db.session.commit()
    return render_template("message.html",uid=uid,message = "Book Issued Successfully",fine=0)  
@app.route("/return/<bid>/<uid>")
def return_book(bid,uid):
    stmt = text(f"select quantity,date_borrowed_on from book_borrowed where book_id = {bid} and borrowed_by = '{uid}';")
    quantity,date_borrowed = db.session.execute(stmt).fetchall()[0]
    date_borrowed = str(date_borrowed).split("-")
    date_borrowed = date(year=int(date_borrowed[0]),month=int(date_borrowed[1]),day=int(date_borrowed[2]))
    curr_date = date.today()
    diff = ((curr_date.year - date_borrowed.year)*365 + (curr_date.month - date_borrowed.month)*28 + (curr_date.day - date_borrowed.day))
    fine = diff*50 if(diff>1) else 0
    if(fine ==0):
        if(int(quantity)>1):
            quantity = int(quantity) - 1
            stmt = text(f"update book_borrowed set quantity = {quantity} where book_id = {bid} and borrowed_by = '{uid}';")
            db.session.execute(stmt)
            db.session.commit()
        else:
            stmt = text(f"delete from book_borrowed where book_id = {bid} and borrowed_by = '{uid}';")
            db.session.execute(stmt)
            db.session.commit()
        stmt = text(f"select quantity from book where book_id = {bid};")
        quantity = int(db.session.execute(stmt).fetchall()[0][0])
        quantity+=1
        stmt = text(f"update book set quantity = {quantity} where book_id = {bid};")
        db.session.execute(stmt)
        db.session.commit()
        return render_template("message.html",uid=uid,message="Book Returned Successfully",fine=0)
    else:
        return render_template("message.html",uid=uid,message= f"Due to late submission ! {fine} Rupees Fine has been generated",fine=fine,bid=bid)
@app.route("/return_fine/<bid>/<uid>")
def return_fine(bid,uid):
    stmt = text(f"delete from book_borrowed where book_id = {bid} and borrowed_by = '{uid}';")
    db.session.execute(stmt)
    db.session.commit()
    stmt = text(f"select quantity from book where book_id = {bid};")
    quantity = int(db.session.execute(stmt).fetchall()[0][0])
    quantity+=1
    stmt = text(f"update book set quantity = {quantity} where book_id = {bid};")
    db.session.execute(stmt)
    db.session.commit()
    return render_template("message.html",uid=uid,message="Book Returned Successfully",fine=0)

@app.route("/return_fine_unpaid/<bid>/<uid>/<fine>")
def return_withoutfine(bid,uid,fine):
    stmt = text(f"update book_borrowed set fine_generated = {fine} where book_id = {bid} and borrowed_by = '{uid}';")
    db.session.execute(stmt)
    db.session.commit()
    return redirect(url_for("show_issued_book",user=uid))  
@app.route("/return/all/<uid>")
def return_all(uid):
    stmt = text(f"select book_id,quantity from book_borrowed where borrowed_by = '{uid}';")
    query = db.session.execute(stmt).fetchall()
    for bid,quant in query:
        stmt = text(f"select quantity from book where book_id = {bid};")
        quantity = int(db.session.execute(stmt).fetchall()[0][0])
        quantity+=quant
        stmt = text(f"update book set quantity = {quantity} where book_id = {bid};")
        db.session.execute(stmt)
        db.session.commit() 
    stmt = text(f"delete from book_borrowed where borrowed_by = '{uid}';")
    db.session.execute(stmt)
    db.session.commit()
    return render_template("message.html",uid=uid,message="All Books Returned Successfully",fine=0)
@app.route("/extend/<bid>/<uid>")
def extend_time(bid,uid):
    stmt = text(f"select duration_month from book_borrowed where book_id = {bid} and borrowed_by = '{uid}';")
    duration = db.session.execute(stmt).fetchall()[0][0]
    duration +=1
    stmt = text(f"update book_borrowed set duration_month = {duration} where book_id = {bid} and borrowed_by = '{uid}';")
    db.session.execute(stmt)
    db.session.commit()
    return render_template("message.html",uid=uid,message="Borrowed duration extended Successfully",fine=0)




#Admin's Side Code Snippet
@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")

@app.route("/admin_login_confirm",methods = ["GET","POST"])
def admin_login_confirm():
    if(request.method == "POST"):
        aid = request.form['aid']
        password = request.form['password']
        query = admin.query.get({"admin_userid":aid})
        if(query == None):
            return render_template("admin_login.html",data = "Admin Not Found ! Kindly Contact to the Administrator")
        else:
            query = str(query).split("-")
            if(password == query[1]):
                return redirect(url_for("admin_home",data = query[0]))
            else:
                return render_template("admin_login.html",data = "Failed to Log In ! Wrong Credentials")


@app.route("/admin_home/<data>")
def admin_home(data):
    stmt = text(f"select admin_name from admin where admin_userid = '{data}';")
    username = db.session.execute(stmt).fetchall()[0][0]
    stmt = text('select * from book;')
    book_count = len(db.session.execute(stmt).fetchall())
    stmt = text("select * from admin;")
    admin_count = len(db.session.execute(stmt).fetchall())
    stmt = text("select * from user;")
    user_count = len(db.session.execute(stmt).fetchall())
    stmt = text("select sum(quantity) from book_borrowed;")
    book_issued_count = db.session.execute(stmt).fetchall()[0][0]
    return render_template("admin_home.html",data = username,book_count=book_count,admin_count=admin_count,user_count=user_count,uid = data,book_issued_count=book_issued_count)

@app.route("/showbook_admin/<uid>")
def show_books_admin(uid):
    stmt = text("select * from book;")
    books = db.session.execute(stmt).fetchall()
    return render_template("showbook_admin.html",tables = books,uid=uid)

@app.route("/show_admins/<uid>")
def show_admins(uid):
    stmt = text("select admin_userid , admin_name , contact_info from admin;")
    admins = db.session.execute(stmt).fetchall()
    return render_template("showadmin.html",admins = admins,uid=uid)

@app.route("/show_users/<uid>")
def show_users(uid):
    stmt = text("select user_id,user_name,contact_info from user;")
    users = db.session.execute(stmt).fetchall()
    return render_template("show_users.html",users=users,uid=uid)

@app.route("/show_issued_book/<uid>")
def show_issued_book_admin(uid):
    stmt = text("select * from book_borrowed;")
    issued_books = db.session.execute(stmt).fetchall()
    return render_template("show_issued_book.html",uid=uid,issued_books=issued_books)
@app.route("/remove_admin/<uid>/<rem_id>")
def remove_admin(uid,rem_id):
    if(rem_id == uid):
        return render_template("message_admin.html",message = "You cannot remove yourself as an Admin !!",uid=uid)
    else:
        stmt = text(f"delete from admin where admin_userid = '{rem_id}';")
        db.session.execute(stmt)
        db.session.commit()
        return render_template("message_admin.html",message = "Admin Removed Successfully",uid=uid)
    
@app.route("/add/<uid>/<message>")
def add_admin(uid,message):
    if(message == "Admin Form"):
        return render_template("admin_form.html",uid=uid,message=message)
    elif(message == "Book Form"):
        return render_template("admin_form.html",uid=uid,message=message)

@app.route("/add_admin_confirm/<uid>",methods = ["GET","POST"])
def add_admin_confirm(uid):
    if(request.method == "POST"):
        aid = request.form['aid']
        aname = request.form['aname']
        contact = request.form['contact']
        password = request.form['password']
        con_password = request.form['con_password']
        if(password == con_password):
            stmt = text(f"insert into admin values('{aid}','{password}','{aname}','{contact}');")
            try:
                db.session.execute(stmt)
                db.session.commit()
                return render_template("message_admin.html",message = "Admin Added Successfully",uid=uid)
            except  IntegrityError :
                return render_template("message_admin.html",message = "Admin Already Exists",uid=uid)
        else:
            return redirect(url_for("add_admin",uid=uid,message = "Password doesnot matched !! Please try again."))



@app.route("/remove_user/<uid>/<uid_rem>")
def remove_user(uid,uid_rem):
    stmt = text(f"delete from user where user_id = '{uid_rem}';")
    db.session.execute(stmt)
    db.session.commit()
    return render_template("message_admin.html",uid=uid,message = "User Remove Successfully")

@app.route("/remove_all_users/<uid>")
def remove_users_all(uid):
    stmt = text("truncate table user;")
    db.session.execute(stmt)
    db.session.commit()
    return render_template("message_admin.html",uid=uid,message="Users Removed Successfully")

@app.route("/add_book/<uid>",methods = ["GET","POST"])
def add_book(uid):
    if(request.method == "POST"):
        bookid = request.form['bid']
        bookname = request.form['bname']
        author = request.form['author']
        price = request.form['price']
        quantity = request.form['quantity']
        stmt = text(f"insert into book values({bookid},'{bookname}','{author}',{price},{quantity});")
        try:
            db.session.execute(stmt)
            db.session.commit()
        except IntegrityError:
            stmt = text(f"select quantity from book where book_id = {bookid};")
            quant = int(db.session.execute(stmt).fetchall()[0][0])
            quant+=int(quantity)
            stmt = text(f"update book set quantity = {quant} where book_id = {bookid};")
            db.session.execute(stmt)
            db.session.commit()
        return render_template("message_admin.html",uid=uid,message="Book added Successfully")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)