import { createElement } from 'react';
import { toast } from 'sonner';

import {
  AlertVariant,
  type AlertService,
  type AlertRequest,
  type AlertId,
} from '@smart-hire/types';
import { AlertActions } from '@smart-hire/ui';

/** Toast alerts and browser confirmation dialogs. */
export class WebAlertService implements AlertService {
  show(request: AlertRequest): AlertId {
    const id = crypto.randomUUID();

    toast[request.variant ?? AlertVariant.Info](
      request.title ?? request.message,
      {
        id,
        description: request.title ? request.message : undefined,
        duration: request.duration,
        action: request.actions?.length
          ? createElement(AlertActions, {
              actions: request.actions,
              onDismiss: () => toast.dismiss(id),
            })
          : undefined,
      },
    );

    return id;
  }

  hide(id?: AlertId): void {
    toast.dismiss(id);
  }

  confirm(
    request: Omit<AlertRequest, 'actions' | 'duration'>,
  ): Promise<boolean> {
    const message = request.title
      ? `${request.title}\n\n${request.message}`
      : request.message;

    return Promise.resolve(window.confirm(message));
  }
}
