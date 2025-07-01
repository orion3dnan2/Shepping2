from werkzeug.security import generate_password_hash
from models import db, User  # إذا كان اسم الكلاس "User"
from admin import Admin      # إذا كان اسم الكلاس "Admin"
from app import app

with app.app_context():
    # جرب Admin أو User حسب اسم الكلاس عندك
    admin = Admin.query.filter_by(username='admin').first()
    if admin:
        new_password = '123456'
        admin.password_hash = generate_password_hash(new_password)
        db.session.commit()
        print(f"✅ Password updated to: {new_password}")
    else:
        print("❌ Admin user not found.")
