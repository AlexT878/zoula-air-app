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

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    const result = await response.json();
    console.log(result);
  } catch (error) {
    console.log(error.message);
  }
}
