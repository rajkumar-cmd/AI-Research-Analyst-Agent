import { FileText } from "lucide-react";

type Report = {
  title: string;
  status: string;
  qualityScore: string;
  createdAt: string;
};

export function ReportList({ reports }: { reports: Report[] }) {
  return (
    <div className="mt-4 divide-y">
      {reports.map((report) => (
        <div key={report.title} className="flex flex-col gap-3 py-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-start gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-md bg-[#ecfbf8] text-primary">
              <FileText className="h-5 w-5" aria-hidden="true" />
            </div>
            <div>
              <h3 className="text-sm font-semibold">{report.title}</h3>
              <p className="mt-1 text-xs text-muted-foreground">{report.createdAt}</p>
            </div>
          </div>
          <div className="flex items-center gap-2 sm:justify-end">
            <span className="rounded-md bg-[#f1f5f6] px-2.5 py-1 text-xs font-semibold">{report.status}</span>
            <span className="rounded-md bg-[#ecfbf8] px-2.5 py-1 text-xs font-semibold text-primary">
              {report.qualityScore}/100
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

