import React, { useEffect, useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const TeamSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Name must be at least 2 characters")
    .max(50, "Name must be 50 characters or less")
    .required("Team name is required"),
});

function TeamsPage({ currentUser }) {
  const [teams, setTeams] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/teams")
      .then((res) => res.json())
      .then((data) => setTeams(data))
      .catch(() => setError("Failed to load teams."));
  }, []);

  function handleSubmit(values, { setSubmitting, resetForm, setErrors }) {
    fetch("/teams", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(values),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then((err) => {
            throw err;
          });
        }
        return res.json();
      })
      .then((newTeam) => {
        setTeams((prev) => [...prev, newTeam]);
        resetForm();
      })
      .catch((err) => {
        setErrors({ name: err.errors ? err.errors.join(", ") : "Something went wrong" });
      })
      .finally(() => setSubmitting(false));
  }

  function handleDelete(id) {
    fetch(`/teams/${id}`, { method: "DELETE", credentials: "include" }).then((res) => {
      if (res.ok || res.status === 204) {
        setTeams((prev) => prev.filter((t) => t.id !== id));
      }
    });
  }

  return (
    <div>
      <h1>Teams</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Add a New Team</h2>
      <Formik
        initialValues={{ name: "" }}
        validationSchema={TeamSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form>
            <label htmlFor="name">Team Name:</label>
            <Field id="name" name="name" type="text" />
            <ErrorMessage name="name" component="div" style={{ color: "red" }} />
            <button type="submit" disabled={isSubmitting}>
              Add Team
            </button>
          </Form>
        )}
      </Formik>

      <h2>All Teams</h2>
      <ul>
        {teams.map((team) => (
          <li key={team.id}>
            {team.name}
            {currentUser && (
              <button onClick={() => handleDelete(team.id)} style={{ marginLeft: "1rem" }}>
                Delete
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TeamsPage;
