from website.models import User, db
from website import app

with app.app_context():
    print("Created admin account")
    #db.create_all()
    admin = User(admin=1, username='admin', password='admin123')

    db.session.add(admin)
    db.session.commit()