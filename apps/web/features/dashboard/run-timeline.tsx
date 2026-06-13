import { CheckCircle2, Clock3 } from "lucide-react";

type RunItem = {
  label: string;
  time: string;
  status: string;
};

export function RunTimeline({ runs }: { runs: RunItem[] }) {
  return (
    <div className="mt-5 space-y-4">
      {runs.map((run) => (
        <div key={run.label} className="flex gap-3">
          <div className="mt-0.5">
            {run.status === "completed" ? (
              <CheckCircle2 className="h-5 w-5 text-primary" aria-hidden="true" />
            ) : (
              <Clock3 className="h-5 w-5 text-[#f9b24a]" aria-hidden="true" />
            )}
          </div>
          <div>
            <p className="text-sm font-semibold">{run.label}</p>
            <p className="mt-1 text-xs text-muted-foreground">{run.time}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

