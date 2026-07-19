# Football  League — Client

This is the React frontend for the Football League app, bootstrapped with
[Create React App](https://github.com/facebook/create-react-app).

It communicates with the Flask API in `../server` via `fetch()` (requests
are proxied to `http://localhost:5555`, configured in `package.json`).

This web app was build for the Phase 4 project that I completed as part of my Software Engineering Transform course at Academy Xi in Australia. It showcases all skills that I learnt in Full stack development as apart of the course.

This the Frontend part of the application.
## Structure

```console
src/
└── components/
    ├── App.js         # Sets up React Router routes
    ├── NavBar.js       # Navigation bar linking to all routes
    ├── Home.js         # Landing page ("/")
    ├── TeamsPage.js    # List + create teams ("/teams")
    ├── PlayersPage.js  # List + create/edit/delete players ("/players")
    └── GamesPage.js    # List + create games ("/games")
```

Each page component fetches its data on mount with `useEffect`, and uses a
`Formik` form (validated with `Yup`) to submit new or updated records to the
API.

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser
(use `PORT=3001 npm start` if port 3000 is already taken).

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in interactive watch mode.

### `npm run build`

Builds the app for production to the `build` folder, minified and optimized
for the best performance.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

This copies all configuration files (webpack, Babel, ESLint, etc.) directly
into the project for full control.

## Learn More

- [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started)
- [React documentation](https://reactjs.org/)
- [React Router documentation](https://v5.reactrouter.com/)
- [Formik documentation](https://formik.org/docs/overview)
- [Yup documentation](https://github.com/jquense/yup)

