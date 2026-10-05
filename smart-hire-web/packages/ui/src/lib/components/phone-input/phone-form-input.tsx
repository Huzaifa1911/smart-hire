import { useId, type ComponentProps } from 'react';
import {
  useController,
  type FieldPath,
  type FieldValues,
  type UseControllerProps,
} from 'react-hook-form';

import { FieldShell } from '../form';
import { PhoneInput } from './phone-input';

export interface PhoneFormInputProps<TValues extends FieldValues = FieldValues>
  extends Omit<
    ComponentProps<typeof PhoneInput>,
    'value' | 'defaultValue' | 'onChange' | 'name' | 'ref'
  > {
  name: FieldPath<TValues>;
  label?: string;
  rules?: UseControllerProps<TValues>['rules'];
}

export function PhoneFormInput<TValues extends FieldValues = FieldValues>({
  name,
  label,
  rules,
  id: suppliedId,
  disabled,
  onBlur,
  'aria-describedby': describedBy,
  ...inputProps
}: PhoneFormInputProps<TValues>) {
  const { field, fieldState } = useController<TValues>({
    name,
    rules,
    disabled,
  });
  const generatedId = useId();
  const id = suppliedId ?? generatedId;
  const error = fieldState.error?.message;
  const messageId = `${id}-message`;
  const description =
    [describedBy, error ? messageId : undefined].filter(Boolean).join(' ') ||
    undefined;

  return (
    <FieldShell
      label={label}
      error={error}
      controlId={id}
      messageId={messageId}
    >
      <PhoneInput
        {...inputProps}
        {...field}
        id={id}
        value={field.value ?? ''}
        aria-invalid={!!error}
        aria-describedby={description}
        onBlur={(event) => {
          field.onBlur();
          onBlur?.(event);
        }}
      />
    </FieldShell>
  );
}

export default PhoneFormInput;
