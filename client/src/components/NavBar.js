import React from "react";
import { NavLink } from "react-router-dom";

function NavBar({ currentUser, onLogout }) {
  const linkStyle = {
    marginRight: "1rem",
    textDecoration: "none",
    color: "#0b3d91",
    fontWeight: "bold",
  };

  const activeStyle = {
    textDecoration: "underline",
  };

  return (
    <nav style={{ padding: "1rem", borderBottom: "2px solid #0b3d91", marginBottom: "1rem" }}>
      <h2 style={{ display: "inline-block", marginRight: "2rem" }}>⚽ Football League</h2>
      <NavLink exact to="/" style={linkStyle} activeStyle={activeStyle}>
        Home
      </NavLink>
      <NavLink to="/teams" style={linkStyle} activeStyle={activeStyle}>
        Teams
      </NavLink>
      <NavLink to="/players" style={linkStyle} activeStyle={activeStyle}>
        Players
      </NavLink>
      <NavLink to="/games" style={linkStyle} activeStyle={activeStyle}>
        Games
      </NavLink>
      {currentUser ? (
        <>
          <span style={{ marginRight: "1rem" }}>Logged in as {currentUser.username}</span>
          <button onClick={onLogout}>Log Out</button>
        </>
      ) : (
        <>
          <NavLink to="/login" style={linkStyle} activeStyle={activeStyle}>
            Log In
          </NavLink>
          <NavLink to="/signup" style={linkStyle} activeStyle={activeStyle}>
            Sign Up
          </NavLink>
        </>
      )}
    </nav>
  );
}

export default NavBar;
