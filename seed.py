from config import create_app, db
from models import Hero, Power

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    heroes = [
        Hero(name="Kamala Khan", super_name="Ms. Marvel"),
        Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
    ]

    powers = [
        Power(name="super strength", description="gives the wielder super-human strengths"),
        Power(name="flight", description="gives the wielder the ability to fly at supersonic speed"),
    ]

    db.session.add_all(heroes + powers)
    db.session.commit()
