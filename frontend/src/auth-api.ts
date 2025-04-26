import { fetchClient } from "./api";
import { saveTokens } from "./auth";
import type { AuthForm } from "./types/auth";

export async function login(username: string, password: string) {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);
  formData.append("grant_type", "password");
  const { data, error } = await fetchClient.POST("/auth/token", {
    body: formData as AuthForm,
  });
  if (error) {
    throw new Error(`${error.detail}`);
  }
  if (!data) {
    throw new Error("No data returned");
  }
  saveTokens(data);
}

export async function register(username: string, password: string) {
  const { data, error } = await fetchClient.POST("/auth/register", {
    body: { username, password },
  });
  if (error) {
    throw new Error(`${error.detail}`);
  }
  if (!data) {
    throw new Error("No data returned");
  }
  saveTokens(data);
}
