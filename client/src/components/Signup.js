import React from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { useHistory } from "react-router-dom";

const SignupSchema = Yup.object().shape({
  username: Yup.string()
    .min(2, "Username must be at least 2 characters")
    .max(50, "Username must be 50 characters or less")
    .required("Username is required"),
  password: Yup.string()
    .min(6, "Password must be at least 6 characters")
    .required("Password is required"),
});

function Signup({ onLogin }) {
  const history = useHistory();

  function handleSubmit(values, { setSubmitting, setErrors }) {
    fetch("/signup", {
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
      .then((user) => {
        onLogin(user);
        history.push("/");
      })
      .catch((err) => {
        setErrors({
          username: err.errors ? err.errors.join(", ") : "Something went wrong",
        });
      })
      .finally(() => setSubmitting(false));
  }

  return (
    <div>
      <h1>Sign Up</h1>
      <Formik
        initialValues={{ username: "", password: "" }}
        validationSchema={SignupSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form>
            <label htmlFor="username">Username:</label>
            <Field id="username" name="username" type="text" />
            <ErrorMessage name="username" component="div" style={{ color: "red" }} />

            <div>
              <label htmlFor="password">Password:</label>
              <Field id="password" name="password" type="password" />
              <ErrorMessage name="password" component="div" style={{ color: "red" }} />
            </div>

            <button type="submit" disabled={isSubmitting}>
              Sign Up
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default Signup;
