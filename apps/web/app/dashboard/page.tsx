import Link from "next/link";
import { ArrowRight, Clock3, FileText, PlayCircle, WalletCards } from "lucide-react";

import { Button } from "@/components/ui/button";
import { ActiveWorkflow } from "@/features/dashboard/active-workflow";
import { DashboardMetricCard } from "@/features/dashboard/dashboard-metric-card";
import { DashboardSectionHeader } from "@/features/dashboard/dashboard-section-header";
import { recentReports, recentRuns, usageMetrics } from "@/features/dashboard/mock-data";
import { ReportList } from "@/features/dashboard/report-list";
import { RunTimeline } from "@/features/dashboard/run-timeline";
import { UsageCard } from "@/features/dashboard/usage-card";

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <section className="grid gap-4 lg:grid-cols-[1.4fr_0.9fr]">
        <div className="rounded-md border bg-white p-6 shadow-soft">
          <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase text-primary">Today&apos;s workspace</p>
              <h1 className="mt-2 text-3xl font-bold tracking-tight">Good morning, Rajkumar.</h1>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
                Track report activity, usage, and research progress from one focused workspace.
              </p>
            </div>
            <Button asChild>
              <Link href="/dashboard/new-research">
                <PlayCircle className="h-4 w-4" aria-hidden="true" />
                Start research
              </Link>
            </Button>
          </div>

          <div className="mt-6 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
            <DashboardMetricCard label="Reports generated" value="12" helper="+3 this week" icon={FileText} />
            <DashboardMetricCard label="Daily quota left" value="7" helper="10 total requests" icon={Clock3} />
            <DashboardMetricCard label="Monthly quota left" value="84" helper="100 total requests" icon={WalletCards} />
            <DashboardMetricCard label="Tokens used" value="182k" helper="$4.18 estimated" icon={ArrowRight} />
          </div>
        </div>

        <ActiveWorkflow />
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        {usageMetrics.map((metric) => (
          <UsageCard key={metric.label} {...metric} />
        ))}
      </section>

      <section className="grid gap-6 xl:grid-cols-[1fr_0.95fr]">
        <div className="rounded-md border bg-white p-6 shadow-soft">
          <DashboardSectionHeader
            title="Recent reports"
            description="Reports will become live once research runs are connected to the backend workflow."
            actionLabel="View all"
            actionHref="/dashboard/reports"
          />
          <ReportList reports={recentReports} />
        </div>

        <div className="rounded-md border bg-white p-6 shadow-soft">
          <DashboardSectionHeader
            title="Recent research runs"
            description="A status timeline for planning, source review, approval, and report generation."
          />
          <RunTimeline runs={recentRuns} />
        </div>
      </section>
    </div>
  );
}
