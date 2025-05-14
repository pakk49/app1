from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
import plotly.express as px
import pandas as pd
import json

import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical.db'

# Setup logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/medical_app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Medical analysis app startup')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# โมเดลผู้ใช้
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    id_card = db.Column(db.String(13), unique=True, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    allergies = db.Column(db.Text)
    conditions = db.Column(db.Text)
    consultations = db.relationship('Consultation', backref='user', lazy=True)

# โมเดลการวิเคราะห์อาการ
class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    severity = db.Column(db.String(20))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# เส้นทางหน้าหลัก
@app.route('/')
def index():
    return render_template('index.html')

# เส้นทางการลงทะเบียน
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        id_card = request.form['id_card']
        birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d')
        gender = request.form['gender']
        allergies = request.form['allergies']
        conditions = request.form['conditions']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password, full_name=full_name,
                   id_card=id_card, birth_date=birth_date, gender=gender,
                   allergies=allergies, conditions=conditions)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('ลงทะเบียนสำเร็จ กรุณาเข้าสู่ระบบ', 'success')
            return redirect(url_for('login'))
        except:
            flash('เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง', 'danger')

    return render_template('register.html')

# เส้นทางการเข้าสู่ระบบ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('เข้าสู่ระบบไม่สำเร็จ กรุณาตรวจสอบข้อมูลอีกครั้ง', 'danger')

    return render_template('login.html')

# เส้นทางการวิเคราะห์อาการ
from medical_analysis import analyze_symptoms

@app.route('/analyze', methods=['GET', 'POST'])
@login_required
def analyze():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        symptoms = request.form.getlist('symptoms')
        
        # คำนวณ BMI
        bmi = weight / ((height/100) ** 2)
        
        # วิเคราะห์อาการ
        condition_scores, severity, recommendations = analyze_symptoms(symptoms, bmi)
        
        # บันทึกการวิเคราะห์
        consultation = Consultation(
            user_id=current_user.id,
            weight=weight,
            height=height,
            symptoms=json.dumps(symptoms),
            diagnosis=json.dumps(condition_scores),
            recommendations=json.dumps(recommendations),
            severity=severity
        )
        db.session.add(consultation)
        db.session.commit()
        
        return redirect(url_for('results', consultation_id=consultation.id))

    return render_template('analyze.html')

# เส้นทางแสดงผลการวิเคราะห์
@app.route('/results/<int:consultation_id>')
@login_required
def results(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    if consultation.user_id != current_user.id:
        flash('คุณไม่มีสิทธิ์เข้าถึงข้อมูลนี้', 'danger')
        return redirect(url_for('dashboard'))
    
    symptoms = json.loads(consultation.symptoms)
    diagnosis = json.loads(consultation.diagnosis) if consultation.diagnosis else {}
    recommendations = json.loads(consultation.recommendations) if consultation.recommendations else []
    
    # สร้างกราฟ BMI
    bmi = consultation.weight / ((consultation.height/100) ** 2)
    
    # จัดเรียงผลการวินิจฉัยตามเปอร์เซ็นต์
    sorted_conditions = sorted(diagnosis.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return render_template('results.html', 
                         consultation=consultation,
                         symptoms=symptoms,
                         bmi=bmi,
                         conditions=sorted_conditions,
                         recommendations=recommendations)

# เส้นทางแดชบอร์ด
@app.route('/dashboard')
@login_required
def dashboard():
    consultations = Consultation.query.filter_by(user_id=current_user.id).all()
    
    # คำนวณอายุปัจจุบัน
    now = datetime.utcnow()
    
    # สร้างกราฟแนวโน้ม BMI
    if consultations:
        df = pd.DataFrame([
            {
                'date': c.date,
                'bmi': c.weight / ((c.height/100) ** 2)
            } for c in consultations
        ])
        fig = px.line(df, x='date', y='bmi', title='แนวโน้ม BMI')
        bmi_graph = fig.to_html(full_html=False)
    else:
        bmi_graph = None

    return render_template('dashboard.html', 
                         consultations=consultations, 
                         bmi_graph=bmi_graph,
                         now=now)

# เส้นทางลืมรหัสผ่าน
# เส้นทางการออกจากระบบ
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ออกจากระบบสำเร็จ', 'success')
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        id_card = request.form['id_card']
        user = User.query.filter_by(username=username, id_card=id_card).first()
        
        if user:
            # ในที่นี้ควรส่งอีเมลยืนยันตัวตน แต่เราจะทำเป็นตัวอย่างอย่างง่าย
            flash('กรุณาติดต่อผู้ดูแลระบบเพื่อรีเซ็ตรหัสผ่าน', 'info')
            return redirect(url_for('login'))
        else:
            flash('ไม่พบข้อมูลผู้ใช้', 'danger')

    return render_template('forgot_password.html')

# Custom template filter for JSON
@app.template_filter('from_json')
def from_json(value):
    return json.loads(value) if value else []

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
