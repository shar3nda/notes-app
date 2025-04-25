import { QueryClient } from "@tanstack/react-query";
import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";
import type { paths } from "./api-gen";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});
const fetchClient = createFetchClient<paths>({
  baseUrl: import.meta.env.VITE_API_PREFIX,
});
export const $api = createClient(fetchClient);
