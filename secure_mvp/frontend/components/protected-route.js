"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useCurrentUser } from "../hooks/use-current-user";


export function ProtectedRoute({ children, requireAdmin = false }) {
  const state = useCurrentUser();
  const router = useRouter();

  useEffect(() => {
    if (state.loading) return;
    if (!state.user) {
      router.replace("/login");
      return;
    }
    if (requireAdmin && state.user.role !== "admin") {
      router.replace("/dashboard");
    }
  }, [requireAdmin, router, state.loading, state.user]);

  if (state.loading) {
    return <div className="card">Checking your session…</div>;
  }

  if (!state.user) {
    return null;
  }

  return children(state.user);
}
