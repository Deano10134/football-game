# Football League app ⚽

A full-stack application for managing a football league — Users, Teams,
Players, Games, and Reviews — built with a Flask/SQLAlchemy REST API backend
and a React frontend.

This web app was build for the Phase 4 project that I completed as part of my Software Engineering Transform course at Academy Xi in Australia. It showcases all skills that I learnt in Full stack development as part of the course.

## Overview

This app lets you:

- Sign up, log in, and log out with session-based authentication.
- View, create, update, and delete **Players** (only the player's creator
  may edit/delete them; must be logged in to create one).
- View and create **Teams**, and delete a team if logged in.
- View and create/update/delete **Games** (matchups between a home team and
  an away team).
- Leave a star **Review** on a Team or a Player if logged in, and delete
  your own reviews.
- Navigate between pages using a React Router-powered nav bar that adapts
  to whether a user is logged in.
- Fill out forms built with Formik and validated with Yup, both client-side
  (immediate feedback) and server-side (data integrity).

## Tech Stack

**Backend:** Flask, Flask-RESTful, Flask-SQLAlchemy, Flask-Migrate,
Flask-Bcrypt, SQLAlchemy-Serializer, Flask-CORS

**Frontend:** React, React Router (v5), Formik, Yup

---

## Project Structure

```console
.
├── Pipfile
├── config.py
├── instance/
│   └── app.db
├── migrations/
├── server/
│   ├── app.py
│   └── models.py
└── client/
    ├── package.json
    ├── public/
    └── src/
        └── components/
            ├── App.js
            ├── NavBar.js
            ├── Home.js
            ├── Signup.js
            ├── Login.js
            ├── TeamsPage.js
            ├── PlayersPage.js
            ├── GamesPage.js
            └── ReviewsPage.js
```

---

## Data Models

All models live in `server/models.py` and use `SerializerMixin` to serialize
to JSON.

### `User`

| Column         | Type    | Notes                          |
| -------------- | ------- | ------------------------------- |
| id             | Integer | Primary key                     |
| username       | String  | Required, unique                |
| _password_hash | String  | Required; hashed with Bcrypt    |

A user has many `players` (the players they created) and many `reviews`
(the reviews they left). Passwords are never stored or exposed in plain
text — the `password_hash` property raises on read and hashes on write via
`Flask-Bcrypt`.

### `Team`

| Column | Type    | Notes            |
| ------ | ------- | ---------------- |
| id     | Integer | Primary key      |
| name   | String  | Required, unique |

A team has many `players` (one-to-many), can appear as either the
`home_team` or `away_team` in many `games` (two one-to-many relationships),
and has many `reviews`.

### `Player`

| Column   | Type    | Notes                                           |
| -------- | ------- | ------------------------------------------------ |
| id       | Integer | Primary key                                      |
| name     | String  | Required, non-empty                              |
| position | String  | Required; must be a valid soccer position code   |
| team_id  | Integer | Foreign key → `teams.id`                         |
| user_id  | Integer | Foreign key → `users.id` (creator of the player)  |

Valid `position` values: `GK, CB, LB, RB, CDM, CM, CAM, LM, RM, LW, RW, ST`.

A player belongs to one `team`, one `user` (its creator), can participate in
many `games` through the `player_games` join table (reciprocal
many-to-many), and has many `reviews`.

### `Game`

| Column       | Type     | Notes                    |
| ------------ | -------- | ------------------------- |
| id           | Integer  | Primary key                |
| date         | DateTime | Required                   |
| home_team_id | Integer  | Foreign key → `teams.id`   |
| away_team_id | Integer  | Foreign key → `teams.id`   |

A game belongs to a `home_team` and an `away_team`, and has many `players`
through the reciprocal many-to-many relationship with `Player`.

### `Review`

| Column    | Type    | Notes                                                  |
| --------- | ------- | -------------------------------------------------------|
| id        | Integer | Primary key                                             |
| content   | String  | Required, non-empty                                     |
| rating    | Integer | Required; must be between 1 and 5                       |
| user_id   | Integer | Foreign key → `users.id` (author of the review)         |
| team_id   | Integer | Foreign key → `teams.id`, nullable                       |
| player_id | Integer | Foreign key → `players.id`, nullable                     |

A review must target exactly one of `team_id` or `player_id` (never both,
never neither); this is enforced by a SQLAlchemy `@validates` check. A
review belongs to the `user` who wrote it and, depending on its target, to
a `team` or a `player`.

### `player_games` (association table)

Join table implementing the many-to-many relationship between `Player` and
`Game`, with `player_id` and `game_id` as a composite primary key.

---

## API Routes

