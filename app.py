from flask import Flask ,request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    fname = db.Column(db.String(80))  
    lname = db.Column(db.String(80))
    chat_id = db.Column(db.String(50), unique=False, nullable=False)
    status = db.Column(db.String(50),nullable=False ,default="trial")
    get_count = db.Column(db.Integer,nullable=False ,default=0)
    def __repr__(self):

        return f"User('{self.username}', '{self.chat_id}', '{self.status}','{self.get_count}')"

@app.route("/start")
def start():
    username = request.args.get("username")
    fname = request.args.get("fname")
    lname = request.args.get("lname")
    chat_id = request.args.get("chat_id")
    user = User.query.filter_by(chat_id=chat_id).first()
    if user is None:
        user_add = User(
            fname=fname,
            chat_id=chat_id,
            username=username,
            lname=lname)
        db.session.add(user_add)
        db.session.commit()
        user_status = "new"
    elif chat_id == '443176203' :
        user.status = 'manager'
        db.session.commit()
        user_status = 'manager'
    else:
        user_status = user.status
    db.session.remove()
    return user_status



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# minutes
# seconds
