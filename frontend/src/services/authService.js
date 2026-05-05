const API_URL = import.meta.env.VITE_API_URL;

import { useAuthStore } from "../store/useAuthStore";
import { apiFetch } from "./apiClient";

export async function loginUser(email, password) {
  const payload = new URLSearchParams();
  payload.append("username", email);
  payload.append("password", password);

  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: payload.toString(),
    });

    const data = await response.json();

    if (!response.ok) {
      const error = new Error(data.detail);
      console.log(response.status);
      error.status = response.status;
      throw error;
    }

    useAuthStore.getState().setAuth(data.user, data.access_token);
    localStorage.setItem("was_logged_in", "true");

    return data;
  } catch (error) {
    console.log(error.message);
    if (!error.status) {
      error.status = 500;
    }
    throw error;
  }
}

export async function logoutUser() {
  useAuthStore.setState({ isInitializing: true });

  try {
    const response = await apiFetch("/auth/logout", {
      method: "POST",
    });

    if (!response.ok) {
      console.warn("Logout error");
    }
  } catch (error) {
    console.error(error);
  } finally {
    localStorage.setItem("was_logged_in", "false");
    useAuthStore.getState().logout();
    window.location.href = "/";
  }
}
