import type { CSSProperties } from 'react';
import { useTheme } from 'next-themes';
import { Toaster as Sonner, type ToasterProps } from 'sonner';

import {
  CircleCheckIcon,
  InfoIcon,
  Loader2Icon,
  OctagonXIcon,
  TriangleAlertIcon,
} from '../icons';

export function Toaster({
  theme: suppliedTheme,
  style,
  ...props
}: ToasterProps) {
  const { theme = 'system' } = useTheme();

  return (
    <Sonner
      theme={
        suppliedTheme ??
        (theme === 'light' || theme === 'dark' ? theme : 'system')
      }
      icons={{
        success: <CircleCheckIcon className="size-4" />,
        info: <InfoIcon className="size-4" />,
        warning: <TriangleAlertIcon className="size-4" />,
        error: <OctagonXIcon className="size-4" />,
        loading: <Loader2Icon className="size-4 animate-spin" />,
      }}
      style={
        {
          '--normal-bg': 'var(--popover)',
          '--normal-text': 'var(--popover-foreground)',
          '--normal-border': 'var(--border)',
          '--border-radius': 'var(--radius)',
          ...style,
        } as CSSProperties
      }
      {...props}
    />
  );
}

export { ThemeProvider } from 'next-themes';
