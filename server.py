from app import app
from app.controllers import users
from app.controllers import profiles
from app.controllers import invitations
from app.controllers import messages
from app.controllers import blogs
from app.controllers import books


if __name__=="__main__":
    app.run(debug=True)