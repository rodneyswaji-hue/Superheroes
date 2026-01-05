from flask import Flask, jsonify, request
from config import Config, db, migrate
from models import Hero, Power, HeroPower

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)


@app.get("/heroes")
def get_heroes():
    return jsonify([h.to_dict() for h in Hero.query.all()]), 200


@app.get("/heroes/<int:id>")
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    return jsonify({
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": [
            {
                "id": hp.id,
                "hero_id": hp.hero_id,
                "power_id": hp.power_id,
                "strength": hp.strength,
                "power": hp.power.to_dict()
            } for hp in hero.hero_powers
        ]
    }), 200


@app.get("/powers")
def get_powers():
    return jsonify([p.to_dict() for p in Power.query.all()]), 200


@app.get("/powers/<int:id>")
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict()), 200


@app.patch("/powers/<int:id>")
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    try:
        power.description = request.json["description"]
        db.session.commit()
        return jsonify(power.to_dict()), 200
    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 422


@app.post("/hero_powers")
def create_hero_power():
    try:
        hp = HeroPower(
            strength=request.json["strength"],
            hero_id=request.json["hero_id"],
            power_id=request.json["power_id"]
        )
        db.session.add(hp)
        db.session.commit()

        return jsonify({
            "id": hp.id,
            "hero_id": hp.hero_id,
            "power_id": hp.power_id,
            "strength": hp.strength,
            "hero": hp.hero.to_dict(),
            "power": hp.power.to_dict()
        }), 201

    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 422


if __name__ == "__main__":
    app.run(debug=True)
