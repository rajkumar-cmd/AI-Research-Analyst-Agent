import type { Metadata } from "next";

import { DashboardShell } from "@/features/dashboard/dashboard-shell";

export const metadata: Metadata = {
  title: "Dashboard | research-agent-os",
  description: "Research Agent OS dashboard workspace."
};

export default function DashboardLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <DashboardShell>{children}</DashboardShell>;
}

