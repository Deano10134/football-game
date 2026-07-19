#!/usr/bin/env python3

# Standard library imports
from datetime import datetime

# Remote library imports
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, db, api
from server.models import Player, Team, Game

class Players(Resource):
    def get(self):
        players = [player.to_dict() for player in Player.query.all()]
        return players, 200

    def post(self):
        data = request.get_json()
        try:
            player = Player(
                name=data.get('name'),
                position=data.get('position'),
                team_id=data.get('team_id'),
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


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)
