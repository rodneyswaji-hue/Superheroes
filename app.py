from flask import request, jsonify
from config import create_app, db
from models import Hero, Power, HeroPower
from flask_mail import Message, Mail

app = create_app()
mail = Mail(app)

# ---------------- GET HEROES ----------------
@app.route("/heroes")
def heroes():
    return jsonify([hero.to_dict() for hero in Hero.query.all()]), 200

# ---------------- GET HERO BY ID ----------------
@app.route("/heroes/<int:id>")
def hero_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return {"error": "Hero not found"}, 404

    return {
        **hero.to_dict(),
        "hero_powers": [
            {
                "id": hp.id,
                "hero_id": hp.hero_id,
                "power_id": hp.power_id,
                "strength": hp.strength,
                "power": hp.power.to_dict()
            } for hp in hero.hero_powers
        ]
    }, 200

# ---------------- GET POWERS ----------------
@app.route("/powers")
def powers():
    return jsonify([p.to_dict() for p in Power.query.all()]), 200

# ---------------- GET POWER BY ID ----------------
@app.route("/powers/<int:id>")
def power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return {"error": "Power not found"}, 404
    return power.to_dict(), 200

# ---------------- PATCH POWER ----------------
@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return {"error": "Power not found"}, 404

    try:
        power.description = request.json.get("description")
        db.session.commit()
        return power.to_dict(), 200
    except Exception as e:
        return {"errors": [str(e)]}, 422

# ---------------- POST HERO POWER ----------------
@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    try:
        hp = HeroPower(
            strength=request.json["strength"],
            hero_id=request.json["hero_id"],
            power_id=request.json["power_id"]
        )
        db.session.add(hp)
        db.session.commit()

        return {
            "id": hp.id,
            "hero_id": hp.hero_id,
            "power_id": hp.power_id,
            "strength": hp.strength,
            "hero": hp.hero.to_dict(),
            "power": hp.power.to_dict()
        }, 201

    except Exception as e:
        return {"errors": [str(e)]}, 422

@app.route("/send-email")
def send_email():
    msg = Message(
        subject="Superheroes API",
        sender="rodneyswaji@gmail.com",
        recipients=["recipient@email.com"],
        body="Your Flask API is working!"
    )
    mail.send(msg)
    return {"message": "Email sent successfully"}, 200
