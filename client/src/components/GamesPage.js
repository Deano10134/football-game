import React, { useEffect, useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const GameSchema = Yup.object().shape({
  date: Yup.date().typeError("Date must be a valid date").required("Date is required"),
  home_team_id: Yup.number()
    .typeError("Home team is required")
    .required("Home team is required"),
  away_team_id: Yup.number()
    .typeError("Away team is required")
    .required("Away team is required")
    .notOneOf([Yup.ref("home_team_id")], "Away team must differ from home team"),
});

function GamesPage() {
  const [games, setGames] = useState([]);
  const [teams, setTeams] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/games")
      .then((res) => res.json())
      .then((data) => setGames(data))
      .catch(() => setError("Failed to load games."));

    fetch("/teams")
      .then((res) => res.json())
      .then((data) => setTeams(data))
      .catch(() => setError("Failed to load teams."));
  }, []);

  function handleSubmit(values, { setSubmitting, resetForm, setErrors }) {
    fetch("/games", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        date: values.date,
        home_team_id: Number(values.home_team_id),
        away_team_id: Number(values.away_team_id),
      }),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then((err) => {
            throw err;
          });
        }
        return res.json();
      })
      .then((newGame) => {
        setGames((prev) => [...prev, newGame]);
        resetForm();
      })
      .catch((err) => {
        setErrors({ date: err.errors ? err.errors.join(", ") : "Something went wrong" });
      })
      .finally(() => setSubmitting(false));
  }

  return (
    <div>
      <h1>Games</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Schedule a New Game</h2>
      <Formik
        initialValues={{ date: "", home_team_id: "", away_team_id: "" }}
        validationSchema={GameSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form>
            <label htmlFor="date">Date:</label>
            <Field id="date" name="date" type="datetime-local" />
            <ErrorMessage name="date" component="div" style={{ color: "red" }} />

            <div>
              <label htmlFor="home_team_id">Home Team:</label>
              <Field as="select" id="home_team_id" name="home_team_id">
                <option value="">Select a team</option>
                {teams.map((team) => (
                  <option key={team.id} value={team.id}>
                    {team.name}
                  </option>
                ))}
              </Field>
              <ErrorMessage name="home_team_id" component="div" style={{ color: "red" }} />
            </div>

            <div>
              <label htmlFor="away_team_id">Away Team:</label>
              <Field as="select" id="away_team_id" name="away_team_id">
                <option value="">Select a team</option>
                {teams.map((team) => (
                  <option key={team.id} value={team.id}>
                    {team.name}
                  </option>
                ))}
              </Field>
              <ErrorMessage name="away_team_id" component="div" style={{ color: "red" }} />
            </div>

            <button type="submit" disabled={isSubmitting}>
              Add Game
            </button>
          </Form>
        )}
      </Formik>

      <h2>All Games</h2>
      <ul>
        {games.map((game) => (
          <li key={game.id}>
            {game.date} — {game.home_team?.name} vs {game.away_team?.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default GamesPage;
