import { CheckCircle2, Clock3, Loader2 } from "lucide-react";

const workflowSteps = [
  { label: "Plan research", status: "done" },
  { label: "Find evidence", status: "running" },
  { label: "Review draft", status: "waiting" }
];

export function ActiveWorkflow() {
  return (
    <aside className="rounded-md border bg-[#17241f] p-6 text-white shadow-soft">
      <p className="text-sm font-semibold uppercase text-[#64d6c4]">Current workflow</p>
      <h2 className="mt-2 text-2xl font-bold">AI data engineering trends</h2>
      <p className="mt-3 text-sm leading-6 text-white/70">
        Demo workflow preview. Real run status will connect after the research workflow days.
      </p>

      <div className="mt-6 space-y-3">
        {workflowSteps.map((step) => (
          <div key={step.label} className="flex items-center gap-3 rounded-md border border-white/10 bg-white/8 p-3">
            {step.status === "done" ? (
              <CheckCircle2 className="h-5 w-5 text-[#64d6c4]" aria-hidden="true" />
            ) : step.status === "running" ? (
              <Loader2 className="h-5 w-5 animate-spin text-[#f9b24a]" aria-hidden="true" />
            ) : (
              <Clock3 className="h-5 w-5 text-white/58" aria-hidden="true" />
            )}
            <span className="text-sm font-semibold">{step.label}</span>
          </div>
        ))}
      </div>
    </aside>
  );
}

