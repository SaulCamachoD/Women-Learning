from flask import render_template
from app import app

@app.route('/books') 
def books():
    return render_template('books.html')