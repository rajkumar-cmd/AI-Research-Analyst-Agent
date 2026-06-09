"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowRight, CheckCircle2, Loader2, Mail, UserRound } from "lucide-react";
import { useForm } from "react-hook-form";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { signIn, signUp } from "./auth-api";
import {
  signInSchema,
  signUpSchema,
  type SignInInput,
  type SignUpInput
} from "./auth-schemas";

type AuthFormProps = {
  mode: "sign-in" | "sign-up";
};

type FormValues = SignInInput | SignUpInput;

const authCopy = {
  "sign-in": {
    eyebrow: "Welcome back",
    title: "Sign in to your research workspace",
    description: "Continue your reports, review saved research, and track usage from one place.",
    button: "Sign in",
    loading: "Signing you in...",
    switchPrompt: "New to Research Agent OS?",
    switchLabel: "Create an account",
    switchHref: "/sign-up",
    successTitle: "Sign-in form is ready"
  },
  "sign-up": {
    eyebrow: "Start your workspace",
    title: "Create your account",
    description: "Set up your research workspace and prepare for your first AI-generated report.",
    button: "Create account",
    loading: "Creating your account...",
    switchPrompt: "Already have an account?",
    switchLabel: "Sign in",
    switchHref: "/sign-in",
    successTitle: "Account form is ready"
  }
};

export function AuthForm({ mode }: AuthFormProps) {
  const copy = authCopy[mode];
  const [submitMessage, setSubmitMessage] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const schema = mode === "sign-up" ? signUpSchema : signInSchema;

  const defaultValues = useMemo(
    () =>
      mode === "sign-up"
        ? { name: "", email: "", password: "" }
        : { email: "", password: "" },
    [mode]
  );

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues
  });

  async function onSubmit(values: FormValues) {
    setSubmitMessage(null);
    setSubmitError(null);

    try {
      const result =
        mode === "sign-up"
          ? await signUp(values as SignUpInput)
          : await signIn(values as SignInInput);
      setSubmitMessage(`${copy.successTitle}. ${result.message}`);
    } catch {
      setSubmitError("Something went wrong. Please try again in a moment.");
    }
  }

  return (
    <div className="rounded-md border bg-white p-6 shadow-soft sm:p-8">
      <Link href="/" className="mb-8 inline-flex items-center gap-2 text-sm font-semibold text-primary">
        <ArrowRight className="h-4 w-4 rotate-180" aria-hidden="true" />
        Back to home
      </Link>

      <div>
        <p className="text-sm font-semibold uppercase text-primary">{copy.eyebrow}</p>
        <h1 className="mt-3 text-3xl font-bold tracking-tight">{copy.title}</h1>
        <p className="mt-3 text-sm leading-6 text-muted-foreground">{copy.description}</p>
      </div>

      <form className="mt-8 space-y-5" onSubmit={handleSubmit(onSubmit)} noValidate>
        {mode === "sign-up" ? (
          <div className="space-y-2">
            <Label htmlFor="name">Full name</Label>
            <div className="relative">
              <UserRound className="pointer-events-none absolute left-3 top-3 h-5 w-5 text-muted-foreground" aria-hidden="true" />
              <Input
                id="name"
                autoComplete="name"
                placeholder="Rajkumar Pradhan"
                className="pl-10"
                aria-invalid={Boolean("name" in errors && errors.name)}
                {...register("name")}
              />
            </div>
            {"name" in errors && errors.name ? (
              <p className="text-sm font-medium text-destructive">{errors.name.message}</p>
            ) : null}
          </div>
        ) : null}

        <div className="space-y-2">
          <Label htmlFor="email">Email address</Label>
          <div className="relative">
            <Mail className="pointer-events-none absolute left-3 top-3 h-5 w-5 text-muted-foreground" aria-hidden="true" />
            <Input
              id="email"
              type="email"
              autoComplete="email"
              placeholder="you@example.com"
              className="pl-10"
              aria-invalid={Boolean(errors.email)}
              {...register("email")}
            />
          </div>
          {errors.email ? <p className="text-sm font-medium text-destructive">{errors.email.message}</p> : null}
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between gap-3">
            <Label htmlFor="password">Password</Label>
            {mode === "sign-in" ? (
              <Link href="/forgot-password" className="text-sm font-semibold text-primary hover:underline">
                Forgot password?
              </Link>
            ) : null}
          </div>
          <Input
            id="password"
            type="password"
            autoComplete={mode === "sign-up" ? "new-password" : "current-password"}
            placeholder={mode === "sign-up" ? "Create a strong password" : "Enter your password"}
            aria-invalid={Boolean(errors.password)}
            {...register("password")}
          />
          {errors.password ? <p className="text-sm font-medium text-destructive">{errors.password.message}</p> : null}
        </div>

        {submitError ? (
          <div className="rounded-md border border-destructive/25 bg-destructive/10 p-4 text-sm font-medium text-destructive">
            {submitError}
          </div>
        ) : null}

        {submitMessage ? (
          <div className="flex items-start gap-3 rounded-md border border-[#64d6c4]/35 bg-[#ecfbf8] p-4 text-sm text-primary">
            <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0" aria-hidden="true" />
            <span>{submitMessage}</span>
          </div>
        ) : null}

        <Button className="w-full" size="lg" type="submit" disabled={isSubmitting}>
          {isSubmitting ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
              {copy.loading}
            </>
          ) : (
            <>
              {copy.button}
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </>
          )}
        </Button>
      </form>

      <p className="mt-7 text-center text-sm text-muted-foreground">
        {copy.switchPrompt}{" "}
        <Link href={copy.switchHref} className="font-semibold text-primary hover:underline">
          {copy.switchLabel}
        </Link>
      </p>
    </div>
  );
}

