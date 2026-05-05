import { useAuthStore } from "../store/useAuthStore";

const API_URL = import.meta.env.VITE_API_URL;

export async function refreshAccessToken() {
  try {
    const response = await fetch(`${API_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) throw new Error("Refresh failed");

    const data = await response.json();
    useAuthStore.getState().setAuth(data.user, data.access_token);
    localStorage.setItem("was_logged_in", "true");
    return data.access_token;
  } catch (error) {
    console.log(error);
    localStorage.removeItem("was_logged_in");
    useAuthStore.getState().logout();
    return null;
  }
}

export async function apiFetch(endpoint, options = {}) {
  const token = useAuthStore.getState().accessToken;

  const sendRequest = async (currentToken) => {
    const defaultHeaders = {
      "Content-Type": "application/json",
      ...(currentToken && { Authorization: `Bearer ${currentToken}` }),
    };

    return await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
      credentials: "include",
    });
  };

  let response = await sendRequest(token);

  if (
    response.status === 401 &&
    !endpoint.includes("/auth/login") &&
    !endpoint.includes("/auth/refresh")
  ) {
    const newToken = await refreshAccessToken();
    if (newToken) {
      response = await sendRequest(newToken);
    }
  }

  return response;
}

export async function logoutUser() {
  useAuthStore.setState({ isInitializing: true });

  try {
    await apiFetch("/auth/logout", {
      method: "POST",
    });
  } catch (error) {
    console.error(error);
  } finally {
    localStorage.removeItem("was_logged_in");
    useAuthStore.getState().logout();
    window.location.href = "/";
  }
}
