from app.config.mysqlconnection import connectToMySQL
from flask import flash


class Message:
    db_name = "speak_db"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.message = db_data['message']
        self.inviter_id = db_data['inviter_id']
        self.friend_id = db_data['friend_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']


    #  Get All messages
    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM messages LEFT JOIN users ON users.id = messages.user_id LEFT JOIN invitations ON invitations.id = messages.user_id WHERE invite.id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        messages = []
        for row in results:
            data = {
              "id": row["id"],
              "message": row["message"],
              "user_id": row["user_id"],
              "invite_id": row["invite_id"],
              "created_at": row["created_at"],
              "updated_at": row["updated_at"],
              "user": row["name"] + "",
            }
            messages.append(cls(data))
        return messages

    # Create Message
    @classmethod
    def save(cls, data):
      query = "INSERT INTO messages(message, inviter_id, friend_id, created_at, updated_at) VALUES(%(message)s,%(inviter_id)s ,%(friend_id)s,NOW(),NOW());"
      result = connectToMySQL( "speak_db" ).query_db( query, data )
      return result

    @classmethod
    def get_by_user(cls, data):
      query = "SELECT * FROM messages JOIN users ON users.id = messages.friend_id WHERE messages.inviter_id = %(id)s;"
      results = connectToMySQL(cls.db_name).query_db(query,data)
      return results

    @classmethod
    def destroy( cls, data ):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        connectToMySQL( "speak_db" ).query_db( query, data )

    @staticmethod
    def validate_message(message):
      is_valid = True
      if len(message["message"]) < 1:
          is_valid = False
          flash("Message cannot be empty.", "message")
      return is_valid