All routes are implemented with Flask-RESTful `Resource` classes in
`server/app.py`, use `db.session` to create/read/update/delete records, and
return appropriate HTTP status codes (`200`, `201`, `204`, `400`, `401`,
`403`, `404`).

| Resource      | Route                | Methods                  |
| ------------- | --------------------- | ------------------------- |
| Signup        | `/signup`             | `POST`                     |
| Login         | `/login`              | `POST`                     |
| Logout        | `/logout`             | `DELETE`                   |
| CheckSession  | `/check_session`      | `GET`                       |
| Player        | `/players`            | `GET`, `POST`               |
| Player        | `/players/<int:id>`   | `GET`, `PATCH`, `DELETE`    |
| Team          | `/teams`              | `GET`, `POST`               |
| Team          | `/teams/<int:id>`     | `GET`, `PATCH`, `DELETE`    |
| Game          | `/games`              | `GET`, `POST`               |
| Game          | `/games/<int:id>`     | `GET`, `PATCH`, `DELETE`    |
| Review        | `/reviews`            | `GET`, `POST`               |
| Review        | `/reviews/<int:id>`   | `GET`, `PATCH`, `DELETE`    |

### Authentication & Authorization

- `Signup` creates a `User` (hashing the password) and starts a session.
- `Login` verifies credentials and starts a session; `Logout` clears it.
- `CheckSession` returns the current user from the session, or `401` if
  no one is logged in.
- Creating a `Player` or a `Review` requires an active session (`401` if
  not logged in).
- Editing/deleting a `Player` or a `Review` requires the requester to be
  the original creator (`403` otherwise).
- Deleting a `Team` requires an active session (`401` if not logged in).

### Server-side validation

Server-side validation (via SQLAlchemy `@validates`) enforces:

- `Player.name` / `Team.name` — must be non-empty strings.
- `Player.position` — must be one of the valid football position codes.
- `Game.home_team_id` / `away_team_id` — must be integers.
- `User.username` — must be a non-empty string.
- `Review.content` — must be a non-empty string.
- `Review.rating` — must be an integer between 1 and 5.
- `Review.team_id` / `player_id` — a review may target a team or a player,
  but not both.

Invalid requests return a `400` with a JSON body like
`{"errors": ["..."]}`. Requests for missing records return a `404` with
`{"error": "..."}`. Unauthenticated/unauthorized requests return `401`/`403`
with `{"error": "..."}`.

---

## Frontend

The React app (in `client/src`) uses `react-router-dom` for client-side
routing and `fetch()` (proxied to the Flask API, with `credentials:
"include"` on requests that require a session) for all data operations.

| Route      | Component         | Description                                              |
| ---------- | ------------------ | ---------------------------------------------------------- |
| `/`        | `Home.js`          | Landing page                                                |
| `/teams`   | `TeamsPage.js`     | List teams, create a new team, delete a team if logged in    |
| `/players` | `PlayersPage.js`   | List players, create a player if logged in, edit/delete your own |
| `/games`   | `GamesPage.js`     | List games, schedule a new game                              |
| `/reviews` | `ReviewsPage.js`   | List reviews, leave a review on a team or player if logged in, delete your own |
| `/signup`  | `Signup.js`        | Create a new user account and log in                         |
| `/login`   | `Login.js`         | Log in to an existing account                                 |

`NavBar.js` renders on every page, provides `NavLink`s to each route, and
shows either "Log In"/"Sign Up" links or the current username with a
"Log Out" button, depending on session state.

`App.js` checks `/check_session` on load to restore an existing session and
passes the `currentUser` down to any page that needs to gate behaviour
behind authentication (creating/editing players, deleting teams, leaving
reviews).

Each page uses a `Formik` form with a `Yup` `validationSchema` to validate
input before submitting:

- **Type validation:** `Yup.number()` (team/player/rating IDs and values),
  `Yup.date()` (game date).
- **Format validation:** `Yup.string().min()/.max()` (names, review
  content), `Yup.string().oneOf()` (player position, restricted to valid
  codes).

---

## Getting Started

### Backend

```console
pipenv install
pipenv shell
export FLASK_APP=server.app
flask db upgrade
flask run -p 5555
```

The API will be available at [http://localhost:5555](http://localhost:5555).

### Frontend

```console
npm install --prefix client
npm start --prefix client
```

The React app runs on [http://localhost:3000](http://localhost:3000) by
default (the `proxy` field in `client/package.json` forwards API requests to
`http://localhost:5555`). If port 3000 is already in use, run
`PORT=3001 npm start --prefix client` instead.

---

## CORS

`config.py` calls `CORS(app, supports_credentials=True)`, enabling
Cross-Origin Resource Sharing (with cookies) on all routes so the React dev
server (running on a different port) can successfully call the Flask API
via `fetch()` and maintain a logged-in session.
