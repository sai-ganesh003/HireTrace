from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from models.user import User
from app import get_db

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

# ── Register ───────────────────────────────────────────────
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Hash the password
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_pw)
            )
            conn.commit()
            flash("Account created! Please log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash("Username or email already exists.", "danger")
        finally:
            conn.close()

    return render_template("register.html")

# ── Login ──────────────────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user["password"], password):
            user_obj = User(user["id"], user["username"], user["email"], user["password"])
            login_user(user_obj)
            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html")

# ── Logout ─────────────────────────────────────────────────
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))