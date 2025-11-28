from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET',
                                          'your-secret-key-change-this')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

Base = declarative_base()

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db_session = Session()


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    contact = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    complaints = relationship('Complaint', backref='user', lazy=True)

    # 👇 seller relationship (uses seller_id)
    waste_sales = relationship('WasteSale',
                               back_populates='seller',
                               foreign_keys='WasteSale.seller_id')

    # 👇 buyer relationship (uses buyer_id)
    purchases = relationship('WasteSale',
                             back_populates='buyer',
                             foreign_keys='WasteSale.buyer_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Bin(Base):
    __tablename__ = 'bins'

    id = Column(Integer, primary_key=True)
    bin_code = Column(String(50), unique=True, nullable=False)
    location = Column(String(100), nullable=False)
    recyclable_weight = Column(Float, default=0.0)
    non_recyclable_weight = Column(Float, default=0.0)
    capacity = Column(Float, default=100.0)
    last_cleaned = Column(DateTime)
    status = Column(String(20), default='Enough Space')
    created_at = Column(DateTime, default=datetime.utcnow)

    def get_fill_percentage(self):
        total_weight = self.recyclable_weight + self.non_recyclable_weight
        return (total_weight / self.capacity) * 100 if self.capacity > 0 else 0

    def update_status(self):
        fill_pct = self.get_fill_percentage()
        if fill_pct >= 80:
            self.status = 'Urgent'
        elif fill_pct >= 50:
            self.status = 'Medium'
        else:
            self.status = 'Enough Space'


class Complaint(Base):
    __tablename__ = 'complaints'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(100))
    status = Column(String(20), default='Pending')
    created_at = Column(DateTime, default=datetime.utcnow)


class WasteSale(Base):
    __tablename__ = 'waste_sales'

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    buyer_id = Column(Integer, ForeignKey('users.id'))
    waste_type = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    description = Column(Text)
    image_path = Column(String(255))
    location = Column(String(100), nullable=False)
    price = Column(Float)
    status = Column(String(20), default='Available')
    created_at = Column(DateTime, default=datetime.utcnow)

    # 👇 Match back_populates exactly (no backref)
    seller = relationship('User',
                          foreign_keys=[seller_id],
                          back_populates='waste_sales')
    buyer = relationship('User',
                         foreign_keys=[buyer_id],
                         back_populates='purchases')


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(int(user_id))


def role_required(role):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash(
                    'Access denied. You do not have permission to view this page.',
                    'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for(f'{current_user.role.lower()}_dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(f'{current_user.role.lower()}_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        user = db_session.query(User).filter_by(username=username,
                                                role=role).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for(f'{role.lower()}_dashboard'))
        else:
            flash('Invalid username, password, or role combination.', 'danger')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for(f'{current_user.role.lower()}_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        contact = request.form.get('contact')
        role = request.form.get('role')
        location = request.form.get('location')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('signup'))

        if db_session.query(User).filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('signup'))

        if db_session.query(User).filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('signup'))

        new_user = User(username=username,
                        email=email,
                        contact=contact,
                        role=role,
                        location=location)
        new_user.set_password(password)

        db_session.add(new_user)
        db_session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/user/dashboard')
@login_required
@role_required('User')
def user_dashboard():
    return render_template('user/dashboard.html')


