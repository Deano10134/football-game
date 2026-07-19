from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

from config import db

# Association table for the many-to-many relationship between players and games
player_games = db.Table('player_games',
    db.Column('player_id', db.Integer, db.ForeignKey('players.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True)
)

# Models go here!

class Player(db.Model, SerializerMixin):
    __tablename__ = 'players'

    serialize_rules = ('-team.players', '-games.players', '-games.home_team', '-games.away_team')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    games = db.relationship('Game', secondary=player_games, back_populates='players')

    @validates('name')
    def validate_name(self, key, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError('Player name must be a non-empty string.')
        return name

    @validates('position')
    def validate_position(self, key, position):
        valid_positions = ['GK', 'CB', 'LB', 'RB', 'CDM', 'CM', 'CAM', 'LM', 'RM', 'LW', 'RW', 'ST']
        if position not in valid_positions:
            raise ValueError(f'Position must be one of {valid_positions}.')
        return position

    def __repr__(self):
        return f'<Player {self.id} {self.name}>'

class Team(db.Model, SerializerMixin):
    __tablename__ = 'teams'

    serialize_rules = ('-players.team', '-players.games', '-home_games.home_team', '-away_games.away_team')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    players = db.relationship('Player', backref='team', lazy=True)
    # Add relationships for home and away games
    home_games = db.relationship('Game', foreign_keys='Game.home_team_id', back_populates='home_team')
    away_games = db.relationship('Game', foreign_keys='Game.away_team_id', back_populates='away_team')

    @validates('name')
    def validate_name(self, key, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError('Team name must be a non-empty string.')
        return name

    def __repr__(self):
        return f'<Team {self.id} {self.name}>'

class Game(db.Model, SerializerMixin):
    __tablename__ = 'games'

    serialize_rules = ('-home_team.home_games', '-home_team.players', '-away_team.away_games', '-away_team.players', '-players.games', '-players.team')

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    home_team = db.relationship('Team', foreign_keys=[home_team_id], back_populates='home_games')
    away_team = db.relationship('Team', foreign_keys=[away_team_id], back_populates='away_games')
    players = db.relationship('Player', secondary=player_games, back_populates='games')

    @validates('home_team_id', 'away_team_id')
    def validate_teams(self, key, value):
        if not isinstance(value, int):
            raise ValueError('Team id must be an integer.')
        return value

    def __repr__(self):
        return f'<Game {self.id}>'
