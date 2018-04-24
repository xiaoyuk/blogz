from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:123456@localhost:8889/build-a-blog' 
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    content = db.Column(db.String(120))
   
    def __init__(self, name, content):
        self.name = name
        self.content = content


@app.route('/mainpage', methods=['GET'])
def display():
    id = request.args.get('id', -1, type=int)
    if id != -1:
        blog = Blog.query.get(id)
        return render_template('individual.html', blog=blog)
    else:
        blogs = Blog.query.all()
        return render_template('mainpage.html', title="Build a Blog!", blogs=blogs)



@app.route('/addblog', methods=['POST','GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['blog']
        blog_content = request.form['content']
        name_error = ''
        content_error = ''
        if len(blog_name) < 1 or len(blog_content) < 1:
            name_error = 'name can not be empty!'
            content_error = 'content can not be empty!'
            return render_template('addblog.html', name_error=name_error, content_error = content_error)

        
        new_blog = Blog(blog_name, blog_content)
        db.session.add(new_blog)
        db.session.commit()
        variable ='/mainpage?id='+str(new_blog.id)
        return redirect(variable)
    else:
        if request.method == 'GET':
            return render_template('addblog.html')

if __name__ == '__main__':
    app.run()