import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import NavBar from "./NavBar";
import Home from "./Home";
import TeamsPage from "./TeamsPage";
import PlayersPage from "./PlayersPage";
import GamesPage from "./GamesPage";
import ReviewsPage from "./ReviewsPage";
import Signup from "./Signup";
import Login from "./Login";

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch("/check_session", { credentials: "include" })
      .then((res) => {
        if (res.ok) {
          return res.json().then((user) => setCurrentUser(user));
        }
      })
      .finally(() => setIsLoading(false));
  }, []);

  function handleLogin(user) {
    setCurrentUser(user);
  }

  function handleLogout() {
    fetch("/logout", { method: "DELETE", credentials: "include" }).then(() => {
      setCurrentUser(null);
    });
  }

  if (isLoading) return <h1>Loading...</h1>;

  return (
    <div>
      <NavBar currentUser={currentUser} onLogout={handleLogout} />
      <div style={{ padding: "0 1rem" }}>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route
            path="/teams"
            render={(props) => <TeamsPage {...props} currentUser={currentUser} />}
          />
          <Route
            path="/players"
            render={(props) => <PlayersPage {...props} currentUser={currentUser} />}
          />
          <Route path="/games" component={GamesPage} />
          <Route
            path="/reviews"
            render={(props) => <ReviewsPage {...props} currentUser={currentUser} />}
          />
          <Route
            path="/signup"
            render={(props) => <Signup {...props} onLogin={handleLogin} />}
          />
          <Route
            path="/login"
            render={(props) => <Login {...props} onLogin={handleLogin} />}
          />
        </Switch>
      </div>
    </div>
  );
}

export default App;
