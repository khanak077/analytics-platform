import { api } from "./api";

export interface AnalyticsSummary {
  total_events: number;

  events_by_name: {
    event_name: string;
    count: number;
  }[];
}

export const getAnalyticsSummary =
  async (): Promise<AnalyticsSummary> => {
    const token = localStorage.getItem("token");

    const response = await api.get(
      "/analytics/summary",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    return response.data;
  };