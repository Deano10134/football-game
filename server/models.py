from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from config import db, bcrypt

# Association table for the many-to-many relationship between players and games
player_games = db.Table('player_games',
    db.Column('player_id', db.Integer, db.ForeignKey('players.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True)
)

# Models go here!

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-players.user', '-_password_hash', '-reviews.user')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    players = db.relationship('Player', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    @validates('username')
    def validate_username(self, key, username):
        if not isinstance(username, str) or len(username.strip()) == 0:
            raise ValueError('Username must be a non-empty string.')
        return username

    def __repr__(self):
        return f'<User {self.id} {self.username}>'

class Player(db.Model, SerializerMixin):
    __tablename__ = 'players'

    serialize_rules = ('-team.players', '-games.players', '-games.home_team', '-games.away_team', '-user.players', '-reviews.player')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    games = db.relationship('Game', secondary=player_games, back_populates='players')
    reviews = db.relationship('Review', backref='player', lazy=True, cascade='all, delete-orphan')

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

    serialize_rules = ('-players.team', '-players.games', '-home_games.home_team', '-away_games.away_team', '-reviews.team')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    players = db.relationship('Player', backref='team', lazy=True)
    # Add relationships for home and away games
    home_games = db.relationship('Game', foreign_keys='Game.home_team_id', back_populates='home_team')
    away_games = db.relationship('Game', foreign_keys='Game.away_team_id', back_populates='away_team')
    reviews = db.relationship('Review', backref='team', lazy=True, cascade='all, delete-orphan')

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

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    serialize_rules = ('-user.reviews', '-team.reviews', '-player.reviews')

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)

    @validates('content')
    def validate_content(self, key, content):
        if not isinstance(content, str) or len(content.strip()) == 0:
            raise ValueError('Review content must be a non-empty string.')
        return content

    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError('Rating must be an integer between 1 and 5.')
        return rating

    @validates('team_id', 'player_id')
    def validate_target(self, key, value):
        other_key = 'player_id' if key == 'team_id' else 'team_id'
        other_value = getattr(self, other_key, None)
        if value is not None and other_value is not None:
            raise ValueError('A review may only target a team or a player, not both.')
        return value

    def __repr__(self):
        return f'<Review {self.id}>'
