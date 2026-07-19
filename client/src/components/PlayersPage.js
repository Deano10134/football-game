import React, { useEffect, useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const POSITIONS = ["GK", "CB", "LB", "RB", "CDM", "CM", "CAM", "LM", "RM", "LW", "RW", "ST"];

const PlayerSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Name must be at least 2 characters")
    .max(50, "Name must be 50 characters or less")
    .required("Player name is required"),
  position: Yup.string()
    .oneOf(POSITIONS, "Must be a valid position")
    .required("Position is required"),
  team_id: Yup.number()
    .typeError("Team is required")
    .required("Team is required"),
});

function PlayersPage() {
  const [players, setPlayers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [error, setError] = useState(null);
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetch("/players")
      .then((res) => res.json())
      .then((data) => setPlayers(data))
      .catch(() => setError("Failed to load players."));

    fetch("/teams")
      .then((res) => res.json())
      .then((data) => setTeams(data))
      .catch(() => setError("Failed to load teams."));
  }, []);

  function handleCreate(values, { setSubmitting, resetForm, setErrors }) {
    fetch("/players", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: values.name,
        position: values.position,
        team_id: Number(values.team_id),
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
      .then((newPlayer) => {
        setPlayers((prev) => [...prev, newPlayer]);
        resetForm();
      })
      .catch((err) => {
        setErrors({ name: err.errors ? err.errors.join(", ") : "Something went wrong" });
      })
      .finally(() => setSubmitting(false));
  }

  function handleUpdate(id, values, { setSubmitting, setErrors }) {
    fetch(`/players/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: values.name,
        position: values.position,
        team_id: Number(values.team_id),
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
      .then((updatedPlayer) => {
        setPlayers((prev) =>
          prev.map((p) => (p.id === updatedPlayer.id ? updatedPlayer : p))
        );
        setEditingId(null);
      })
      .catch((err) => {
        setErrors({ name: err.errors ? err.errors.join(", ") : "Something went wrong" });
      })
      .finally(() => setSubmitting(false));
  }

  function handleDelete(id) {
    fetch(`/players/${id}`, { method: "DELETE" }).then((res) => {
      if (res.ok || res.status === 204) {
        setPlayers((prev) => prev.filter((p) => p.id !== id));
      }
    });
  }

  return (
    <div>
      <h1>Players</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Add a New Player</h2>
      <Formik
        initialValues={{ name: "", position: "", team_id: "" }}
        validationSchema={PlayerSchema}
        onSubmit={handleCreate}
      >
        {({ isSubmitting }) => (
          <Form>
            <label htmlFor="name">Name:</label>
            <Field id="name" name="name" type="text" />
            <ErrorMessage name="name" component="div" style={{ color: "red" }} />

            <div>
              <label htmlFor="position">Position:</label>
              <Field as="select" id="position" name="position">
                <option value="">Select a position</option>
                {POSITIONS.map((pos) => (
                  <option key={pos} value={pos}>
                    {pos}
                  </option>
                ))}
              </Field>
              <ErrorMessage name="position" component="div" style={{ color: "red" }} />
            </div>

            <div>
              <label htmlFor="team_id">Team:</label>
              <Field as="select" id="team_id" name="team_id">
                <option value="">Select a team</option>
                {teams.map((team) => (
                  <option key={team.id} value={team.id}>
                    {team.name}
                  </option>
                ))}
              </Field>
              <ErrorMessage name="team_id" component="div" style={{ color: "red" }} />
            </div>

            <button type="submit" disabled={isSubmitting}>
              Add Player
            </button>
          </Form>
        )}
      </Formik>

      <h2>All Players</h2>
      <ul>
        {players.map((player) =>
          editingId === player.id ? (
            <li key={player.id}>
              <Formik
                initialValues={{
                  name: player.name,
                  position: player.position,
                  team_id: player.team_id,
                }}
                validationSchema={PlayerSchema}
                onSubmit={(values, actions) => handleUpdate(player.id, values, actions)}
              >
                {({ isSubmitting }) => (
                  <Form>
                    <Field name="name" type="text" />
                    <ErrorMessage name="name" component="div" style={{ color: "red" }} />

                    <Field as="select" name="position">
                      {POSITIONS.map((pos) => (
                        <option key={pos} value={pos}>
                          {pos}
                        </option>
                      ))}
                    </Field>
                    <ErrorMessage name="position" component="div" style={{ color: "red" }} />

                    <Field as="select" name="team_id">
                      {teams.map((team) => (
                        <option key={team.id} value={team.id}>
                          {team.name}
                        </option>
                      ))}
                    </Field>
                    <ErrorMessage name="team_id" component="div" style={{ color: "red" }} />

                    <button type="submit" disabled={isSubmitting}>
                      Save
                    </button>
                    <button type="button" onClick={() => setEditingId(null)}>
                      Cancel
                    </button>
                  </Form>
                )}
              </Formik>
            </li>
          ) : (
            <li key={player.id}>
              {player.name} — {player.position} — {player.team?.name}
              <button onClick={() => setEditingId(player.id)} style={{ marginLeft: "1rem" }}>
                Edit
              </button>
              <button onClick={() => handleDelete(player.id)} style={{ marginLeft: "0.5rem" }}>
                Delete
              </button>
            </li>
          )
        )}
      </ul>
    </div>
  );
}

export default PlayersPage;
