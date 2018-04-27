from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:654321@localhost:8889/blogz' 
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    content = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   
    def __init__(self, name, content, user):
        self.name = name
        self.content = content
        self.user = user

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='user')
   
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'display', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')   

@app.route('/')
def index():
    users=User.query.all()
    return render_template('index.html', users=users)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        error_message = ''
        if user and user.password == password: 
            session ['username'] = username
            return redirect('/addblog')
        else:
            if user and user.password != password:
                error_message = 'Invalid password'
            elif not user:
                error_message = 'username does not exist'
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        username_error = ''
        password_error = ''
        verify_password_error = ''

        if username == '':
            username_error = 'username can not be empty!'
            
        else:
            if len(username) < 3:
                username_error = 'username length cannot be less than 3 characters!'
                    
        if password == '':
            password_error = 'password can not be empty!'
        else:
            if len(password) < 3:
                password_error = 'password length cannot be less than 3 characters!'
                password = ''
        
        if verify == '':
            verify_password_error = 'verify password can not be empty!'
        else:
            if verify != password:
                verify_password_error = 'password does not match!'
                verify = ''

        if not username_error and not password_error and not verify_password_error:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/addblog')
            else:
                username_error = 'username already exists'
        
            return render_template('signup.html', username=username, username_error=username_error)
        else:
            return render_template('signup.html', username_error = username_error, password_error = password_error, verify_password_error = verify_password_error,
            username=username, password=password, verify=verify)

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username'] 
    return redirect('/mainpage')


@app.route('/mainpage', methods=['GET'])
def display():
    id = request.args.get('id')
    user = request.args.get('user')
    blogs = Blog.query.all()
    if (id):
        blog = Blog.query.get(id)
        return render_template('individual.html', blog=blog)
    if (user):
        blogs = Blog.query.all()
        return render_template('singleUser.html', blogs=blogs)




@app.route('/addblog', methods=['POST','GET'])
def addblog():

    if request.method == 'POST':
        blog_name = request.form['blog']
        blog_content = request.form['content']
        name_error = ''
        content_error = ''
        if len(blog_name) < 1 or len(blog_content) < 1:
            name_error = 'name can not be empty!'
            content_error = 'content can not be empty!'
            return render_template('addblog.html', name_error=name_error, content_error = content_error)

        
        new_blog = Blog(blog_name, blog_content, user)
        db.session.add(new_blog)
        db.session.commit()
        variable ='/mainpage?id='+str(new_blog.id)
        return redirect(variable)
    else:
        if request.method == 'GET':
            return render_template('addblog.html')

if __name__ == '__main__':
    app.run()