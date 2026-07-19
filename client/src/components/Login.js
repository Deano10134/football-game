import React from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { useHistory } from "react-router-dom";

const LoginSchema = Yup.object().shape({
  username: Yup.string().required("Username is required"),
  password: Yup.string().required("Password is required"),
});

function Login({ onLogin }) {
  const history = useHistory();

  function handleSubmit(values, { setSubmitting, setErrors }) {
    fetch("/login", {
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
        setErrors({ username: err.error || "Invalid username or password" });
      })
      .finally(() => setSubmitting(false));
  }

  return (
    <div>
      <h1>Log In</h1>
      <Formik
        initialValues={{ username: "", password: "" }}
        validationSchema={LoginSchema}
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
              Log In
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default Login;
