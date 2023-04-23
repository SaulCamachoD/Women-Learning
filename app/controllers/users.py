from flask import render_template, request, redirect, session, flash
from app import app
from app.models.user import User
from app.models.profile import Profile
from app.models.invitation import Invitation
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/application') 
def form():
    return render_template('application.html')


@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/application')
    data ={ 
        "name": request.form['name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email/Password","login")
        return redirect('/application')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect('/application')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session: 
        return redirect('/application')
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    invitations = Invitation.get_by_user(data)
    return render_template('dashboard.html', user=user, invitations=invitations)


@app.route('/user/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    User.destroy(data)
    return redirect('/users')


@app.route('/message')
def messages():
    return render_template('message.html')


@app.route('/community')
def community():
    if "user_id" not in session: 
        return redirect('/application')
    age = request.args.get('age')
    native_language = request.args.get('native_language')
    language_of_interest = request.args.get('language_of_interest')
    level = request.args.get('level')

    profiles = Profile.get_all_info_photo()

    if age:
        profiles = [p for p in profiles if p['age'] == int(age)]
    if native_language:
        profiles = [p for p in profiles if p['native_language'] == native_language]
    if language_of_interest:
        profiles = [p for p in profiles if p['language_of_interest'] == language_of_interest]
    if level:
        profiles = [p for p in profiles if p['level'] == level]

    return render_template('community.html', community=profiles)

@app.route( '/view/<idUser>', methods=["GET"] )
def view( idUser ):
    if "user_id" not in session: 
        return redirect('/application')
    data = {
        "id": int(idUser),
    }
    user = User.get_by_id( data )
    profiles = Profile.get_by_user(data)
    return render_template('view.html', user=user, profiles=profiles)


@app.route('/show/<int:idUser>')
def show(idUser):
    data = {
        "id": idUser,
    }
    user_data = User.get_one_user(data)
    return render_template('show_user.html', user_data=user_data)


@app.route('/invite_person', methods=['POST'])
def invite_person():
        data ={
            "name": request.form['name'],
        }
        friend_id = Profile.get_by_name(data)
        data ={
            "inviter_id": session['user_id'],
            "friend_id" : friend_id,
        }
        Invitation.save(data)
        return redirect ('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


