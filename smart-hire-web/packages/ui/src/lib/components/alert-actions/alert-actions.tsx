import { AlertActionStyle, type AlertAction } from '@smart-hire/types';

import { Button } from '../button';

export interface AlertActionsProps {
  actions: AlertAction[];
  onDismiss: () => void;
}

/** Presents every supplied action; the platform adapter owns toast dismissal. */
export function AlertActions({ actions, onDismiss }: AlertActionsProps) {
  return (
    <div
      role="group"
      aria-label="Alert actions"
      className="flex flex-wrap gap-2"
    >
      {actions.map((action, index) => {
        const destructive = action.style === AlertActionStyle.Destructive;
        const cancel = action.style === AlertActionStyle.Cancel;
        const variant = destructive
          ? 'destructive'
          : cancel
            ? 'outline'
            : 'default';

        return (
          <Button
            key={index}
            type="button"
            data-action-style={action.style ?? AlertActionStyle.Default}
            size="sm"
            variant={variant}
            onClick={() => {
              action.onPress?.();
              onDismiss();
            }}
          >
            {action.label}
          </Button>
        );
      })}
    </div>
  );
}
