import { QueryClient } from "@tanstack/react-query";
import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";
import type { paths } from "./api-gen";
import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  saveTokens,
} from "./auth";
import { TokenResponse } from "./types/auth";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const fetchWithRetry = async (request: Request) => {
  const url = new URL(request.url, window.location.origin);

  if (url.pathname.startsWith(`${import.meta.env.VITE_API_PREFIX}/auth/`)) {
    return fetch(request);
  }

  let authRequest = request.clone();

  const token = getAccessToken();
  if (!token) {
    clearTokens();
    setTimeout(() => {
      window.location.reload();
    }, 0);
    throw new Error("Unauthorized, reloading...");
  }

  authRequest.headers.set("Authorization", `Bearer ${token}`);

  let response = await fetch(authRequest);

  if (response.status !== 401) {
    return response;
  }

  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    clearTokens();
    return response;
  }

  const formData = new FormData();
  formData.append("refresh_token", refreshToken);
  formData.append("grant_type", "refresh_token");
  const refreshResponse = await fetch(
    `${import.meta.env.VITE_API_PREFIX}/auth/token`,
    {
      method: "POST",
      body: formData,
    },
  );
  if (!refreshResponse.ok) {
    clearTokens();
    return response;
  }

  const tokens: TokenResponse = await refreshResponse.json();
  if (!tokens.access_token) {
    clearTokens();
    return response;
  }

  saveTokens(tokens);

  request.headers.set("Authorization", `Bearer ${getAccessToken()}`);

  response = await fetch(request);
  return response;
};

export const fetchClient = createFetchClient<paths>({
  baseUrl: import.meta.env.VITE_API_PREFIX,
  fetch: fetchWithRetry,
});
export const $api = createClient(fetchClient);
