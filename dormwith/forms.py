from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField , BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from dormwith.models import Student

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[
                                DataRequired(),
                                Length(min=7,max=10)
                            ])
    password = PasswordField('Password',
                                validators=[
                                    DataRequired()
                                ]
                            )
    confirm_password = PasswordField('Confirm Password',
                                validators=[
                                    DataRequired(),
                                    EqualTo('password')
                                ]
                            )
    firstname = StringField('Firstname',
                            validators=[
                                DataRequired(),
                                Length(max=20)
                            ])
    lastname = StringField('Lastname',
                            validators=[
                                DataRequired(),
                                Length(max=20)
                            ])
    birthdate = DateField('Birth Date',#id='register_birthdate',
                            validators=[
                                DataRequired()
                            ])
    ent_year = SelectField('Entrance Year', choices = [(str(i), str(i)) for i in range(2000,2020)],
                            validators=[
                                DataRequired()
                            ])
    edu_field = StringField('Education Field',
                            validators=[
                                DataRequired(),
                                Length(max=20)
                            ])
    city = StringField('City',
                            validators=[
                                DataRequired(),
                                Length(max=20)
                            ])
    submit = SubmitField('Sign Up')

    sen_light = BooleanField('Sensitivity to light')
    sen_sound = BooleanField('Sensitivity to sound')

    def validate_username(self, username):
        student = Student.query.filter_by(username=username.data).first()
        if student:
            print("blah")
            raise ValidationError('This username is taken.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                            validators=[
                                DataRequired()
                            ])
    password = PasswordField('Password',
                                validators=[
                                    DataRequired()
                                ]
                            )
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class AdvForm(FlaskForm):
    message = TextAreaField('Content',
                            validators=[
                                DataRequired()
                            ])
    submit = SubmitField('منتشر کن')


class MeForm(FlaskForm):

    birthdate = DateField('تاریخ تولد')
    ent_year = SelectField('سال ورود', choices = [(str(i), str(i)) for i in range(2000,2020)])
    edu_field = StringField('رشته تحصیلی')
    city = StringField('شهر')
    submit = SubmitField('تغییر ویژگی ها')

    sen_light = BooleanField('حساسیت به نور')
    sen_sound = BooleanField('حساسیت به صدا')
