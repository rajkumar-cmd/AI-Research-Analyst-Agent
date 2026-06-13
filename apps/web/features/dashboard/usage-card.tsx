type UsageCardProps = {
  label: string;
  value: string;
  helper: string;
  percent: number;
};

export function UsageCard({ label, value, helper, percent }: UsageCardProps) {
  return (
    <div className="rounded-md border bg-white p-5 shadow-soft">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold">{label}</p>
          <p className="mt-2 text-2xl font-bold">{value}</p>
        </div>
        <span className="rounded-md bg-[#ecfbf8] px-2.5 py-1 text-xs font-semibold text-primary">{percent}%</span>
      </div>
      <div className="mt-4 h-2 rounded-full bg-[#e5eceb]">
        <div className="h-2 rounded-full bg-primary" style={{ width: `${percent}%` }} />
      </div>
      <p className="mt-3 text-xs font-medium text-muted-foreground">{helper}</p>
    </div>
  );
}

