from app.config.mysqlconnection import connectToMySQL
from flask import flash

class Blog:
    db_name = "speak_db"
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save_blog(cls, data):
        query = "INSERT INTO blogs (content, user_id) VALUES (%(content)s,%(id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_all_blog(cls, data):
        query = "SELECT users.name, blogs.id, blogs.content FROM users JOIN blogs ON users.id = blogs.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        blogs = []
        for row in results:
            data_blog = {
                'name':(row['name']),
                'id':(row['id']),
                'content': (row['content']),
            }
            blogs.append(data_blog)
        return blogs


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT blogs.id,blogs.content FROM blogs WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        get_one_blog = []
        for row in results:
            profile_data = {
                'id': row['id'],
                'content': row['content']
            }
            get_one_blog.append(profile_data)
        return get_one_blog