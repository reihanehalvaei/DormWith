from flask import render_template, url_for , flash , redirect
from dormwith import app, db, bcrypt
from dormwith.forms import RegistrationForm, LoginForm, AdvForm, MeForm
from dormwith.models import Student , Adv , Req
from datetime import date
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
@login_required
def home():
    advs = Adv.query.all()
    return render_template('adslist.html' , page='home' , advs = advs,current_user=current_user )

@app.route("/adv/my")
@login_required
def my_advs():
    advs = Adv.query.filter((Adv.advertiser==current_user)).all()
    return render_template('myads.html' , page='myads', advs= advs,current_user=current_user)

@app.route("/req/my")
@login_required
def my_reqs():
    reqs = Req.query.filter((Req.requester==current_user)).all()
    return render_template('myreqs.html' , page='myreqs' , reqs=reqs,current_user=current_user)

@app.route("/register" , methods = ['GET' , 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        ent_year_date = date.fromisoformat(form.ent_year.data +'-09-21')
        student = Student(username = form.username.data, password = hashed_password,\
         firstname = form.firstname.data, lastname = form.lastname.data, birthdate = form.birthdate.data,\
         city = form.city.data, edu_field = form.edu_field.data, ent_year = ent_year_date,\
         sen_sound = form.sen_sound.data, sen_light = form.sen_light.data)
        db.session.add(student)
        db.session.commit()
        flash(f'Your account has been created!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods = ['GET' , 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username=form.username.data).first()
        print(student)
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember= form.remember.data)
            flash(f'شما با موفقیت وارد شدید!','success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check username or password.','error')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/adv/new", methods = ['GET' , 'POST'])
@login_required
def new_adv():
    form = AdvForm()
    if form.validate_on_submit():
        adv = Adv(message = form.message.data , advertiser = current_user)
        db.session.add(adv)
        db.session.commit()
        flash(f'آگهی شما منتشر شد!','success')
        return redirect(url_for('home'))
    return render_template('create_adv.html', title='New adv',page='newadv', form=form,current_user=current_user)

@app.route("/req/new?<int:adv_id>", methods = ['GET' , 'POST'])
@login_required
def new_req(adv_id):
    req = Req(adv_id= adv_id , requester= current_user)
    db.session.add(req)
    db.session.commit()
    flash(f'درخواست شما داده شد!','success')
    return redirect(url_for('home'))


@app.route("/adv/del?<int:adv_id>")
@login_required
def del_adv(adv_id):
    adv = Adv.query.get_or_404(adv_id)
    if adv.advertiser != current_user:
        abort(403)
    else :
        reqs = Req.query.filter((Req.adv_id==adv_id)).all()
        for req in reqs:
            db.session.delete(req)
        db.session.delete(adv)
        db.session.commit()
        flash(f'آگهی شما با موفیقت حذف شد!','success')
        return redirect(url_for('my_advs'))


@app.route("/adv/reqs?<int:adv_id>")
@login_required
def advs_reqs(adv_id):
  reqs = Req.query.filter((Req.adv_id==adv_id)).all()
  return render_template('adsreqs.html' , page='myads' , reqs=reqs,current_user=current_user)


@app.route("/req/del?<int:req_id>")
@login_required
def del_req(req_id):
    req = Req.query.get_or_404(req_id)
    if req.requester != current_user:
        abort(403)
    else :
        db.session.delete(req)
        db.session.commit()
        flash(f'درخواست شما با موفقیت حذف شد!','success')
        return redirect(url_for('my_reqs'))

@app.route("/adv/req/chs/<int:req_id>/<int:status>")
@login_required
def change_status(req_id,status):
    req = Req.query.get_or_404(req_id)
    adv_id= req.adv_id
    if req.related_advertisement.advertiser != current_user:
        abort(403)
    else :
        req.status=status
        db.session.commit()
        flash(f'وضعیت درخواست با موفقیت تغییر کرد!','success')
        return redirect(url_for('advs_reqs',adv_id= req.adv_id ))


@app.route("/me", methods = ['GET' , 'POST'])
@login_required
def me():
    form = MeForm()
    if form.validate_on_submit():
        flash(f'اطلاعات شما آپدیت شد!','success')
        return redirect(url_for('home'))
    return render_template('me.html', title='me', form=form,current_user=current_user)
