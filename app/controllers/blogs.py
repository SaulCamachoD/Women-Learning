from flask import render_template, request, redirect, session, flash
from app import app
from app.models.user import User
from app.models.invitation import Invitation
from app.models.message import Message
from app.models.profile import Profile
from app.models.blog import Blog

@app.route('/blog')
def blog():
    data = {}
    info_blogs = Blog.get_all_blog(data)
    return render_template('blog.html', info_blogs = info_blogs)

@app.route('/create_blog')
def create_blog():
    data = {
        "id": session['user_id']
    }
    user=User.get_one_user(data)
    return render_template('create_blog_2.html', user=user)





@app.route('/blog_2', methods = ['POST'])
def blog_2():
    if "user_id" not in session: 
        return redirect('/application')
    data = {
        "id": session['user_id'],
        "content" : request.form['content'] 
    }
    Blog.save_blog(data)
    return redirect('/create_blog')


@app.route('/show_blog/<int:idblog>')
def show_blog(idblog):
    data = {
        "id": idblog,
    }
    blog=Blog.get_by_id(data)
    return render_template('show_blog.html',blog=blog)