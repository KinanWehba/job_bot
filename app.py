from flask import Flask ,request,Response, jsonify
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
    user_status = db.Column(db.String(50), nullable=False, default="trial")
    add_count = db.Column(db.Integer, nullable=False, default=0)
    query_count = db.Column(db.Integer, nullable=False, default=0)
    jobs = db.relationship('Job', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.chat_id}', '{self.user_status}','{self.add_count}','{self.query_count}')"

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.String(200), nullable=False)
    organization = db.Column(db.String(100))
    job_status = db.Column(db.String(50), nullable=False, default="activate")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    details = db.relationship('JobDetail', backref='job', lazy=True)

    def __repr__(self):
        return f"Job('{self.job_title}', '{self.job_description}', '{self.organization}', '{self.job_status}', '{self.user_id}', '{self.category_id}')"

class JobDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    detail_name = db.Column(db.String(100), nullable=False)
    detail_title = db.Column(db.String(200), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    def __repr__(self):
        return f"Job('{self.detail_name}', '{self.detail_title}', '{self.job_id}')"
    
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
        fname = kwarg.get("fname")
        lname = kwarg.get("lname")
        user_add = User(
            fname=fname,
            chat_id=chat_id,
            username=username,
            lname=lname)
        db.session.add(user_add)
        db.session.commit()
        user = user_add
    about_user = { "username" : user.username,
                    "fname" : user.fname,
                    "lname" : user.lname,
                    "chat_id" : user.chat_id,
                    "user_status" : user.user_status,
                    "user_id" : user.id,}
    return about_user

def category_info(category_name):
    category = Category.query.filter_by(category_name=category_name).first()
    if not category :
        category_add = Category(category_name=category_name,)
        db.session.add(category_add)
        db.session.commit()
        category_id = category_add.id
    else :
        category_id = category.id
    return category_id


def job_info(job_id=None,**kwarg):
    chat_id= kwarg.get("chat_id")
    category=kwarg.get("category")
    job_title=kwarg.get("job_title")
    job_description=kwarg.get("job_description")
    organization=kwarg.get("organization")
    user = user_info(chat_id)
    user_id = user.get("user_id")
    if not job_id :
        condition = (category and job_title and job_description)
        if condition :
            category_id = category_info(category)
            if not organization :
                organization = "غير محدد"
            job_add = Job(
                job_title=job_title,
                job_description=job_description,
                user_id=user_id,
                category_id=category_id,
                organization=organization,)
            db.session.add(job_add)
            db.session.commit()
            job_id = job_add.id
        about_job = { "job_id" : job_id,
                "organization" : organization,
                "category" : category,
                "job_title" : job_title,
                "job_description" : job_description,}
        return about_job

@app.route("/start")
def start():
    chat_id = request.args.get("chat_id")
    user = user_info(chat_id,
            username = request.args.get("username"),
            fname = request.args.get("fname") ,
            lname = request.args.get("lname"),)
    user_status = user.get("user_status")
    
    return user_status

@app.route("/add_job")
def add_job():
    job = job_info(chat_id= request.args.get("chat_id"),
                   category=request.args.get("المسمى الوظيفي"),
                   job_title=request.args.get("عنوان العمل"),
                   job_description=request.args.get("تفصيل العمل"),
                   organization=request.args.get("اسم المؤسسة"))
    job = jsonify(job)



    return job



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

