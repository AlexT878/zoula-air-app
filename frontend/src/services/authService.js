const API_URL = import.meta.env.VITE_API_URL;

export async function loginUser(email, password) {
  const payload = new URLSearchParams();
  payload.append("username", email);
  payload.append("password", password);

  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
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
    return data;
  } catch (error) {
    console.log(error.message);
    if (!error.status) {
      error.status = 500;
    }
    throw error;
  }
}
