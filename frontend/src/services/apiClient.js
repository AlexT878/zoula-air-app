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

    return data.access_token;
  } catch (error) {
    console.log(error);
    useAuthStore.getState().logout();
    return null;
  }
}

export async function apiFetch(endpoint, options = {}) {
  let token = useAuthStore.getState().accessToken;

  if (
    !token &&
    !endpoint.includes("/auth/login") &&
    !endpoint.includes("/auth/refresh")
  ) {
    token = await refreshAccessToken();
  }

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

  if (response.status === 401 && !endpoint.includes("/auth/login")) {
    const newToken = await refreshAccessToken();
    if (newToken) {
      response = await sendRequest(newToken);
    }
  }

  return response;
}
