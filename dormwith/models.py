from datetime import datetime ,date
from dormwith import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(student_id):
    return Student.query.get(student_id)



class Student(db.Model, UserMixin):
    id          =   db.Column(db.Integer    , primary_key = True)
    username    =   db.Column(db.String(10) , unique = True     , nullable = False)
    password    =   db.Column(db.String(25) , nullable = False)
    firstname   =   db.Column(db.String(25) , nullable = False)
    lastname    =   db.Column(db.String(25) , nullable = False)
    birthdate   =   db.Column(db.Date       , nullable = False)
    city        =   db.Column(db.String(20) , nullable = False)
    edu_field   =   db.Column(db.String(20) , nullable = False)
    ent_year    =   db.Column(db.Date       , nullable = False)
    sen_sound   =   db.Column(db.Boolean    , nullable = False  , default = 0)
    sen_light   =   db.Column(db.Boolean    , nullable = False  , default = 0)
    advs        =   db.relationship('Adv' ,backref = 'advertiser' , lazy = True )
    reqs        =   db.relationship('Req' ,backref = 'requester' , lazy = True )

    def __repr__(self):
        return  f"Student('{self.username}','{self.password}', '{self.firstname}', '{self.lastname}', '{self.birthdate}','{self.city}', '{self.edu_field}','{self.ent_year}')"


class Adv(db.Model):
    id          =   db.Column(db.Integer    , primary_key = True)
    message     =   db.Column(db.Text   )
    date_adv    =   db.Column(db.DateTime , nullable = False , default =  datetime.utcnow)
    std_id      =   db.Column(db.Integer , db.ForeignKey('student.id') , nullable = False)
    reqs        =   db.relationship('Req' ,backref = 'related_advertisement' , lazy = True )

    def __repr__(self):
        return  f"Adv('{self.message}' , '{self.date_adv}','{self.std_id}' , '{self.reqs}'  )"

class Req(db.Model):
    id          =   db.Column(db.Integer    , primary_key = True)
    date_req    =   db.Column(db.DateTime , nullable = False , default =  datetime.utcnow)
    std_id      =   db.Column(db.Integer , db.ForeignKey('student.id') , nullable = False)
    adv_id      =   db.Column(db.Integer , db.ForeignKey('adv.id') , nullable = False)
    status      =   db.Column(db.Integer , nullable = False , default = 0)   # 1 reject   , 2 accept , 0 Not seen

    def __repr__(self):
        return  f"Req('{self.std_id}' , '{self.adv_id}' , '{self.date_req}')"
