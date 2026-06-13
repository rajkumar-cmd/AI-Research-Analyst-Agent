import { FileText } from "lucide-react";

import { PlaceholderPanel } from "@/features/dashboard/placeholder-panel";

export default function ReportsPage() {
  return (
    <PlaceholderPanel
      icon={FileText}
      eyebrow="Report history"
      title="Report history is planned for Day 13"
      description="This page will list previous reports, filters, report readers, source detail, and export actions."
      primaryActionLabel="Back to dashboard"
      primaryActionHref="/dashboard"
    />
  );
}

