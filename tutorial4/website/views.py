from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask import Flask  # Import Flask module

from .models import User, WasteCollection
from .form import ScheduleCollectionForm, TrackRecyclingForm

views = Blueprint("views", __name__)

@views.route('/check-data')
def check_data():
    users = User.query.all()
    collections = WasteCollection.query.all()
    return jsonify({
        'users': [{'username': user.username, 'email': user.email, 'role': user.role} for user in users],
        'collections': [{'address': c.address, 'date': c.collection_date, 'time': c.collection_time, 'status': c.status} for c in collections]
    })



@views.route("/")
@views.route("/home")
@login_required
def home():
    schedule = ScheduleCollectionForm()
    track = TrackRecyclingForm()
    return render_template("home.html", user=current_user, schedule=schedule, track=track)

@views.route("/")
@views.route("/schedule")
@login_required
def schedule():
    return render_template("schedule.html", user=current_user, form=ScheduleCollectionForm())

@views.route("/")
@views.route("/recycle")
@login_required
def recycle():
    return render_template("track.html", user=current_user, form=TrackRecyclingForm())

@views.route("/")
@views.route("/admin")
@login_required
def admin():
    return render_template("admin.html", user=current_user)

# Helper function to check if the current user is an admin
def admin_required(func):
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Access denied. Admins only.')
            return redirect(url_for('views.index'))  # or appropriate route
        return func(*args, **kwargs)
    return wrapper

@views.route('/admin', methods=['GET'])
@admin_required
def admin_dashboard():
    users = User.query.all()
    collections = WasteCollection.query.all()

    # Debugging statements
    print("Users:", users)
    print("Collections:", collections)

    return render_template('admin.html', users=users, collections=collections)

# Register the blueprint in your app factory
def create_app():
    app = Flask(__name__)
    # other setup code...
    app.register_blueprint(views)
    return app
