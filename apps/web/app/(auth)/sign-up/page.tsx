import type { Metadata } from "next";

import { AuthForm } from "@/features/auth/auth-form";

export const metadata: Metadata = {
  title: "Create account | research-agent-os",
  description: "Create your AI Research Analyst OS account."
};

export default function SignUpPage() {
  return <AuthForm mode="sign-up" />;
}

