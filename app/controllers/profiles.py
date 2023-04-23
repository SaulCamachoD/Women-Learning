from flask import render_template, request, redirect, session, flash
from app import app
from app.models.user import User
from app.models.profile import Profile
from app.models.blog import Blog
import os

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/create', methods=['POST'])
def create():
    age = request.form['age']
    native_language = request.form['native_language']
    language_of_interest = request.form['language_of_interest']
    level = request.form['level']
    interest = request.form['interest']
    photo = request.files['photo']
    filename = photo.filename
    filepath = os.path.join(app.static_folder, 'files', filename)
    photo.save(filepath)
    data = { 
        "age": age,
        "native_language": native_language,
        "language_of_interest": language_of_interest,
        "level": level,
        "interest": interest,
        "user_id": session['user_id'],
        "photo": filepath.replace(app.static_folder, app.static_url_path)
    }
    Profile.save(data)
    return redirect('/perfiles')


@app.route('/perfiles')
def view_profiles():
        data ={ 
            "id" : session['user_id'],
        }
        profiles = Profile.get_by_user(data)
        return render_template('perfiles.html', profiles=profiles)

@app.route( '/profile/<idProfile>/destroy', methods=["POST"] )
def profile_destroy( idProfile ):
        data = {
            "id": int(idProfile),
        }
        Profile.destroy( data )
        return redirect ('/perfiles')


@app.route('/perfiles/new')
def new_perfiles():
    return "Hello World"

