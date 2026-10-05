import { AsYouType, isValidPhoneNumber } from 'libphonenumber-js';

/** International input normalization; callers must supply a country calling code. */
export function toE164(value: string): string {
  const digits = value.replace(/\D/g, '').replace(/^0+/, '').slice(0, 15);

  return digits ? `+${digits}` : '';
}

export function formatPhoneNumber(value: string): string {
  return new AsYouType().input(toE164(value));
}

/** Validation is separate: partial normalized input is not a valid phone number. */
export function isValidPhone(value: string): boolean {
  return isValidPhoneNumber(toE164(value));
}
