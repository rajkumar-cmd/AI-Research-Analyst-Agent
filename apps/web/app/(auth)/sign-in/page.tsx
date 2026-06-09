import type { Metadata } from "next";

import { AuthForm } from "@/features/auth/auth-form";

export const metadata: Metadata = {
  title: "Sign in | research-agent-os",
  description: "Sign in to continue your AI research reports."
};

export default function SignInPage() {
  return <AuthForm mode="sign-in" />;
}

