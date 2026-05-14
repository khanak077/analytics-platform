import { api } from "./api";

import type {
  AuthResponse,
  LoginPayload,
  RegisterPayload,
} from "@/types/auth";

export const login = async (
  payload: LoginPayload
): Promise<AuthResponse> => {
  const response = await api.post("/auth/login", payload);

  return response.data;
};

export const register = async (
  payload: RegisterPayload
): Promise<AuthResponse> => {
  const response = await api.post("/auth/register", payload);

  return response.data;
};