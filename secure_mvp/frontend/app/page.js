export default function HomePage() {
  return (
    <div className="stack">
      <section className="card">
        <h1>Secure Django + Next.js MVP</h1>
        <p className="muted">
          This frontend is built for a Django REST API secured with server-side sessions, CSRF protection,
          role-based access control, throttling, and audit logging.
        </p>
      </section>
      <section className="split">
        <article className="card">
          <h2>Security choices</h2>
          <p className="muted">
            The browser stores only an HttpOnly session cookie managed by the backend. No auth token is
            kept in localStorage.
          </p>
        </article>
        <article className="card">
          <h2>Deployment</h2>
          <p className="muted">
            Frontend can run on Vercel while the API runs on Render, Railway, or PythonAnywhere with
            explicit CORS and CSRF origin configuration.
          </p>
        </article>
      </section>
    </div>
  );
}
