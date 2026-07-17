from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Association table for the many-to-many relationship between players and games
player_games = db.Table('player_games',
    db.Column('player_id', db.Integer, db.ForeignKey('players.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True)
)

# Models go here!

class Player(db.Model, SerializerMixin):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    position = db.Column(db.String)
    
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    games = db.relationship('Game', secondary=player_games, back_populates='players')

    def __repr__(self):
        return f'<Player {self.id} {self.name}>'

class Team(db.Model, SerializerMixin):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    players = db.relationship('Player', backref='team', lazy=True)
    # Add relationships for home and away games
    home_games = db.relationship('Game', foreign_keys='Game.home_team_id', back_populates='home_team')
    away_games = db.relationship('Game', foreign_keys='Game.away_team_id', back_populates='away_team')

    def __repr__(self):
        return f'<Team {self.id} {self.name}>'

class Game(db.Model, SerializerMixin):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    home_team = db.relationship('Team', foreign_keys=[home_team_id], back_populates='home_games')
    away_team = db.relationship('Team', foreign_keys=[away_team_id], back_populates='away_games')
    players = db.relationship('Player', secondary=player_games, back_populates='games')

    def __repr__(self):
        return f'<Game {self.id}>'
