import Link from "next/link";
import { Bell, FileText, Home, SearchCheck, Sparkles, UserRound, WalletCards } from "lucide-react";

import { ProtectedDashboard } from "./protected-dashboard";

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: Home },
  { label: "New research", href: "/dashboard/new-research", icon: SearchCheck },
  { label: "Reports", href: "/dashboard/reports", icon: FileText },
  { label: "Usage", href: "/dashboard/usage", icon: WalletCards }
];

export function DashboardShell({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <ProtectedDashboard>
      <div className="min-h-screen bg-[#eef5f3] text-foreground">
        <aside className="fixed inset-y-0 left-0 z-40 hidden w-72 border-r bg-[#14211f] text-white lg:block">
          <div className="flex h-full flex-col">
            <Link href="/" className="flex h-16 items-center gap-2 border-b border-white/10 px-5 text-sm font-bold">
              <span className="flex h-8 w-8 items-center justify-center rounded-md bg-[#f9b24a] text-[#14211f]">
                <Sparkles className="h-4 w-4" aria-hidden="true" />
              </span>
              Research Agent OS
            </Link>

            <nav className="flex-1 space-y-1 px-3 py-5">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className="flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-semibold text-white/72 transition-colors hover:bg-white/10 hover:text-white"
                  >
                    <Icon className="h-4 w-4" aria-hidden="true" />
                    {item.label}
                  </Link>
                );
              })}
            </nav>

            <div className="m-3 rounded-md border border-white/10 bg-white/8 p-4">
              <p className="text-xs font-semibold uppercase text-[#64d6c4]">Demo workspace</p>
              <p className="mt-2 text-sm leading-6 text-white/74">Frontend shell now. Live user data connects after API wiring.</p>
            </div>
          </div>
        </aside>

        <div className="lg:pl-72">
          <header className="sticky top-0 z-30 border-b bg-white/90 backdrop-blur">
            <div className="flex h-16 items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
              <div className="flex items-center gap-3">
                <Link href="/dashboard" className="flex items-center gap-2 text-sm font-bold lg:hidden">
                  <span className="flex h-9 w-9 items-center justify-center rounded-md bg-primary text-white">
                    <Sparkles className="h-4 w-4" aria-hidden="true" />
                  </span>
                  <span className="hidden sm:inline">Research Agent OS</span>
                </Link>
                <div>
                  <p className="text-xs font-semibold uppercase text-primary">Workspace</p>
                  <p className="text-sm font-semibold">Research dashboard</p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <button className="inline-flex h-10 w-10 items-center justify-center rounded-md border bg-white" type="button">
                  <Bell className="h-4 w-4" aria-hidden="true" />
                  <span className="sr-only">Notifications</span>
                </button>
                <div className="hidden items-center gap-3 rounded-md border bg-white px-3 py-2 sm:flex">
                  <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary text-white">
                    <UserRound className="h-4 w-4" aria-hidden="true" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold leading-none">Rajkumar</p>
                    <p className="mt-1 text-xs text-muted-foreground">Research lead</p>
                  </div>
                </div>
              </div>
            </div>
          </header>

          <nav className="flex gap-2 overflow-x-auto border-b bg-white px-4 py-3 sm:px-6 lg:hidden">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className="inline-flex shrink-0 items-center gap-2 rounded-md border bg-white px-3 py-2 text-sm font-semibold"
                >
                  <Icon className="h-4 w-4 text-primary" aria-hidden="true" />
                  {item.label}
                </Link>
              );
            })}
          </nav>

          <main className="px-4 py-6 sm:px-6 lg:px-8">{children}</main>
        </div>
      </div>
    </ProtectedDashboard>
  );
}
