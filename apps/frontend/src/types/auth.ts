export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  organization_name: string;
}

export interface AuthResponse {
  access_token: string;
}