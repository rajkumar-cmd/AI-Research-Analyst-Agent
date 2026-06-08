import Link from "next/link";
import {
  ArrowRight,
  BarChart3,
  CheckCircle2,
  Database,
  FileText,
  GitBranch,
  Layers3,
  LockKeyhole,
  Network,
  SearchCheck,
  ShieldCheck,
  Sparkles,
  TimerReset,
  Workflow,
  Zap
} from "lucide-react";

import { Button } from "@/components/ui/button";

const workflowSteps = [
  "Quota Guard",
  "Planner",
  "Research",
  "Hybrid Retrieval",
  "Source Validation",
  "Summarizer",
  "Critic",
  "Human Approval",
  "Report Writer"
];

const platformPillars = [
  {
    icon: Workflow,
    title: "Stateful agent orchestration",
    text: "LangGraph coordinates quota checks, planning, retrieval, validation, critique, approval, and report writing as observable steps."
  },
  {
    icon: SearchCheck,
    title: "Citation-ready retrieval",
    text: "Hybrid search combines dense retrieval, keyword filters, metadata scoring, rank fusion, and source validation before report generation."
  },
  {
    icon: ShieldCheck,
    title: "Governed research output",
    text: "Human approval, role controls, usage quotas, token accounting, and admin analytics make the system reviewable and accountable."
  }
];

const retrievalFeatures = [
  "Dense vector search",
  "Keyword filtering",
  "Metadata filters",
  "Reciprocal rank fusion",
  "Source freshness checks",
  "Citation coverage scoring"
];

const techStack = [
  "Next.js",
  "TypeScript",
  "Tailwind CSS",
  "shadcn/ui",
  "FastAPI",
  "LangGraph",
  "PostgreSQL",
  "Redis",
  "ChromaDB",
  "Pytest",
  "Docker"
];

const reportSections = [
  "Executive summary",
  "Key trends",
  "Competitor examples",
  "Risks",
  "Recommendations",
  "Citations",
  "Quality score",
  "Token usage"
];

const adminMetrics = [
  { label: "Reports", value: "128", icon: BarChart3 },
  { label: "Tokens", value: "2.4M", icon: Database },
  { label: "Avg latency", value: "41s", icon: TimerReset }
];

