import { ProtectedRoute } from "../../components/protected-route";


export default function AdminPage() {
  return (
    <ProtectedRoute requireAdmin>
      {(user) => (
        <section className="card">
          <h1>Admin area</h1>
          <p className="muted">Only admin users should be able to stay on this route.</p>
          <p>Signed in as {user.email}.</p>
        </section>
      )}
    </ProtectedRoute>
  );
}
