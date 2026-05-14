"use client";

import { useEffect, useState } from "react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import {
  AnalyticsSummary,
  getAnalyticsSummary,
} from "@/services/analytics-service";

export default function DashboardPage() {
  const [data, setData] =
    useState<AnalyticsSummary | null>(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
        try {
        const response =
            await getAnalyticsSummary();

        setData(response);
        } catch (error) {
        console.error(error);
        } finally {
        setLoading(false);
        }
    };

    fetchAnalytics();

    const socket = new WebSocket(
        "ws://127.0.0.1:8000/ws/events"
    );

    socket.onmessage = async () => {
        const updated =
        await getAnalyticsSummary();

        setData(updated);
    };

    return () => {
        socket.close();
    };
    }, []);

  if (loading) {
    return (
      <div className="p-10">
        Loading analytics...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 p-10">
      <div className="mb-10 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold">
            Analytics Dashboard
          </h1>

          <p className="mt-2 text-slate-600">
            Realtime event monitoring platform
          </p>
        </div>
      </div>

      <div className="mb-8 grid grid-cols-1 gap-6 md:grid-cols-3">
        <div className="rounded-2xl bg-white p-6 shadow">
          <p className="text-sm text-slate-500">
            Total Events
          </p>

          <h2 className="mt-3 text-5xl font-bold">
            {data?.total_events}
          </h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow">
          <p className="text-sm text-slate-500">
            Event Types
          </p>

          <h2 className="mt-3 text-5xl font-bold">
            {data?.events_by_name.length}
          </h2>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow">
          <p className="text-sm text-slate-500">
            System Status
          </p>

          <h2 className="mt-3 text-2xl font-bold text-green-600">
            Healthy
          </h2>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
        <div className="rounded-2xl bg-white p-6 shadow">
          <h2 className="mb-6 text-2xl font-bold">
            Events Breakdown
          </h2>

          <div className="space-y-4">
            {data?.events_by_name.map((event) => (
              <div
                key={event.event_name}
                className="flex items-center justify-between rounded-xl border p-4"
              >
                <span className="font-medium">
                  {event.event_name}
                </span>

                <span className="rounded-full bg-slate-100 px-4 py-1 font-bold">
                  {event.count}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow">
          <h2 className="mb-6 text-2xl font-bold">
            Event Volume
          </h2>

          <div className="h-[300px]">
            <ResponsiveContainer
              width="100%"
              height="100%"
            >
              <BarChart
                data={data?.events_by_name}
              >
                <XAxis dataKey="event_name" />

                <YAxis />

                <Tooltip />

                <Bar
                  dataKey="count"
                  radius={[10, 10, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}