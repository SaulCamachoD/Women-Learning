from app.config.mysqlconnection import connectToMySQL
from app import app
import os
from flask import flash


class Profile:
    db_name = 'speak_db'
    def __init__(self,data):
        self.id = data['id']
        self.age = data['age']
        self.native_language = data['native_language']
        self.language_of_interest = data['language_of_interest']
        self.level = data['level']
        self.photo = data['photo']
        self.interest = data['interest']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM profiles;"
        results = connectToMySQL(cls.db_name).query_db(query)
        profiles = []
        for row in results:
            profiles.append( cls(row))
        return profiles
    
    @classmethod
    def get_all_info_photo(cls):
        query = "SELECT profiles.photo, profiles.age, profiles.interest, profiles.user_id, profiles.native_language, profiles.language_of_interest, profiles.level, users.name FROM profiles JOIN users ON profiles.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        profiles = []
        for row in results:
            profile_data = {
                'photo': os.path.join(app.static_url_path, row['photo']),
                'age': row['age'],
                'interest': row['interest'],
                'user_id': row['user_id'],
                'native_language': row['native_language'],
                'language_of_interest': row['language_of_interest'],
                'level': row['level'],
                'name': row['name']

            }
            profiles.append(profile_data)
        return profiles
    
    @classmethod #or get one
    def get_by_id(cls,data):
        query = "SELECT * FROM profiles WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_by_name(cls,data):
        query = "SELECT * FROM users JOIN profiles ON profiles.user_id = users.id WHERE users.name = %(name)s;"
        result = connectToMySQL( "speak_db" ).query_db( query, data )
        result = result[0]['id']
        if not result:
            result = 0
        return result

    @classmethod
    def get_by_user(cls, data):
        query = "SELECT * FROM profiles JOIN users ON users.id = profiles.user_id WHERE profiles.user_id = %(id)s;"
        results = connectToMySQL( "speak_db" ).query_db( query, data )
        profiles = []
        for row in results:
            profiles.append( cls(row))
        return profiles

    @classmethod
    def save(cls,data):
        query = "INSERT INTO profiles(age,native_language,language_of_interest,level,interest,user_id,photo,created_at,updated_at) VALUES(%(age)s, %(native_language)s,%(language_of_interest)s,%(level)s,%(interest)s,%(user_id)s,%(photo)s,NOW(), NOW());"
        result = connectToMySQL( "speak_db" ).query_db( query, data )
        return result

    @classmethod
    def destroy( cls, data ):
        query = "DELETE FROM profiles WHERE id = %(id)s;"
        connectToMySQL( "speak_db" ).query_db( query, data )

