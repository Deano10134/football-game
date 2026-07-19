import React from "react";
import { Switch, Route } from "react-router-dom";
import NavBar from "./NavBar";
import Home from "./Home";
import TeamsPage from "./TeamsPage";
import PlayersPage from "./PlayersPage";
import GamesPage from "./GamesPage";

function App() {
  return (
    <div>
      <NavBar />
      <div style={{ padding: "0 1rem" }}>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/teams" component={TeamsPage} />
          <Route path="/players" component={PlayersPage} />
          <Route path="/games" component={GamesPage} />
        </Switch>
      </div>
    </div>
  );
}

export default App;
