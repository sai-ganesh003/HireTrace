from dotenv import load_dotenv
load_dotenv()  # Must be first before anything else!

from flask import Flask
from config import Config
import pymysql
from flask_login import LoginManager

# ── DB helper ──────────────────────────────────────────────
def get_db():
    """Call this anywhere you need a fresh DB connection."""
    conn = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        port=Config.MYSQL_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

# ── App factory ─────────────────────────────────────────────
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return User(user["id"], user["username"], user["email"], user["password"])
        return None

    # Register blueprints
    from routes.auth import auth_bp
    from routes.jobs import jobs_bp
    from routes.dashboard import dashboard_bp
    from routes.interviews import interviews_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(interviews_bp)

    return app

# ── Run ─────────────────────────────────────────────────────
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)