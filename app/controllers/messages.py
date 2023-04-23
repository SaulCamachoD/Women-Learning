from flask import render_template, request, redirect, session, flash
from app import app
from app.models.message import Message
from app.models.invitation import Invitation

@app.route('/messages')
def view_messages():
        if "user_id" not in session: 
                return redirect('/application')
        data ={ 
        "id" : session['user_id'],
        }
        messages = Message.get_by_user(data)
        return render_template('messages.html', messages=messages)

@app.route('/message/<idInvitation>', methods=['POST'])
def message(idInvitation):
        data = {
        "id": int(idInvitation),
        }
        Invitation.decline( data )
        return render_template('message.html', idFriend=request.form["idFriend"])

@app.route('/message/<idFriend>/confirm', methods=['POST'])
def message_per(idFriend):
        data ={
        "message": request.form['message'],
        "inviter_id": int(idFriend), #observación
        "friend_id" : session['user_id'], #observación
        }
        Message.save(data)
        return redirect ('/dashboard')

@app.route('/message/<idFriend>/answer', methods=['POST'])
def message_answer(idFriend):
        return render_template('message.html', idFriend=idFriend)

@app.route( '/message/<idMessage>/destroy', methods=["POST"] )
def message_destroy( idMessage ):
        data = {
        "id": int(idMessage),
        }
        Message.destroy( data )
        return redirect ('/messages')