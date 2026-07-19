# Football League app ⚽

A full-stack application for managing a football league — Teams, Players, and
Games — built with a Flask/SQLAlchemy REST API backend and a React frontend.

This web app was build for the Phase 4 project that I completed as part of my Software Engineering Transform course at Academy Xi in Australia. It showcases all skills that I learnt in Full stack development as part of the course.

## Overview

This app lets you:

- View, create, update, and delete **Players**.
- View and create/update/delete **Teams**.
- View and create/update/delete **Games** (matchups between a home team and
  an away team).
- Navigate between pages using a React Router-powered nav bar.
- Fill out forms built with Formik and validated with Yup, both client-side
  (immediate feedback) and server-side (data integrity).

## Tech Stack

**Backend:** Flask, Flask-RESTful, Flask-SQLAlchemy, Flask-Migrate,
SQLAlchemy-Serializer, Flask-CORS

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
            ├── TeamsPage.js
            ├── PlayersPage.js
            └── GamesPage.js
```

---

## Data Models

All models live in `server/models.py` and use `SerializerMixin` to serialize
to JSON.

### `Team`

| Column | Type    | Notes            |
| ------ | ------- | ---------------- |
| id     | Integer | Primary key      |
| name   | String  | Required, unique |

A team has many `players` (one-to-many), and can appear as either the
`home_team` or `away_team` in many `games` (two one-to-many relationships).

### `Player`

| Column   | Type    | Notes                                           |
| -------- | ------- | ------------------------------------------------ |
| id       | Integer | Primary key                                      |
| name     | String  | Required, non-empty                              |
| position | String  | Required; must be a valid soccer position code   |
| team_id  | Integer | Foreign key → `teams.id`                         |

Valid `position` values: `GK, CB, LB, RB, CDM, CM, CAM, LM, RM, LW, RW, ST`.

A player belongs to one `team`, and can participate in many `games` through
the `player_games` join table (reciprocal many-to-many).

### `Game`

| Column       | Type     | Notes                    |
| ------------ | -------- | ------------------------- |
| id           | Integer  | Primary key                |
| date         | DateTime | Required                   |
| home_team_id | Integer  | Foreign key → `teams.id`   |
| away_team_id | Integer  | Foreign key → `teams.id`   |

A game belongs to a `home_team` and an `away_team`, and has many `players`
through the reciprocal many-to-many relationship with `Player`.

### `player_games` (association table)

Join table implementing the many-to-many relationship between `Player` and
`Game`, with `player_id` and `game_id` as a composite primary key.

---

## API Routes

All routes are implemented with Flask-RESTful `Resource` classes in
`server/app.py`, use `db.session` to create/read/update/delete records, and
return appropriate HTTP status codes (`200`, `201`, `204`, `400`, `404`).

| Resource | Route               | Methods                  |
| -------- | -------------------- | ------------------------- |
| Player   | `/players`           | `GET`, `POST`              |
| Player   | `/players/<int:id>`  | `GET`, `PATCH`, `DELETE`   |
| Team     | `/teams`             | `GET`, `POST`              |
| Team     | `/teams/<int:id>`    | `GET`, `PATCH`, `DELETE`   |
| Game     | `/games`             | `GET`, `POST`              |
| Game     | `/games/<int:id>`    | `GET`, `PATCH`, `DELETE`   |

Server-side validation (via SQLAlchemy `@validates`) enforces:

- `Player.name` / `Team.name` — must be non-empty strings.
- `Player.position` — must be one of the valid football position codes.
- `Game.home_team_id` / `away_team_id` — must be integers.

Invalid requests return a `400` with a JSON body like
`{"errors": ["..."]}`. Requests for missing records return a `404` with
`{"error": "..."}`.

---

## Frontend

The React app (in `client/src`) uses `react-router-dom` for client-side
routing and `fetch()` (proxied to the Flask API) for all data operations.

| Route      | Component        | Description                              |
| ---------- | ----------------- | ------------------------------------------ |
| `/`        | `Home.js`         | Landing page                                |
| `/teams`   | `TeamsPage.js`    | List teams, create a new team                |
| `/players` | `PlayersPage.js`  | List players, create/edit/delete a player    |
| `/games`   | `GamesPage.js`    | List games, schedule a new game              |

`NavBar.js` renders on every page and provides `NavLink`s to each route.

Each page uses a `Formik` form with a `Yup` `validationSchema` to validate
input before submitting:

- **Type validation:** `Yup.number()` (team IDs), `Yup.date()` (game date).
- **Format validation:** `Yup.string().min()/.max()` (names),
  `Yup.string().oneOf()` (player position, restricted to valid codes).

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

`config.py` calls `CORS(app)`, enabling Cross-Origin Resource Sharing on all
routes so the React dev server (running on a different port) can
successfully call the Flask API via `fetch()`.
