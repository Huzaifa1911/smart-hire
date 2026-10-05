import type { ReactNode } from 'react';

import { cn } from '../../utils';
import { Label } from '../label';

export { FormProvider as Form } from 'react-hook-form';

export interface FieldShellProps {
  label?: ReactNode;
  error?: string;
  controlId: string;
  messageId: string;
  children: ReactNode;
  className?: string;
}

export function FieldShell({
  label,
  error,
  controlId,
  messageId,
  children,
  className,
}: FieldShellProps) {
  return (
    <div data-slot="form-item" className={cn('grid gap-2', className)}>
      {label && (
        <Label
          htmlFor={controlId}
          data-error={!!error}
          className="data-[error=true]:text-destructive"
        >
          {label}
        </Label>
      )}
      {children}
      {error && (
        <p id={messageId} role="alert" className="text-sm text-destructive">
          {error}
        </p>
      )}
    </div>
  );
}
