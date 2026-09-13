'use client';

import { useState } from 'react';

interface DashboardStats {
  totalUsers: number;
  activeSubscriptions: number;
  monthlyRevenue: number;
  apiCalls: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalUsers: 1234,
    activeSubscriptions: 89,
    monthlyRevenue: 12450,
    apiCalls: 52000,
  });

  return (
    <section id="dashboard" className="space-y-6">
      <h2 className="text-2xl font-bold">Dashboard</h2>
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          label="Total Users"
          value={stats.totalUsers.toLocaleString()}
          trend="+12%"
          positive
        />
        <StatCard
          label="Active Subscriptions"
          value={stats.activeSubscriptions.toLocaleString()}
          trend="+5%"
          positive
        />
        <StatCard
          label="Monthly Revenue"
          value={`$${stats.monthlyRevenue.toLocaleString()}`}
          trend="+18%"
          positive
        />
        <StatCard
          label="API Calls"
          value={stats.apiCalls.toLocaleString()}
          trend="-2%"
          positive={false}
        />
      </div>
    </section>
  );
}

interface StatCardProps {
  label: string;
  value: string;
  trend: string;
  positive: boolean;
}

function StatCard({ label, value, trend, positive }: StatCardProps) {
  return (
    <div className="rounded-xl border border-gray-200 p-6 shadow-sm transition hover:shadow-md dark:border-gray-800">
      <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
      <p className="mt-2 text-3xl font-bold">{value}</p>
      <p
        className={`mt-1 text-sm ${
          positive ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
        }`}
      >
        {trend}
      </p>
    </div>
  );
}