from flask import Blueprint, request, jsonify
from marvel.modules.characters import Characters
from werkzeug.wrappers import response
from marvel_super_heroes.helpers import token_required
from marvel_super_heroes.models import db, User, Hero, hero_schema, heroes_schema
from marvel import Marvel



#m=Marvel("","")
m = Marvel("93f46f1ff08973d70263cb4b0756acb0","08396b0cb4c569191987b2b16565f64704252596")
characters = m.characters

#characters = m.characters
all_characters = characters.all()
x = 1011334
for n in range(0,6):
    all_characters = characters.comics(x)
    x=x+1
    for i in range(1,12):
        print(all_characters['data']['results'][int(i)]['title'])




api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
@token_required
def get_data(current_user_token):
    return {'some': 'value'}


@api.route('/heroes', methods=['POST'])
@token_required
def create_hero(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comic_appeared_in = request.json['comic_appeared_in']
    super_power = request.json['super_power']
    user_token = current_user_token.token

    hero = Hero(name, description, comic_appeared_in, super_power, user_token)
    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)


@api.route('/heroes', methods=['GET'])
@token_required
def get_heroes(current_user_token):
    owner = current_user_token.token
    heroes = Hero.query.filter_by(user_token=owner).all()
    response = hero_schema.dump(Hero)
    return jsonify(response)


@api.route('/heroes/<id>', methods=['GET'])
@token_required
def get_hero(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        hero = Hero.query.get(id)
        response = hero_schema.dump(Hero)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


@api.route('/heroes/<id>', methods=['POST', 'PUT'])
@token_required
def update_drone(current_user_token, id):
    hero = Hero.query.get(id)  # Get Hero Instance

    hero.name = request.json['name']
    hero.description = request.json['description']
    hero.comic_appeared_in = request.json['comic_appeared_in']
    hero.super_power = request.json['super_power']
    hero.user_token = current_user_token.token

    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)

@api.route('/heroes/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Hero.query.get(id)
    db.session.delete(hero)
    db.session.commit()   

    response = hero_schema.dump(hero)
    return jsonify(response)

