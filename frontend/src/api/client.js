import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const client = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const submitEvent = async (description) => {
  const response = await client.post("/events/", { description });
  return response.data;
};

export const getHistory = async () => {
  const response = await client.get("/events/");
  return response.data;
};

export default client;
