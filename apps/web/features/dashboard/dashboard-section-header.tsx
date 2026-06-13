import Link from "next/link";
import { ArrowRight } from "lucide-react";

type DashboardSectionHeaderProps = {
  title: string;
  description: string;
  actionLabel?: string;
  actionHref?: string;
};

export function DashboardSectionHeader({
  title,
  description,
  actionLabel,
  actionHref
}: DashboardSectionHeaderProps) {
  return (
    <div className="flex flex-col gap-3 border-b pb-4 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <h2 className="text-xl font-bold">{title}</h2>
        <p className="mt-1 text-sm leading-6 text-muted-foreground">{description}</p>
      </div>
      {actionLabel && actionHref ? (
        <Link href={actionHref} className="inline-flex items-center gap-2 text-sm font-semibold text-primary">
          {actionLabel}
          <ArrowRight className="h-4 w-4" aria-hidden="true" />
        </Link>
      ) : null}
    </div>
  );
}

