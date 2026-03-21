"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { apiFetch, getCsrfToken } from "../../../lib/api";


export default function LoginPage() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const router = useRouter();

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    try {
      const csrfToken = await getCsrfToken();
      await apiFetch("/api/auth/login/", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: JSON.stringify(form),
      });
      router.push("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="card">
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" type="email" autoComplete="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <input id="password" type="password" autoComplete="current-password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        </div>
        <button className="button" type="submit">Sign in</button>
        {error ? <p className="error">{error}</p> : null}
      </form>
    </section>
  );
}
