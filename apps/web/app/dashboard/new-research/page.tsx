"use client";

import { useMemo, useState } from "react";
import {
  AlertCircle,
  CheckCircle2,
  ClipboardCheck,
  Clock3,
  FileText,
  ListChecks,
  PlayCircle,
  SearchCheck,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

const presetQueries = [
  "Research top trends in AI data engineering for 2026",
  "Compare enterprise copilots for finance operations teams",
  "Analyze vector database adoption across SaaS product teams",
];

const workflowSteps = [
  {
    id: "quota_guard",
    label: "Quota guard",
    description: "Daily allowance and request limits checked",
    icon: ShieldCheck,
  },
  {
    id: "planner_agent",
    label: "Planner agent",
    description: "Research scope, key questions, and source plan created",
    icon: ListChecks,
  },
  {
    id: "research_agent",
    label: "Research agent",
    description: "Initial market notes and evidence targets collected",
    icon: SearchCheck,
  },
  {
    id: "summarizer_agent",
    label: "Summarizer agent",
    description: "Findings converted into an executive brief",
    icon: FileText,
  },
  {
    id: "critic_agent",
    label: "Critic agent",
    description: "Gaps, unsupported claims, and risks reviewed",
    icon: AlertCircle,
  },
  {
    id: "human_approval",
    label: "Human approval",
    description: "Reviewer approval required before report writing",
    icon: ClipboardCheck,
  },
  {
    id: "report_writer_agent",
    label: "Report writer",
    description: "Approved draft converted into final report format",
    icon: Sparkles,
  },
];

const draftSections = [
  "Executive summary",
  "Market trends",
  "Competitor examples",
  "Risks and gaps",
  "Recommendations",
  "Source quality notes",
];

type RunStatus = "idle" | "running" | "waiting" | "approved";

export default function NewResearchPage() {
  const [query, setQuery] = useState(presetQueries[0]);
  const [audience, setAudience] = useState("Product and data leaders");
  const [depth, setDepth] = useState("Executive brief");
  const [status, setStatus] = useState<RunStatus>("idle");

  const activeStepIndex = useMemo(() => {
    if (status === "idle") {
      return -1;
    }

    if (status === "running" || status === "waiting") {
      return workflowSteps.findIndex((step) => step.id === "human_approval");
    }

    return workflowSteps.length - 1;
  }, [status]);

  const handleStartRun = () => {
    setStatus("running");
    window.setTimeout(() => setStatus("waiting"), 650);
  };

  const handleApprove = () => {
    setStatus("approved");
  };

  const handleReset = () => {
    setStatus("idle");
  };

  return (
    <div className="space-y-6">
      <section className="grid gap-4 xl:grid-cols-[1.05fr_0.95fr]">
        <div className="rounded-md border bg-white p-6 shadow-soft">
          <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase text-primary">New research</p>
              <h1 className="mt-2 text-3xl font-bold tracking-tight">Start a research run</h1>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
                Create a focused research request, review agent progress, and approve the draft before the report is finalized.
              </p>
            </div>
            <RunStatusBadge status={status} />
          </div>

          <div className="mt-6 grid gap-5">
            <div className="grid gap-2">
              <Label htmlFor="research-query">Research question</Label>
              <textarea
                id="research-query"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                className="min-h-28 w-full rounded-md border border-input bg-white px-3 py-3 text-sm leading-6 shadow-sm outline-none transition-colors placeholder:text-muted-foreground focus-visible:ring-2 focus-visible:ring-ring"
              />
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="grid gap-2">
                <Label htmlFor="audience">Audience</Label>
                <Input id="audience" value={audience} onChange={(event) => setAudience(event.target.value)} />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="depth">Output depth</Label>
                <select
                  id="depth"
                  value={depth}
                  onChange={(event) => setDepth(event.target.value)}
                  className="h-11 w-full rounded-md border border-input bg-white px-3 text-sm shadow-sm outline-none focus-visible:ring-2 focus-visible:ring-ring"
                >
                  <option>Executive brief</option>
                  <option>Detailed report</option>
                  <option>Board-ready memo</option>
                </select>
              </div>
            </div>

            <div className="grid gap-2">
              <p className="text-sm font-semibold">Quick starts</p>
              <div className="grid gap-2 lg:grid-cols-3">
                {presetQueries.map((preset) => (
                  <button
                    key={preset}
                    type="button"
                    onClick={() => setQuery(preset)}
                    className={cn(
                      "rounded-md border bg-[#f7fbfa] px-3 py-3 text-left text-sm font-semibold leading-5 transition-colors hover:border-primary hover:bg-white",
                      query === preset && "border-primary bg-white text-primary"
                    )}
                  >
                    {preset}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex flex-col gap-3 border-t pt-5 sm:flex-row sm:items-center sm:justify-between">
              <div className="text-sm text-muted-foreground">
                Estimated run: <span className="font-semibold text-foreground">7 agent steps</span> - approval required
              </div>
              <div className="flex gap-2">
                <Button type="button" variant="outline" onClick={handleReset}>
                  Reset
                </Button>
                <Button type="button" onClick={handleStartRun} disabled={!query.trim() || status === "running"}>
                  <PlayCircle className="h-4 w-4" aria-hidden="true" />
                  Start run
                </Button>
              </div>
            </div>
          </div>
        </div>

        <ApprovalPanel status={status} query={query} audience={audience} depth={depth} onApprove={handleApprove} />
      </section>

      <section className="grid gap-6 xl:grid-cols-[0.92fr_1.08fr]">
        <div className="rounded-md border bg-white p-6 shadow-soft">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-sm font-semibold uppercase text-primary">Workflow</p>
              <h2 className="mt-1 text-xl font-bold">Agent progress</h2>
            </div>
            <div className="rounded-md border bg-[#f7fbfa] px-3 py-2 text-sm font-semibold">
              {activeStepIndex < 0 ? "Ready" : `${Math.min(activeStepIndex + 1, workflowSteps.length)} / ${workflowSteps.length}`}
            </div>
          </div>

          <div className="mt-5 space-y-3">
            {workflowSteps.map((step, index) => (
              <WorkflowStepCard
                key={step.id}
                step={step}
                state={getStepState(index, activeStepIndex, status)}
              />
            ))}
          </div>
        </div>

        <DraftPreview query={query} audience={audience} depth={depth} status={status} />
      </section>
    </div>
  );
}

function RunStatusBadge({ status }: Readonly<{ status: RunStatus }>) {
  const labelByStatus = {
    idle: "Ready to start",
    running: "Running agents",
    waiting: "Waiting for approval",
    approved: "Report writing complete",
  };

  return (
    <div className="inline-flex w-fit items-center gap-2 rounded-md border bg-[#f7fbfa] px-3 py-2 text-sm font-semibold">
      <span
        className={cn(
          "h-2.5 w-2.5 rounded-full",
          status === "idle" && "bg-muted-foreground",
          status === "running" && "bg-secondary",
          status === "waiting" && "bg-accent",
          status === "approved" && "bg-primary"
        )}
      />
      {labelByStatus[status]}
    </div>
  );
}

function ApprovalPanel({
  status,
  query,
  audience,
  depth,
  onApprove,
}: Readonly<{
  status: RunStatus;
  query: string;
  audience: string;
  depth: string;
  onApprove: () => void;
}>) {
  const isWaiting = status === "waiting";
  const isApproved = status === "approved";

  return (
    <div className="rounded-md border bg-[#14211f] p-6 text-white shadow-soft">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase text-[#64d6c4]">Approval checkpoint</p>
          <h2 className="mt-2 text-2xl font-bold">Review before final report</h2>
          <p className="mt-3 text-sm leading-6 text-white/72">
            Confirm the draft direction before the final report is prepared.
          </p>
        </div>
        <ClipboardCheck className="h-6 w-6 text-[#f9b24a]" aria-hidden="true" />
      </div>

      <div className="mt-6 grid gap-3">
        <ApprovalFact label="Research question" value={query || "No question entered"} />
        <ApprovalFact label="Audience" value={audience || "General business reader"} />
        <ApprovalFact label="Output depth" value={depth} />
      </div>

      <div className="mt-6 rounded-md border border-white/10 bg-white/8 p-4">
        <div className="flex items-center gap-2 text-sm font-semibold">
          {isApproved ? (
            <CheckCircle2 className="h-4 w-4 text-[#64d6c4]" aria-hidden="true" />
          ) : (
            <Clock3 className="h-4 w-4 text-[#f9b24a]" aria-hidden="true" />
          )}
          {isWaiting ? "Draft payload is waiting for reviewer approval" : "Approval request will be created after critique"}
        </div>
        <p className="mt-2 text-sm leading-6 text-white/68">
          {isApproved
            ? "The draft was approved and the final report outline is ready."
            : "Approve the draft, request changes, or stop the run if the findings need more work."}
        </p>
      </div>

      <div className="mt-6 grid gap-2 sm:grid-cols-3">
        <Button type="button" onClick={onApprove} disabled={!isWaiting} className="bg-[#64d6c4] text-[#14211f] hover:bg-[#64d6c4]/90">
          Approve
        </Button>
        <Button type="button" variant="outline" disabled={!isWaiting} className="border-white/20 bg-transparent text-white hover:bg-white/10">
          Request revision
        </Button>
        <Button type="button" variant="outline" disabled={!isWaiting} className="border-white/20 bg-transparent text-white hover:bg-white/10">
          Reject
        </Button>
      </div>
    </div>
  );
}

function ApprovalFact({ label, value }: Readonly<{ label: string; value: string }>) {
  return (
    <div className="rounded-md border border-white/10 bg-white/8 p-3">
      <p className="text-xs font-semibold uppercase text-white/48">{label}</p>
      <p className="mt-1 text-sm font-semibold leading-5 text-white">{value}</p>
    </div>
  );
}

function WorkflowStepCard({
  step,
  state,
}: Readonly<{
  step: (typeof workflowSteps)[number];
  state: "idle" | "active" | "completed";
}>) {
  const Icon = step.icon;

  return (
    <div
      className={cn(
        "grid grid-cols-[2.5rem_1fr_auto] items-center gap-3 rounded-md border bg-[#f7fbfa] p-3 transition-colors",
        state === "active" && "border-accent bg-white",
        state === "completed" && "border-primary/40 bg-white"
      )}
    >
      <div
        className={cn(
          "flex h-10 w-10 items-center justify-center rounded-md border bg-white",
          state === "active" && "border-accent text-accent",
          state === "completed" && "border-primary text-primary"
        )}
      >
        <Icon className="h-4 w-4" aria-hidden="true" />
      </div>
      <div>
        <p className="text-sm font-bold">{step.label}</p>
        <p className="mt-1 text-xs leading-5 text-muted-foreground">{step.description}</p>
      </div>
      <StepBadge state={state} />
    </div>
  );
}

function StepBadge({ state }: Readonly<{ state: "idle" | "active" | "completed" }>) {
  if (state === "completed") {
    return <CheckCircle2 className="h-5 w-5 text-primary" aria-label="Completed" />;
  }

  if (state === "active") {
    return <Clock3 className="h-5 w-5 text-accent" aria-label="Active" />;
  }

  return <span className="h-2.5 w-2.5 rounded-full bg-muted" aria-label="Not started" />;
}

function DraftPreview({
  query,
  audience,
  depth,
  status,
}: Readonly<{
  query: string;
  audience: string;
  depth: string;
  status: RunStatus;
}>) {
  return (
    <div className="rounded-md border bg-white p-6 shadow-soft">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase text-primary">Draft preview</p>
          <h2 className="mt-1 text-xl font-bold">Research report outline</h2>
        </div>
        <div className="rounded-md border bg-[#f7fbfa] px-3 py-2 text-sm font-semibold">
          {status === "approved" ? "Final draft" : "Preview"}
        </div>
      </div>

      <div className="mt-5 rounded-md border bg-[#f7fbfa] p-4">
        <p className="text-xs font-semibold uppercase text-muted-foreground">Working title</p>
        <h3 className="mt-2 text-lg font-bold leading-7">{query || "Untitled research run"}</h3>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <MiniFact label="Audience" value={audience || "General business reader"} />
          <MiniFact label="Depth" value={depth} />
        </div>
      </div>

      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        {draftSections.map((section) => (
          <div key={section} className="rounded-md border p-4">
            <div className="flex items-center gap-2">
              <FileText className="h-4 w-4 text-primary" aria-hidden="true" />
              <p className="text-sm font-bold">{section}</p>
            </div>
            <p className="mt-2 text-xs leading-5 text-muted-foreground">
              {status === "idle"
                ? "Generated after the research agents run."
                : "Draft content prepared for reviewer validation."}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

function MiniFact({ label, value }: Readonly<{ label: string; value: string }>) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase text-muted-foreground">{label}</p>
      <p className="mt-1 text-sm font-semibold">{value}</p>
    </div>
  );
}

function getStepState(index: number, activeStepIndex: number, status: RunStatus): "idle" | "active" | "completed" {
  if (activeStepIndex < 0) {
    return "idle";
  }

  if (status === "approved") {
    return "completed";
  }

  if (index < activeStepIndex) {
    return "completed";
  }

  if (index === activeStepIndex) {
    return "active";
  }

  return "idle";
}
