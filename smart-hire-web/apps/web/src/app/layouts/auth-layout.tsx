import { useEffect, useRef, type ReactNode } from 'react';

import { useAppCoreContext } from '@smart-hire/core';
import { Button } from '@smart-hire/ui';

interface AuthLayoutProps {
  title: string;
  description: string;
  eyebrow: string;
  children: ReactNode;
  footer?: ReactNode;
  back?: () => void;
}

export function AuthLayout({
  title,
  description,
  eyebrow,
  children,
  footer,
  back,
}: AuthLayoutProps) {
  const { platformName } = useAppCoreContext();
  const headingRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    headingRef.current?.focus();
  }, [title]);

  return (
    <div className="min-h-svh bg-muted/40 text-foreground">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:z-10 focus:rounded-md focus:bg-background focus:p-3"
      >
        Skip to content
      </a>
      <header className="border-b bg-background">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-6 py-5">
          <span className="text-xl font-semibold tracking-tight">
            {platformName}
            <span className="text-primary">.</span>
          </span>
          <span className="text-sm text-muted-foreground">
            Account &amp; workspace
          </span>
        </div>
      </header>
      <div className="mx-auto grid max-w-5xl items-start gap-10 px-5 py-10 md:grid-cols-[minmax(0,1fr)_minmax(0,1.4fr)] md:gap-16 md:py-16">
        <aside className="md:sticky md:top-12">
          <p className="text-xs font-medium uppercase tracking-widest text-muted-foreground">
            Your next chapter
          </p>
          <h2 className="mt-4 max-w-sm text-3xl font-semibold leading-tight tracking-tight md:text-4xl">
            One account.
            <br />
            More possibilities.
          </h2>
          <p className="mt-5 max-w-sm text-sm leading-7 text-muted-foreground">
            Find your next role or build the team that moves your organization
            forward.
          </p>
          <div className="mt-8 hidden space-y-5 border-t pt-6 text-sm md:block">
            <p>
              01{' '}
              <span className="ml-3 text-muted-foreground">
                Create your account
              </span>
            </p>
            <p>
              02{' '}
              <span className="ml-3 text-muted-foreground">
                Set up your profile or workspace
              </span>
            </p>
            <p>
              03{' '}
              <span className="ml-3 text-muted-foreground">
                Make your next move
              </span>
            </p>
          </div>
        </aside>
        <main
          id="main-content"
          className="min-w-0 rounded-xl border bg-card text-card-foreground shadow-sm"
        >
          <div className="p-6 sm:p-8">
            {back && (
              <Button
                variant="ghost"
                size="sm"
                className="-ml-3 mb-5"
                onClick={back}
              >
                ← Back
              </Button>
            )}
            <p className="text-xs font-medium uppercase tracking-widest text-muted-foreground">
              {eyebrow}
            </p>
            <h1
              ref={headingRef}
              tabIndex={-1}
              className="mt-3 text-2xl font-semibold leading-tight tracking-tight outline-none"
            >
              {title}
            </h1>
            <p className="mb-7 mt-3 text-sm leading-6 text-muted-foreground">
              {description}
            </p>
            {children}
            {footer && (
              <div className="mt-6 border-t pt-5 text-center text-sm text-muted-foreground">
                {footer}
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
