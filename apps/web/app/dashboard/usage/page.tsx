import { BarChart3 } from "lucide-react";

import { PlaceholderPanel } from "@/features/dashboard/placeholder-panel";

export default function UsagePage() {
  return (
    <PlaceholderPanel
      icon={BarChart3}
      eyebrow="Usage"
      title="Usage analytics arrives on Day 14"
      description="Token totals, cost estimates, daily usage, and model-level usage charts will land here."
      primaryActionLabel="Back to dashboard"
      primaryActionHref="/dashboard"
    />
  );
}

