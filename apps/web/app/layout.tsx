import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "research-agent-os",
  description:
    "AI Research Analyst OS for reliable multi-step research workflows with LangGraph, hybrid retrieval, source validation, and observability."
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
