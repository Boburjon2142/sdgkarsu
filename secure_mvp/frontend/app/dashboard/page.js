import { ProtectedRoute } from "../../components/protected-route";


export default function DashboardPage() {
  return (
    <ProtectedRoute>
      {(user) => (
        <section className="card">
          <h1>Dashboard</h1>
          <p className="muted">Welcome, {user.first_name || user.email}.</p>
          <p>Your current role is <strong>{user.role}</strong>.</p>
        </section>
      )}
    </ProtectedRoute>
  );
}
