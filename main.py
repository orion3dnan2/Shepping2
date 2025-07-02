from app import app, db
import os

if __name__ == "__main__":
    # إنشاء الجداول إذا لم تكن موجودة
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)