@app.route('/user/scan_bin', methods=['POST'])
@login_required
@role_required('User')
def scan_bin():
    bin_code = request.json.get('bin_code')
    bin_data = db_session.query(Bin).filter_by(bin_code=bin_code).first()

    if bin_data:
        return jsonify({
            'success': True,
            'bin': {
                'code':
                bin_data.bin_code,
                'location':
                bin_data.location,
                'recyclable_weight':
                bin_data.recyclable_weight,
                'non_recyclable_weight':
                bin_data.non_recyclable_weight,
                'fill_percentage':
                round(bin_data.get_fill_percentage(), 2),
                'last_cleaned':
                bin_data.last_cleaned.strftime('%Y-%m-%d')
                if bin_data.last_cleaned else 'Never',
                'status':
                bin_data.status
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Bin not found'})


@app.route('/user/complaint', methods=['GET', 'POST'])
@login_required
@role_required('User')
def user_complaint():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')

        complaint = Complaint(user_id=current_user.id,
                              title=title,
                              description=description,
                              location=location)

        db_session.add(complaint)
        db_session.commit()

        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('user_complaint'))

    return render_template('user/complaint.html')


@app.route('/user/sell', methods=['GET', 'POST'])
@login_required
@role_required('User')
def user_sell():
    if request.method == 'POST':
        waste_type = request.form.get('waste_type')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        price = request.form.get('price')

        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = filename

        waste_sale = WasteSale(seller_id=current_user.id,
                               waste_type=waste_type,
                               quantity=float(quantity),
                               description=description,
                               price=float(price) if price else None,
                               image_path=image_path,
                               location=current_user.location)

        db_session.add(waste_sale)
        db_session.commit()

        flash('Waste listed successfully!', 'success')
        return redirect(url_for('user_sell'))

    recyclers = db_session.query(User).filter_by(
        role='Recycler', location=current_user.location).all()
    return render_template('user/sell.html', recyclers=recyclers)


@app.route('/collector/dashboard')
@login_required
@role_required('Collector')
def collector_dashboard():
    bins = db_session.query(Bin).filter_by(
        location=current_user.location).all()
    return render_template('collector/dashboard.html', bins=bins)


@app.route('/collector/complaints')
@login_required
@role_required('Collector')
def collector_complaints():
    complaints = db_session.query(Complaint).filter_by(
        location=current_user.location).all()
    return render_template('collector/complaints.html', complaints=complaints)


@app.route('/collector/sell', methods=['GET', 'POST'])
@login_required
@role_required('Collector')
def collector_sell():
    if request.method == 'POST':
        waste_type = request.form.get('waste_type')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        price = request.form.get('price')

        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = filename

        waste_sale = WasteSale(seller_id=current_user.id,
                               waste_type=waste_type,
                               quantity=float(quantity),
                               description=description,
                               price=float(price) if price else None,
                               image_path=image_path,
                               location=current_user.location)

        db_session.add(waste_sale)
        db_session.commit()

        flash('Waste listed successfully!', 'success')
        return redirect(url_for('collector_sell'))

    return render_template('collector/sell.html')


@app.route('/collector/analytics')
@login_required
@role_required('Collector')
def collector_analytics():
    return render_template('collector/analytics.html')


@app.route('/recycler/dashboard')
@login_required
@role_required('Recycler')
def recycler_dashboard():
    return redirect(url_for('recycler_buy'))


@app.route('/recycler/buy')
@login_required
@role_required('Recycler')
def recycler_buy():
    waste_listings = db_session.query(WasteSale).filter_by(
        location=current_user.location, status='Available').all()
    return render_template('recycler/buy.html', waste_listings=waste_listings)


@app.route('/recycler/complaint', methods=['GET', 'POST'])
@login_required
@role_required('Recycler')
def recycler_complaint():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')

        complaint = Complaint(user_id=current_user.id,
                              title=title,
                              description=description,
                              location=location)

        db_session.add(complaint)
        db_session.commit()

        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('recycler_complaint'))

    my_complaints = db_session.query(Complaint).filter_by(
        user_id=current_user.id).all()
    return render_template('recycler/complaint.html', complaints=my_complaints)


@app.route('/recycler/sell', methods=['GET', 'POST'])
@login_required
@role_required('Recycler')
def recycler_sell():
    if request.method == 'POST':
        waste_type = request.form.get('waste_type')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        price = request.form.get('price')

        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = filename

        waste_sale = WasteSale(seller_id=current_user.id,
                               waste_type=waste_type,
                               quantity=float(quantity),
                               description=description,
                               price=float(price) if price else None,
                               image_path=image_path,
                               location=current_user.location)

        db_session.add(waste_sale)
        db_session.commit()

        flash('Waste listed successfully!', 'success')
        return redirect(url_for('recycler_sell'))

    return render_template('recycler/sell.html')


@app.route('/government/dashboard')
@login_required
@role_required('Government')
def government_dashboard():
    bins = db_session.query(Bin).filter_by(
        location=current_user.location).all()
    return render_template('government/dashboard.html', bins=bins)


@app.route('/government/complaints')
@login_required
@role_required('Government')
def government_complaints():
    complaints = db_session.query(Complaint).filter_by(
        location=current_user.location).all()
    return render_template('government/complaints.html', complaints=complaints)


@app.route('/government/transactions')
@login_required
@role_required('Government')
def government_transactions():
    transactions = db_session.query(WasteSale).filter_by(
        location=current_user.location).all()
    return render_template('government/transactions.html',
                           transactions=transactions)


@app.route('/government/analytics')
@login_required
@role_required('Government')
def government_analytics():
    return render_template('government/analytics.html')

@app.route('/api/bin-stats')
def bin_stats():
    urgent = Bin.query.filter_by(status="Urgent").count()
    medium = Bin.query.filter_by(status="Medium").count()
    good = Bin.query.filter_by(status="Enough Space").count()

    return jsonify({
        "urgent": urgent,
        "medium": medium,
        "good": good
    })
    
@app.route('/update_weight', methods=['POST'])
def update_weight():
    data = request.get_json()

    bin_code = data.get('bin_code')
    recyclable_weight = data.get('recyclable_weight')

    if not bin_code or recyclable_weight is None:
        return jsonify({"success": False, "message": "Invalid data"}), 400

    # Find the bin
    bin_obj = db_session.query(Bin).filter_by(bin_code=bin_code).first()

    if not bin_obj:
        return jsonify({"success": False, "message": "Bin not found"}), 404

    # Update weight into database
    bin_obj.recyclable_weight = float(recyclable_weight)

    # Auto-update status
    bin_obj.update_status()

    db_session.commit()

    return jsonify({"success": True, "message": "Weight updated!", 
                    "recyclable_weight": bin_obj.recyclable_weight,
                    "status": bin_obj.status})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
