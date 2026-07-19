import React, { useEffect, useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const ReviewSchema = Yup.object().shape({
  targetType: Yup.string()
    .oneOf(["team", "player"], "Must choose team or player")
    .required("Please choose what to review"),
  targetId: Yup.number()
    .typeError("Please select a team or player")
    .required("Please select a team or player"),
  rating: Yup.number()
    .typeError("Rating is required")
    .min(1, "Rating must be between 1 and 5")
    .max(5, "Rating must be between 1 and 5")
    .required("Rating is required"),
  content: Yup.string()
    .min(2, "Review must be at least 2 characters")
    .max(500, "Review must be 500 characters or less")
    .required("Review content is required"),
});

function ReviewsPage({ currentUser }) {
  const [reviews, setReviews] = useState([]);
  const [teams, setTeams] = useState([]);
  const [players, setPlayers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/reviews")
      .then((res) => res.json())
      .then((data) => setReviews(data))
      .catch(() => setError("Failed to load reviews."));

    fetch("/teams")
      .then((res) => res.json())
      .then((data) => setTeams(data))
      .catch(() => setError("Failed to load teams."));

    fetch("/players")
      .then((res) => res.json())
      .then((data) => setPlayers(data))
      .catch(() => setError("Failed to load players."));
  }, []);

  function handleSubmit(values, { setSubmitting, resetForm, setErrors }) {
    const body = {
      content: values.content,
      rating: Number(values.rating),
      team_id: values.targetType === "team" ? Number(values.targetId) : null,
      player_id: values.targetType === "player" ? Number(values.targetId) : null,
    };

    fetch("/reviews", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(body),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then((err) => {
            throw err;
          });
        }
        return res.json();
      })
      .then((newReview) => {
        setReviews((prev) => [...prev, newReview]);
        resetForm();
      })
      .catch((err) => {
        setErrors({
          content: err.errors ? err.errors.join(", ") : err.error || "Something went wrong",
        });
      })
      .finally(() => setSubmitting(false));
  }

  function handleDelete(id) {
    fetch(`/reviews/${id}`, { method: "DELETE", credentials: "include" }).then((res) => {
      if (res.ok || res.status === 204) {
        setReviews((prev) => prev.filter((r) => r.id !== id));
      }
    });
  }

  function reviewTarget(review) {
    if (review.team) return `Team: ${review.team.name}`;
    if (review.player) return `Player: ${review.player.name}`;
    return "Unknown";
  }

  return (
    <div>
      <h1>Reviews</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}

      {currentUser ? (
        <>
          <h2>Leave a Review</h2>
          <Formik
            initialValues={{ targetType: "", targetId: "", rating: "", content: "" }}
            validationSchema={ReviewSchema}
            onSubmit={handleSubmit}
          >
            {({ values, isSubmitting }) => (
              <Form>
                <div>
                  <label htmlFor="targetType">Review a:</label>
                  <Field as="select" id="targetType" name="targetType">
                    <option value="">Select type</option>
                    <option value="team">Team</option>
                    <option value="player">Player</option>
                  </Field>
                  <ErrorMessage name="targetType" component="div" style={{ color: "red" }} />
                </div>

                {values.targetType === "team" && (
                  <div>
                    <label htmlFor="targetId">Team:</label>
                    <Field as="select" id="targetId" name="targetId">
                      <option value="">Select a team</option>
                      {teams.map((team) => (
                        <option key={team.id} value={team.id}>
                          {team.name}
                        </option>
                      ))}
                    </Field>
                    <ErrorMessage name="targetId" component="div" style={{ color: "red" }} />
                  </div>
                )}

                {values.targetType === "player" && (
                  <div>
                    <label htmlFor="targetId">Player:</label>
                    <Field as="select" id="targetId" name="targetId">
                      <option value="">Select a player</option>
                      {players.map((player) => (
                        <option key={player.id} value={player.id}>
                          {player.name}
                        </option>
                      ))}
                    </Field>
                    <ErrorMessage name="targetId" component="div" style={{ color: "red" }} />
                  </div>
                )}

                <div>
                  <label htmlFor="rating">Rating (1-5):</label>
                  <Field id="rating" name="rating" type="number" min="1" max="5" />
                  <ErrorMessage name="rating" component="div" style={{ color: "red" }} />
                </div>

                <div>
                  <label htmlFor="content">Review:</label>
                  <Field id="content" name="content" as="textarea" />
                  <ErrorMessage name="content" component="div" style={{ color: "red" }} />
                </div>

                <button type="submit" disabled={isSubmitting}>
                  Submit Review
                </button>
              </Form>
            )}
          </Formik>
        </>
      ) : (
        <p>Log in to leave a review.</p>
      )}

      <h2>All Reviews</h2>
      <ul>
        {reviews.map((review) => (
          <li key={review.id}>
            {reviewTarget(review)} — Rating: {review.rating}/5 — "{review.content}"
            {review.user && <em> (by {review.user.username})</em>}
            {currentUser && currentUser.id === review.user_id && (
              <button onClick={() => handleDelete(review.id)} style={{ marginLeft: "1rem" }}>
                Delete
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ReviewsPage;
