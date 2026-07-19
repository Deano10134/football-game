#!/usr/bin/env python3

# Standard library imports
from datetime import datetime

# Remote library imports
from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, db, api
from server.models import Player, Team, Game, User, Review


class Signup(Resource):
    def post(self):
        data = request.get_json()
        try:
            user = User(username=data.get('username'))
            user.password_hash = data.get('password')
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return user.to_dict(), 201
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 400

api.add_resource(Signup, '/signup')


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {'error': 'Invalid username or password'}, 401

api.add_resource(Login, '/login')


class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204

api.add_resource(Logout, '/logout')


class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return user.to_dict(), 200
        return {'error': 'Not logged in'}, 401

api.add_resource(CheckSession, '/check_session')


class Players(Resource):
    def get(self):
        players = [player.to_dict() for player in Player.query.all()]
        return players, 200

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Must be logged in to create a player'}, 401

        data = request.get_json()
        try:
            player = Player(
                name=data.get('name'),
                position=data.get('position'),
                team_id=data.get('team_id'),
                user_id=user_id,
            )
            db.session.add(player)
            db.session.commit()
            return player.to_dict(), 201
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 400

api.add_resource(Players, '/players')

class PlayerByID(Resource):
    def get(self, id):
        player = Player.query.filter_by(id=id).first()
        if not player:
            return {'error': 'Player not found'}, 404
        return player.to_dict(), 200

    def patch(self, id):
        player = Player.query.filter_by(id=id).first()
        if not player:
            return {'error': 'Player not found'}, 404

        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Must be logged in to edit a player'}, 401
        if player.user_id != user_id:
            return {'error': 'You may only edit players you created'}, 403

        data = request.get_json()
        try:
            for attr in data:
                setattr(player, attr, data[attr])
            db.session.commit()
            return player.to_dict(), 200
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 400

    def delete(self, id):
        player = Player.query.filter_by(id=id).first()
        if not player:
            return {'error': 'Player not found'}, 404

        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Must be logged in to delete a player'}, 401
        if player.user_id != user_id:
            return {'error': 'You may only delete players you created'}, 403

        db.session.delete(player)
        db.session.commit()
        return {}, 204

api.add_resource(PlayerByID, '/players/<int:id>')

class Teams(Resource):
    def get(self):
        teams = [team.to_dict() for team in Team.query.all()]
        return teams, 200

    def post(self):
        data = request.get_json()
        try:
            team = Team(name=data.get('name'))
            db.session.add(team)
            db.session.commit()
            return team.to_dict(), 201
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 400

api.add_resource(Teams, '/teams')

class TeamByID(Resource):
    def get(self, id):
        team = Team.query.filter_by(id=id).first()
        if not team:
            return {'error': 'Team not found'}, 404
        return team.to_dict(), 200

    def patch(self, id):
        team = Team.query.filter_by(id=id).first()
        if not team:
            return {'error': 'Team not found'}, 404

        data = request.get_json()
        try:
            for attr in data:
                setattr(team, attr, data[attr])
            db.session.commit()
            return team.to_dict(), 200
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 400

    def delete(self, id):
        team = Team.query.filter_by(id=id).first()
        if not team:
            return {'error': 'Team not found'}, 404

        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Must be logged in to delete a team'}, 401

        db.session.delete(team)
        db.session.commit()
        return {}, 204

api.add_resource(TeamByID, '/teams/<int:id>')

class Games(Resource):
    def get(self):
        games = [game.to_dict() for game in Game.query.all()]
        return games, 200

    def post(self):
        data = request.get_json()
        try:
            date_str = data.get('date')
            game = Game(
                date=datetime.fromisoformat(date_str) if date_str else None,
                home_team_id=data.get('home_team_id'),
                away_team_id=data.get('away_team_id'),
            )
            db.session.add(game)
            db.session.commit()
            return game.to_dict(), 201
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 400

api.add_resource(Games, '/games')

class GameByID(Resource):
    def get(self, id):
        game = Game.query.filter_by(id=id).first()
        if not game:
            return {'error': 'Game not found'}, 404
        return game.to_dict(), 200

    def patch(self, id):
        game = Game.query.filter_by(id=id).first()
        if not game:
            return {'error': 'Game not found'}, 404

        data = request.get_json()
        try:
            for attr in data:
                if attr == 'date' and data[attr]:
                    setattr(game, attr, datetime.fromisoformat(data[attr]))
                else:
                    setattr(game, attr, data[attr])
            db.session.commit()
            return game.to_dict(), 200
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 400

    def delete(self, id):
        game = Game.query.filter_by(id=id).first()
        if not game:
            return {'error': 'Game not found'}, 404

        db.session.delete(game)
        db.session.commit()
        return {}, 204

api.add_resource(GameByID, '/games/<int:id>')


class Reviews(Resource):
    def get(self):
        reviews = [review.to_dict() for review in Review.query.all()]
        return reviews, 200

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Must be logged in to leave a review'}, 401

        data = request.get_json()
        team_id = data.get('team_id')
        player_id = data.get('player_id')

        if bool(team_id) == bool(player_id):
            return {'errors': ['A review must target exactly one of team_id or player_id.']}, 400

        try:
            review = Review(
                content=data.get('content'),
                rating=data.get('rating'),
                user_id=user_id,
                team_id=team_id,
                player_id=player_id,
            )
            db.session.add(review)
            db.session.commit()
            return review.to_dict(), 201
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 400

api.add_resource(Reviews, '/reviews')

class ReviewByID(Resource):
    def get(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    def patch(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            return {'error': 'Review not found'}, 404

        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Must be logged in to edit a review'}, 401
        if review.user_id != user_id:
            return {'error': 'You may only edit reviews you created'}, 403

        data = request.get_json()
        try:
            for attr in data:
                setattr(review, attr, data[attr])
            db.session.commit()
            return review.to_dict(), 200
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 400

    def delete(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            return {'error': 'Review not found'}, 404

        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Must be logged in to delete a review'}, 401
        if review.user_id != user_id:
            return {'error': 'You may only delete reviews you created'}, 403

        db.session.delete(review)
        db.session.commit()
        return {}, 204

api.add_resource(ReviewByID, '/reviews/<int:id>')


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)
