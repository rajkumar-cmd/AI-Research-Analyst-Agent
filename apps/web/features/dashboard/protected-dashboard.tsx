"use client";

import Link from "next/link";
import { ShieldCheck } from "lucide-react";

export function ProtectedDashboard({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <>
      <div className="border-b border-[#64d6c4]/30 bg-[#ecfbf8] px-4 py-2 text-sm text-primary sm:px-6 lg:pl-[19rem] lg:pr-8">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-2 font-medium">
            <ShieldCheck className="h-4 w-4" aria-hidden="true" />
            Demo workspace is visible while real account checks are being connected.
          </div>
          <Link href="/sign-in" className="font-semibold hover:underline">
            Sign in
          </Link>
        </div>
      </div>
      {children}
    </>
  );
}

