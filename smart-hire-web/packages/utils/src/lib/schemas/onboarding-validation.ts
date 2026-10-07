export function validateRequiredText(value: unknown): true | string {
  return (
    (typeof value === 'string' && value.trim().length > 0) || 'Enter a value.'
  );
}

export function validateEmail(value: unknown): true | string {
  return (
    (typeof value === 'string' &&
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim())) ||
    'Enter a valid email address.'
  );
}

export function validateExperience(value: unknown): true | string {
  return (
    ((typeof value === 'string' || typeof value === 'number') &&
      String(value).trim() !== '' &&
      Number.isFinite(Number(value)) &&
      Number(value) >= 0) ||
    'Enter zero or more years of experience.'
  );
}
