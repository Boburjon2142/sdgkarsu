"use client";

import { useEffect, useState } from "react";

import { apiFetch } from "../../lib/api";
import { ProtectedRoute } from "../../components/protected-route";


export default function ProjectsPage() {
  return (
    <ProtectedRoute>
      {() => <ProjectsContent />}
    </ProtectedRoute>
  );
}


function ProjectsContent() {
  const [state, setState] = useState({ loading: true, results: [], error: "" });

  useEffect(() => {
    apiFetch("/api/projects/")
      .then((data) => setState({ loading: false, results: data.results || [], error: "" }))
      .catch((err) => setState({ loading: false, results: [], error: err.message }));
  }, []);

  if (state.loading) {
    return <div className="card">Loading projects…</div>;
  }

  return (
    <section className="stack">
      <div className="card">
        <h1>Projects</h1>
        <p className="muted">Only projects the signed-in user can access are returned by the API.</p>
      </div>
      {state.error ? <p className="error">{state.error}</p> : null}
      {state.results.map((project) => (
        <article className="card" key={project.id}>
          <h2>{project.title}</h2>
          <p>{project.description}</p>
          <p className="muted">Status: {project.status}</p>
        </article>
      ))}
    </section>
  );
}
