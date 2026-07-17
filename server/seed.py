#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

from app import app
from models import db, Player, Team, Game

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")
        
        Player.query.delete()
        Team.query.delete()
        Game.query.delete()

        t1 = Team(name='New York Giants')
        t2 = Team(name='New England Patriots')
        t3 = Team(name='Dallas Cowboys')
        t4 = Team(name='Philadelphia Eagles')

        p1 = Player(name='Eli Manning', position='Quarterback', team=t1)
        p2 = Player(name='Tom Brady', position='Quarterback', team=t2)
        p3 = Player(name='Dak Prescott', position='Quarterback', team=t3)
        p4 = Player(name='Jalen Hurts', position='Quarterback', team=t4)

        g1 = Game(home_team=t1, away_team=t2, home_team_score=21, away_team_score=17)
        g2 = Game(home_team=t3, away_team=t4, home_team_score=24, away_team_score=20)

        db.session.add_all([t1, t2, t3, t4, p1, p2, p3, p4, g1, g2])
        db.session.commit()
        
        print("Seed complete!")
