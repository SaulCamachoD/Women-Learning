from flask import render_template, request, redirect, session, flash
from app import app
from app.models.user import User
from app.models.invitation import Invitation
from app.models.message import Message
from app.models.profile import Profile

@app.route('/invite')
def invite():
    return render_template('invite.html')

@app.route('/invite_person/<idFriend>', methods=['POST'])
def invite_per(idFriend):
        data ={
            "inviter_id": session['user_id'],
            "friend_id" : int(idFriend),
        }
        Invitation.save(data)
        return redirect ('/dashboard')

@app.route( '/invitation/<idInvitation>/accepted', methods=["POST"] )
def accepted( idInvitation ):
        data = {
            "id": int(idInvitation),
        }
        Invitation.decline( data )
        return redirect ('/dashboard')

@app.route( '/invitation/<idInvitation>/destroy', methods=["POST"] )
def decline( idInvitation ):
        data = {
            "id": int(idInvitation),
        }
        Invitation.decline( data )
        return redirect ('/dashboard')