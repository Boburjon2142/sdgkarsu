"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { apiFetch, getCsrfToken } from "../../../lib/api";


export default function RegisterPage() {
  const [form, setForm] = useState({
    email: "",
    username: "",
    first_name: "",
    last_name: "",
    password: "",
    password_confirm: "",
  });
  const [error, setError] = useState("");
  const router = useRouter();

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    try {
      const csrfToken = await getCsrfToken();
      await apiFetch("/api/auth/register/", {
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
      <h1>Create account</h1>
      <form onSubmit={handleSubmit}>
        <div className="split">
          <div className="field"><label>Email</label><input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></div>
          <div className="field"><label>Username</label><input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} /></div>
          <div className="field"><label>First name</label><input value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} /></div>
          <div className="field"><label>Last name</label><input value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} /></div>
          <div className="field"><label>Password</label><input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></div>
          <div className="field"><label>Confirm password</label><input type="password" value={form.password_confirm} onChange={(e) => setForm({ ...form, password_confirm: e.target.value })} /></div>
        </div>
        <button className="button" type="submit">Register</button>
        {error ? <p className="error">{error}</p> : null}
      </form>
    </section>
  );
}
