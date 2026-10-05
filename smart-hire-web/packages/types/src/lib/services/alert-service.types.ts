export enum AlertVariant {
  Info = 'info',
  Success = 'success',
  Warning = 'warning',
  Error = 'error',
}

export enum AlertActionStyle {
  Default = 'default',
  Cancel = 'cancel',
  Destructive = 'destructive',
}

export interface AlertAction {
  label: string;
  style?: AlertActionStyle;
  onPress?: () => void;
}

export interface AlertRequest {
  title?: string;
  message: string;
  variant?: AlertVariant;
  actions?: AlertAction[];
  duration?: number;
}

export type AlertId = string;

export interface AlertService {
  show(request: AlertRequest): AlertId;
  hide(id?: AlertId): void;
  confirm(
    request: Omit<AlertRequest, 'actions' | 'duration'>,
  ): Promise<boolean>;
}
