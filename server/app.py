#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
from models import Player, Team, Game

class Players(Resource):
    def get(self):
        players = [player.to_dict() for player in Player.query.all()]
        return players, 200
    
api.add_resource(Players, '/players')

class PlayerByID(Resource):
    def get(self, id):
        player = Player.query.filter_by(id=id).first().to_dict()
        return player, 200

api.add_resource(PlayerByID, '/players/<int:id>')

class Teams(Resource):
    def get(self):
        teams = [team.to_dict() for team in Team.query.all()]
        return teams, 200

api.add_resource(Teams, '/teams')

class TeamByID(Resource):
    def get(self, id):
        team = Team.query.filter_by(id=id).first().to_dict()
        return team, 200

api.add_resource(TeamByID, '/teams/<int:id>')

class Games(Resource):
    def get(self):
        games = [game.to_dict() for game in Game.query.all()]
        return games, 200

api.add_resource(Games, '/games')

class GameByID(Resource):
    def get(self, id):
        game = Game.query.filter_by(id=id).first().to_dict()
        return game, 200

api.add_resource(GameByID, '/games/<int:id>')


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

