import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const data = [
  { time: "09:00", count: 12 },
  { time: "10:00", count: 25 },
  { time: "11:00", count: 40 },
  { time: "12:00", count: 65 },
  { time: "13:00", count: 52 },
  { time: "14:00", count: 80 },
  { time: "15:00", count: 95 },
  { time: "16:00", count: 60 }
];

const SlackChart = () => {
  return (
    <div className="bg-[#0f172a] p-6 rounded-2xl shadow-lg w-full h-[280px]">
      <h3 className="text-white text-lg font-semibold mb-4">
        Slack Activity (Hourly)
      </h3>

      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />

          {/* TIME AXIS */}
          <XAxis dataKey="time" stroke="#94a3b8" />

          <YAxis stroke="#94a3b8" />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="count"
            stroke="#38bdf8"
            strokeWidth={3}
            dot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SlackChart;
