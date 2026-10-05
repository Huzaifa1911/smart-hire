import { forwardRef, type ComponentProps } from 'react';

import { formatPhoneNumber, toE164 } from '@smart-hire/utils';

import { Input } from '../input/input';

export interface PhoneInputProps
  extends Omit<
    ComponentProps<typeof Input>,
    'value' | 'onChange' | 'type' | 'defaultValue'
  > {
  value?: string;
  onChange?: (value: string) => void;
}

export const PhoneInput = forwardRef<HTMLInputElement, PhoneInputProps>(
  ({ value = '', onChange, ...props }, ref) => (
    <Input
      {...props}
      ref={ref}
      type="tel"
      inputMode="tel"
      value={formatPhoneNumber(value)}
      onChange={(event) => onChange?.(toE164(event.target.value))}
    />
  ),
);

PhoneInput.displayName = 'PhoneInput';

export default PhoneInput;
