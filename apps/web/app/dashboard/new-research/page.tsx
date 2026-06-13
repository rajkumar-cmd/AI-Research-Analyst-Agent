import { SearchCheck } from "lucide-react";

import { PlaceholderPanel } from "@/features/dashboard/placeholder-panel";

export default function NewResearchPage() {
  return (
    <PlaceholderPanel
      icon={SearchCheck}
      eyebrow="New research"
      title="Research creation arrives on Day 9"
      description="This shell is ready for the query form, run creation call, progress timeline, and approval actions."
      primaryActionLabel="Back to dashboard"
      primaryActionHref="/dashboard"
    />
  );
}

