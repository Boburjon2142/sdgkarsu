"use client";

import { useRouter } from "next/navigation";

import { useCurrentUser } from "../hooks/use-current-user";
import { apiFetch, getCsrfToken } from "../lib/api";


export function Navigation() {
  const { user } = useCurrentUser();
  const router = useRouter();

  async function handleLogout() {
    try {
      const csrfToken = await getCsrfToken();
      await apiFetch("/api/auth/logout/", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
      });
    } finally {
      router.push("/login");
      router.refresh();
    }
  }

  return (
    <header className="nav">
      <strong>Secure MVP</strong>
      <nav className="nav__links">
        <a href="/">Home</a>
        {user ? <a href="/projects">Projects</a> : null}
        {user ? <a href="/dashboard">Dashboard</a> : null}
        {user?.role === "admin" ? <a href="/admin">Admin</a> : null}
        {!user ? <a href="/login">Login</a> : null}
        {!user ? <a href="/register">Register</a> : null}
        {user ? (
          <button className="button button--secondary" type="button" onClick={handleLogout}>
            Logout
          </button>
        ) : null}
      </nav>
    </header>
  );
}