export default function LandingPage() {
  return (
    <main className="overflow-hidden">
      <header className="fixed left-0 right-0 top-0 z-50 border-b border-white/10 bg-[#14211f]/90 text-white backdrop-blur">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link href="/" className="flex items-center gap-2 text-sm font-bold">
            <span className="flex h-8 w-8 items-center justify-center rounded-md bg-[#f9b24a] text-[#14211f]">
              <Sparkles className="h-4 w-4" aria-hidden="true" />
            </span>
            research-agent-os
          </Link>
          <nav className="hidden items-center gap-7 text-sm text-white/75 md:flex">
            <Link href="#workflow" className="hover:text-white">
              Workflow
            </Link>
            <Link href="#retrieval" className="hover:text-white">
              Retrieval
            </Link>
            <Link href="#analytics" className="hover:text-white">
              Analytics
            </Link>
            <Link href="#report" className="hover:text-white">
              Report
            </Link>
          </nav>
          <Button asChild size="sm" variant="secondary">
            <Link href="/sign-up">
              <Zap className="h-4 w-4" aria-hidden="true" />
              Start demo
            </Link>
          </Button>
        </div>
      </header>

      <section className="workflow-scene relative min-h-[760px] text-white">
        <div className="absolute inset-0 opacity-90">
          <div className="scene-line left-[57%] top-[27%] w-[190px] rotate-[18deg]" />
          <div className="scene-line left-[64%] top-[43%] w-[170px] rotate-[-20deg]" />
          <div className="scene-line left-[54%] top-[59%] w-[240px] rotate-[9deg]" />
          <div className="scene-line left-[74%] top-[34%] w-[120px] rotate-[87deg]" />
          <div className="absolute left-[58%] top-[22%] hidden h-20 w-52 rounded-md border border-[#64d6c4]/40 bg-[#1d3834]/80 p-4 shadow-soft lg:block">
            <p className="text-xs uppercase text-[#64d6c4]">Planner Agent</p>
            <p className="mt-2 text-sm text-white/80">Breaks broad questions into verifiable research tasks.</p>
          </div>
          <div className="absolute left-[74%] top-[38%] hidden h-24 w-56 rounded-md border border-[#f98f6f]/45 bg-[#2b302b]/85 p-4 shadow-soft lg:block">
            <p className="text-xs uppercase text-[#f98f6f]">Validation Gate</p>
            <p className="mt-2 text-sm text-white/80">Scores credibility, freshness, and citation coverage.</p>
          </div>
          <div className="absolute left-[60%] top-[61%] hidden h-24 w-64 rounded-md border border-[#f9b24a]/45 bg-[#323023]/85 p-4 shadow-soft lg:block">
            <p className="text-xs uppercase text-[#f9b24a]">Human Approval</p>
            <p className="mt-2 text-sm text-white/80">Pauses before final report generation for review.</p>
          </div>
          <div className="workflow-dot absolute left-[83%] top-[21%] h-5 w-5 rounded-full bg-[#64d6c4]" />
          <div className="workflow-dot absolute left-[70%] top-[53%] h-4 w-4 rounded-full bg-[#f98f6f]" />
          <div className="workflow-dot absolute left-[86%] top-[66%] h-5 w-5 rounded-full bg-[#f9b24a]" />
        </div>

        <div className="relative mx-auto flex min-h-[760px] max-w-7xl flex-col justify-center px-4 pb-16 pt-28 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-md border border-white/20 bg-white/10 px-3 py-2 text-sm text-white/80">
              <GitBranch className="h-4 w-4 text-[#64d6c4]" aria-hidden="true" />
              LangGraph-native research workflow
            </div>
            <h1 className="mt-7 max-w-4xl text-5xl font-bold leading-tight sm:text-6xl lg:text-7xl">
              AI Research Analyst OS for Reliable Multi-Step Research Workflows
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-white/75">
              Generate validated research reports using LangGraph, hybrid search, source validation, human approval,
              and token-level observability.
            </p>
            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Button asChild size="lg" variant="secondary">
                <Link href="/dashboard/new-research">
                  <Sparkles className="h-4 w-4" aria-hidden="true" />
                  Generate report
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-white/25 bg-white/10 text-white hover:bg-white/20">
                <Link href="#workflow">
                  View workflow
                  <ArrowRight className="h-4 w-4" aria-hidden="true" />
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-white py-20 sm:py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-5 md:grid-cols-3">
            {platformPillars.map((pillar) => {
              const Icon = pillar.icon;
              return (
                <article key={pillar.title} className="rounded-md border bg-white p-6 shadow-soft">
                  <Icon className="h-6 w-6 text-primary" aria-hidden="true" />
                  <h2 className="mt-5 text-xl font-semibold">{pillar.title}</h2>
                  <p className="mt-3 text-sm leading-6 text-muted-foreground">{pillar.text}</p>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section id="workflow" className="bg-[#edf4f3] py-20 sm:py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-end">
            <div>
              <p className="text-sm font-semibold uppercase text-primary">Workflow visualization</p>
              <h2 className="mt-3 max-w-3xl text-3xl font-bold sm:text-4xl">A research pipeline you can inspect step by step</h2>
            </div>
            <p className="max-w-xl text-sm leading-6 text-muted-foreground">
              Each node becomes a traceable unit with status, latency, token usage, and output payloads for later
              debugging and admin review.
            </p>
          </div>

          <div className="mt-10 grid gap-3 lg:grid-cols-9">
            {workflowSteps.map((step, index) => (
              <div key={step} className="relative rounded-md border bg-white p-4 shadow-soft">
                <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary text-sm font-bold text-white">
                  {index + 1}
                </div>
                <p className="mt-4 min-h-12 text-sm font-semibold leading-5">{step}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="retrieval" className="bg-white py-20 sm:py-24">
        <div className="mx-auto grid max-w-7xl gap-10 px-4 sm:px-6 lg:grid-cols-[0.9fr_1.1fr] lg:px-8">
          <div>
            <p className="text-sm font-semibold uppercase text-primary">Hybrid retrieval</p>
            <h2 className="mt-3 text-3xl font-bold sm:text-4xl">Source discovery built for citation quality</h2>
            <p className="mt-5 text-sm leading-6 text-muted-foreground">
              The retrieval layer is planned around ChromaDB collections, provider abstractions, citation-ready result
              objects, and validation metadata that survives into the final report.
            </p>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {retrievalFeatures.map((feature) => (
              <div key={feature} className="flex items-center gap-3 rounded-md border bg-[#fbfcfd] p-4">
                <CheckCircle2 className="h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
                <span className="text-sm font-medium">{feature}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="analytics" className="bg-[#17241f] py-20 text-white sm:py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-10 lg:grid-cols-[0.85fr_1.15fr] lg:items-center">
            <div>
              <p className="text-sm font-semibold uppercase text-[#64d6c4]">Admin analytics preview</p>
              <h2 className="mt-3 text-3xl font-bold sm:text-4xl">Operational visibility for every run</h2>
              <p className="mt-5 text-sm leading-6 text-white/72">
                Admin views will surface user quotas, failed runs, model spend, step-level token usage, and report
                throughput so the agent behaves like a governed product.
              </p>
            </div>
            <div className="grid gap-4 sm:grid-cols-3">
              {adminMetrics.map(({ label, value, icon: Icon }) => (
                <div key={label} className="rounded-md border border-white/10 bg-white/10 p-5">
                  <Icon className="h-5 w-5 text-[#f9b24a]" aria-hidden="true" />
                  <p className="mt-5 text-3xl font-bold">{value}</p>
                  <p className="mt-1 text-sm text-white/70">{label}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section id="report" className="bg-[#f7f9fb] py-20 sm:py-24">
        <div className="mx-auto grid max-w-7xl gap-10 px-4 sm:px-6 lg:grid-cols-[1fr_1fr] lg:px-8">
          <div>
            <p className="text-sm font-semibold uppercase text-primary">Report preview</p>
            <h2 className="mt-3 text-3xl font-bold sm:text-4xl">Structured output that feels boardroom-ready</h2>
            <p className="mt-5 text-sm leading-6 text-muted-foreground">
              The final research artifact will combine executive clarity with traceable evidence, source scoring, model
              metadata, and a timeline of agent decisions.
            </p>
            <div className="mt-7 flex flex-wrap gap-2">
              {techStack.map((tech) => (
                <span key={tech} className="rounded-md border bg-white px-3 py-2 text-xs font-semibold text-[#25322f]">
                  {tech}
                </span>
              ))}
            </div>
          </div>

          <article className="rounded-md border bg-white p-6 shadow-soft">
            <div className="flex items-start justify-between gap-4 border-b pb-5">
              <div>
                <p className="text-xs font-semibold uppercase text-primary">Sample report</p>
                <h3 className="mt-2 text-xl font-bold">AI data engineering trends for 2026</h3>
              </div>
              <FileText className="h-6 w-6 text-accent" aria-hidden="true" />
            </div>
            <div className="mt-5 grid gap-3 sm:grid-cols-2">
              {reportSections.map((section) => (
                <div key={section} className="rounded-md bg-[#f1f5f6] px-4 py-3 text-sm font-medium">
                  {section}
                </div>
              ))}
            </div>
            <div className="mt-6 rounded-md border border-[#64d6c4]/35 bg-[#ecfbf8] p-4">
              <div className="flex items-center gap-2 text-sm font-semibold text-primary">
                <LockKeyhole className="h-4 w-4" aria-hidden="true" />
                Human approval required before final generation
              </div>
            </div>
          </article>
        </div>
      </section>

      <section className="bg-white py-16">
        <div className="mx-auto flex max-w-7xl flex-col gap-6 px-4 sm:px-6 md:flex-row md:items-center md:justify-between lg:px-8">
          <div>
            <p className="text-sm font-semibold uppercase text-primary">Built for interviews and GitHub progress</p>
            <h2 className="mt-2 text-3xl font-bold">Day 2 turns the scaffold into a visible product surface.</h2>
          </div>
          <Button asChild size="lg">
            <Link href="/sign-up">
              Continue to auth
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </Button>
        </div>
      </section>

      <footer className="border-t bg-[#14211f] py-8 text-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 text-sm text-white/70 sm:px-6 md:flex-row md:items-center md:justify-between lg:px-8">
          <p>research-agent-os</p>
          <div className="flex items-center gap-3">
            <Network className="h-4 w-4" aria-hidden="true" />
            <Layers3 className="h-4 w-4" aria-hidden="true" />
            <Database className="h-4 w-4" aria-hidden="true" />
          </div>
        </div>
      </footer>
    </main>
  );
}
