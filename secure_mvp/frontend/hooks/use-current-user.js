"use client";

import { useEffect, useState } from "react";

import { apiFetch } from "../lib/api";


export function useCurrentUser() {
  const [state, setState] = useState({
    loading: true,
    user: null,
    error: "",
  });

  useEffect(() => {
    let active = true;

    apiFetch("/api/auth/me/")
      .then((user) => {
        if (!active) return;
        setState({ loading: false, user, error: "" });
      })
      .catch((error) => {
        if (!active) return;
        setState({ loading: false, user: null, error: error.message });
      });

    return () => {
      active = false;
    };
  }, []);

  return state;
}
