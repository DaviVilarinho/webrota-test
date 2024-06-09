import { LoginForm } from "@/interfaces/LoginForm";
import type UserCoordinates from "@/interfaces/UserCoordinates";
import { BASE_API } from "@/http/baseApi";

interface ApiUserCoordinates {
  "date_time": string;
  "latitude": number;
  "longitude": number;
}

export const getUserCoordinates = async (username: string, token: string) => {
  const response = await fetch(`${BASE_API}/user-coordinates/${username}`, {
    headers: {
      "x-access-token": token,
      username,
    },
  });

  return (await response.json()).map((
    apiUserCoordinate: ApiUserCoordinates,
  ) => ({
    date_time: apiUserCoordinate.date_time,
    lat: apiUserCoordinate.latitude,
    lng: apiUserCoordinate.longitude,
  })) as Array<UserCoordinates>;
};

export const login = async (loginForm: LoginForm) => {
  console.log(loginForm);
  const response = await fetch(
    `${BASE_API}/login?hashed_password=${loginForm.hashedPassword}&username=${loginForm.username}`,
  );

  if (response.status > 300) {
    throw new Error("Auth error");
  }

  return response.text();
};

export const register = async (registerForm: LoginForm) => {
  console.log(registerForm);
  const response = await fetch(`${BASE_API}/users`, {
    method: "POST",
    body: JSON.stringify(registerForm),
  });

  if (response.status > 300) {
    throw new Error("Auth error");
  }

  return response.text();
};
