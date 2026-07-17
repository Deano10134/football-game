from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!

class Player(db.Model, SerializerMixin):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    position = db.Column(db.String)
    
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    def __repr__(self):
        return f'<Player {self.id} {self.name}>'

class Team(db.Model, SerializerMixin):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    players = db.relationship('Player', backref='team')

    def __repr__(self):
        return f'<Team {self.id} {self.name}>'

class Game(db.Model, SerializerMixin):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    home_team_score = db.Column(db.Integer)
    away_team_score = db.Column(db.Integer)

    home_team = db.relationship('Team', foreign_keys=[home_team_id], backref='home_games')
    away_team = db.relationship('Team', foreign_keys=[away_team_id], backref='away_games')

    def __repr__(self):
        return f'<Game {self.id}>'
