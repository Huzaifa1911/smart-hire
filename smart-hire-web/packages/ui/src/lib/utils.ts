import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/** Shared styling utility, colocated as in the reference UI package. */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
