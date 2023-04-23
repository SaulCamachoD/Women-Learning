from app.config.mysqlconnection import connectToMySQL
from app import app
import os
import re	# the regex module

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db_name = 'speak_db'
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # FOR  REGISTER 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users
    
    # FOR  REGISTER 
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (name,email,password,created_at,updated_at) VALUES(%(name)s,%(email)s,%(password)s,NOW(),NOW());"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    # FOR  REGISTER AND LOGIN
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_one_user(cls,data):
        query = "SELECT users.name, users.email, profiles.age, profiles.level, profiles.photo, profiles.native_language, profiles.language_of_interest FROM users JOIN profiles ON users.id = profiles.user_id WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        get_one = []
        for row in results:
            profile_data = {
                'photo': os.path.join(app.static_url_path, row['photo']),
                'age': row['age'],
                'native_language': row['native_language'],
                'language_of_interest': row['language_of_interest'],
                'level': row['level'],
                'name': row['name'],
                'email': row['email']
            }
            get_one.append(profile_data)
        return get_one

    # FOR  PROFILE
    @classmethod
    def save_profile(cls,data):
        query = "INSERT INTO profiles (alias,email,password,created_at,updated_at) VALUES(%(name)s,%(email)s,%(password)s,NOW(),NOW());"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results
    
    # FOR  PROFILE
    @classmethod
    def gell_all_profile(cls,data):
        query  = "SELECT * FROM profiles;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        profiles = []
        for row in results:
            profiles.append( cls(row))
        return profiles

    @classmethod
    def send_invitation(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;" 
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(user['name']) < 3:
            flash("Name must be at least 3 characters","register")
            is_valid= False
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid
