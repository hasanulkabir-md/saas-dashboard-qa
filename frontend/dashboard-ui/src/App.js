import React, { useState, useEffect } from "react";

function App() {
  const [users, setUsers] = useState([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const fetchUsers = async () => {
    try {
      const res = await fetch("http://localhost:8000/user/list");
      if (!res.ok) throw new Error("Failed to fetch users");
      const data = await res.json();
      setUsers(data);
    } catch (err) {
      console.error("Fetch users error:", err);
    }
  };

  const createUser = async () => {
    try {
      const res = await fetch("http://localhost:8000/user/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email }),
      });
      if (!res.ok) throw new Error("Failed to create user");
      await res.json();
      fetchUsers();
    } catch (err) {
      console.error("Create user error:", err);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>SaaS Dashboard</h1>

      <h3>Create User</h3>
      <input
        placeholder="Name"
        data-testid="name"
        onChange={(e) => setName(e.target.value)}
      />
      <input
        placeholder="Email"
        data-testid="email"
        onChange={(e) => setEmail(e.target.value)}
      />
      <button data-testid="add-user" onClick={createUser}>
        Add User
      </button>

      <h3>User List</h3>
      <ul>
        {users.map((u, idx) => (
          <li key={idx}>
            {u.name} — {u.email}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
