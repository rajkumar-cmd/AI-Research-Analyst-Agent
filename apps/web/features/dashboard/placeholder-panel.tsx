import Link from "next/link";
import type { LucideIcon } from "lucide-react";
import { ArrowRight } from "lucide-react";

import { Button } from "@/components/ui/button";

type PlaceholderPanelProps = {
  icon: LucideIcon;
  eyebrow: string;
  title: string;
  description: string;
  primaryActionLabel: string;
  primaryActionHref: string;
};

export function PlaceholderPanel({
  icon: Icon,
  eyebrow,
  title,
  description,
  primaryActionLabel,
  primaryActionHref
}: PlaceholderPanelProps) {
  return (
    <section className="rounded-md border bg-white p-8 shadow-soft">
      <div className="flex h-12 w-12 items-center justify-center rounded-md bg-[#ecfbf8] text-primary">
        <Icon className="h-6 w-6" aria-hidden="true" />
      </div>
      <p className="mt-6 text-sm font-semibold uppercase text-primary">{eyebrow}</p>
      <h1 className="mt-2 max-w-2xl text-3xl font-bold tracking-tight">{title}</h1>
      <p className="mt-4 max-w-2xl text-sm leading-6 text-muted-foreground">{description}</p>
      <Button asChild className="mt-7">
        <Link href={primaryActionHref}>
          {primaryActionLabel}
          <ArrowRight className="h-4 w-4" aria-hidden="true" />
        </Link>
      </Button>
    </section>
  );
}

