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
    status = db.Column(db.String(50), nullable=False, default="trial")
    add_count = db.Column(db.Integer, nullable=False, default=0)
    query_count = db.Column(db.Integer, nullable=False, default=0)
    jobs = db.relationship('Job', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.chat_id}', '{self.status}','{self.add_count}','{self.query_count}')"

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.String(200), nullable=False)
    organization = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Job('{self.title}', '{self.description}', '{self.user_id}', '{self.category_id}')"
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    categorys = db.relationship('Job', backref='category', lazy=True)
    def __repr__(self):
        return f"Category('{self.category_name}'"



# def find_user_by_job_id(job_id):
#     user = User.query.join(Job).filter(Job.id == job_id).first()
#     return user
# # تحديد job_id الذي تبحث عنه
# job_id_to_find = 1  # استبدل بقيمة job_id الفعلية

# # استخدام الدالة للعثور على المستخدم
# found_user = find_user_by_job_id(job_id_to_find)
def user_info(chat_id,**kwarg):
    user = User.query.filter_by(chat_id=chat_id).first()
    if not user :
        username = kwarg.get("username")
        print(username)
        fname = kwarg.get("fname")
        lname = kwarg.get("lname")
        user_add = User(
            fname=fname,
            chat_id=chat_id,
            username=username,
            lname=lname)
        db.session.add(user_add)
        db.session.commit()
        db.session.remove()
        user = User.query.filter_by(chat_id=chat_id).first()
    about_user = { "username" : user.username,
                    "fname" : user.fname,
                    "lname" : user.lname,
                    "chat_id" : user.chat_id,
                    "status" : user.status,
                    "id" : user.id,}
    return about_user

def category_info(category_name):
    category = Category.query.filter_by(category_name=category_name).first()
    if not category :
        category_add = Category(category_name=category_name,)
        db.session.add(category_add)
        db.session.commit()
        db.session.remove()
        category = Category.query.filter_by(category_name=category_name).first()
    category_id = category.id
    return category_id

@app.route("/start")
def start():
    username = request.args.get("username")
    fname = request.args.get("fname")
    lname = request.args.get("lname")
    chat_id = request.args.get("chat_id")
    user = user_info(chat_id,username = username,fname = fname ,lname = lname)
    user_status = user.get("status")
    return user_status

@app.route("/add_job")
def add_job():
    chat_id = request.args.get("chat_id")
    user = user_info(chat_id)
    user_id = user.get("id")
    category = request.args.get("*المسمى الوظيفي")
    job_title = request.args.get("*عنوان الاعلان")
    job_description = request.args.get("*نص الاعلان")
    condition =  (category and job_title and job_description)
    if condition :
        category_id = category_info(category)
        organization = request.args.get("اسم المؤسسة")
        if not organization :
            organization = "غير محدد"
        job_add = Job(
            job_title=job_title,
            job_description=job_description,
            user_id=user_id,
            category_id=category_id,
            job_organization=organization,)
        db.session.add(job_add)
        db.session.commit()
        db.session.remove()
        return "add"


    else :

        return "error"
    # fname = request.args.get("fname")
    # lname = request.args.get("lname")
    # chat_id = request.args.get("chat_id")
    # user = User.query.filter_by(chat_id=chat_id).first()
    # if user is None:
    #     user_add = User(
    #         fname=fname,
    #         chat_id=chat_id,
    #         username=username,
    #         lname=lname)
    #     db.session.add(user_add)
    #     db.session.commit()
    #     user_status = "new"
    # elif chat_id == '443176203' :
    #     user.status = 'manager'
    #     db.session.commit()
    #     user_status = 'manager'
    # else:
    #     user_status = user.status
    # db.session.remove()
    return "user_status"



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

