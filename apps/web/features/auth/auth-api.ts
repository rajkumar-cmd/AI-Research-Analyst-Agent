import type { SignInInput, SignUpInput } from "./auth-schemas";

type AuthResult = {
  message: string;
  redirectTo: string;
};

const demoDelayMs = 650;

function wait(ms: number) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}

export async function signIn(input: SignInInput): Promise<AuthResult> {
  await wait(demoDelayMs);

  return {
    message: `Welcome back. ${input.email} is ready for the dashboard preview while API wiring is finalized.`,
    redirectTo: "/dashboard"
  };
}

export async function signUp(input: SignUpInput): Promise<AuthResult> {
  await wait(demoDelayMs);

  return {
    message: `${input.name}, your account form is ready. The real signup endpoint is available and will be connected to the UI next.`,
    redirectTo: "/dashboard"
  };
}
