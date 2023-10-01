from website.models import Settings, db
from website import app

with app.app_context():
    print("Created admin account")
    #db.create_all()
    default_settings = Settings(dockhands=1, truckdrivers=1, supervisors=1)

    db.session.add(default_settings)
    db.session.commit()