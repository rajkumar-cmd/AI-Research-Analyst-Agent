import Link from "next/link";
import { CheckCircle2, ShieldCheck, Sparkles } from "lucide-react";

const trustPoints = [
  "Demo-friendly mock mode before API keys are required",
  "Reviewable research steps for every generated report",
  "Built for source quality, usage visibility, and team controls"
];

export default function AuthLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <main className="min-h-screen bg-[#eef5f3]">
      <div className="grid min-h-screen lg:grid-cols-[0.92fr_1.08fr]">
        <section className="workflow-scene relative hidden overflow-hidden px-10 py-8 text-white lg:flex lg:flex-col">
          <Link href="/" className="relative z-10 flex items-center gap-2 text-sm font-bold">
            <span className="flex h-8 w-8 items-center justify-center rounded-md bg-[#f9b24a] text-[#14211f]">
              <Sparkles className="h-4 w-4" aria-hidden="true" />
            </span>
            Research Agent OS
          </Link>

          <div className="relative z-10 my-auto max-w-xl">
            <p className="text-sm font-semibold uppercase text-[#64d6c4]">Reliable research starts here</p>
            <h1 className="mt-4 text-5xl font-bold leading-tight">
              Turn one research question into a checked, cited, approval-ready report.
            </h1>
            <p className="mt-5 text-base leading-7 text-white/72">
              Create an account to start building the research workflow: plan the question, gather evidence, review the
              draft, and track the quality of every final report.
            </p>
            <div className="mt-8 space-y-3">
              {trustPoints.map((point) => (
                <div key={point} className="flex items-start gap-3 rounded-md border border-white/12 bg-white/8 p-4">
                  <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-[#f9b24a]" aria-hidden="true" />
                  <span className="text-sm leading-6 text-white/82">{point}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="relative z-10 rounded-md border border-white/12 bg-white/8 p-4">
            <div className="flex items-center gap-2 text-sm font-semibold">
              <ShieldCheck className="h-4 w-4 text-[#64d6c4]" aria-hidden="true" />
              Human review and source validation are part of the workflow.
            </div>
          </div>
        </section>

        <section className="flex min-h-screen items-center justify-center px-4 py-10 sm:px-6 lg:px-8">
          <div className="w-full max-w-md">{children}</div>
        </section>
      </div>
    </main>
  );
}

