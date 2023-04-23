from app.config.mysqlconnection import connectToMySQL
from flask import flash

class Invitation:
    db_name = "speak_db"
    def __init__(self,db_data):
        self.id = db_data['id']
        self.inviter_id = db_data['inviter_id']
        self.friend_id= db_data['friend_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO invitations(inviter_id, friend_id, created_at, updated_at) VALUES (%(inviter_id)s,%(friend_id)s, NOW(), NOW());"
        result = connectToMySQL( "speak_db" ).query_db( query, data )
        return result   
    
    @classmethod
    def get_all_invitations(cls, inviter_id):
        query = "SELECT COUNT(*) AS all_invitations FROM invitations WHERE user_id = %(user_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, {'inviter_id': str(inviter_id)})
        return result[0]['all_invitations'] if result else 0

    @classmethod
    def get_some_invitations(cls, user_id):
        query = "SELECT users.id, COUNT(invitations.invited) AS invitations_from_some, users.name FROM invitations INNER JOIN users ON invitations.inviter_id = users.id GROUP BY users.id;"
        result = connectToMySQL(cls.db_name).query_db(query)
        user_invitation = {res['id']: res['invitations_from_some'] for res in result}
        return user_invitation.get(user_id, 0)

    @classmethod
    def get_invitations_accepted(cls, user_id):
        query = "SELECT users.name as user_name, invitations.friend_id as inviter_id, COUNT(*) as invited_count FROM invitations JOIN users ON invitations.friend_id = users.id WHERE invitation.inviter_id = %(inviter_id)s GROUP BY invites.inviter_id, users.name;"
        data = {'user_id': user_id}
        result = connectToMySQL(cls.db_name).query_db(query, data)
        user_invitation = {res['user_name']: res['invitated_count'] for res in result}
        return user_invitation
    
    @classmethod
    def get_invitations_denied(cls, user_id):
        query = "SELECT users.name as user_name, invitations.friend_id as inviter_id, COUNT(*) as invited_count FROM invitations JOIN users ON invitations.friend_id = users.id WHERE invitation.inviter_id = %(inviter_id)s GROUP BY invitation.inviter_id, users.name;"
        data = {'user_id': user_id}
        result = connectToMySQL(cls.db_name).query_db(query, data)
        user_pokes = {res['user_name']: res['invitated_count'] for res in result}
        return user_pokes

    @classmethod
    def get_by_user(cls, data):
        query = "SELECT * FROM invitations JOIN profiles ON profiles.id = invitations.friend_id JOIN users ON users.id = invitations.inviter_id  WHERE invitations.friend_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        
        return results
    
    @classmethod
    def decline( cls, data ):
        query = "DELETE FROM invitations WHERE id = %(id)s;"
        connectToMySQL( "speak_db" ).query_db( query, data )