import type { LucideIcon } from "lucide-react";

type DashboardMetricCardProps = {
  label: string;
  value: string;
  helper: string;
  icon: LucideIcon;
};

export function DashboardMetricCard({ label, value, helper, icon: Icon }: DashboardMetricCardProps) {
  return (
    <div className="rounded-md border bg-[#f8fbfb] p-4">
      <div className="flex items-center justify-between gap-3">
        <p className="text-sm font-medium text-muted-foreground">{label}</p>
        <Icon className="h-4 w-4 text-primary" aria-hidden="true" />
      </div>
      <p className="mt-3 text-2xl font-bold">{value}</p>
      <p className="mt-1 text-xs font-medium text-muted-foreground">{helper}</p>
    </div>
  );
}

