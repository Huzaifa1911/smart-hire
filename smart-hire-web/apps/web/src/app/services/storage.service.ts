import type { StorageService } from '@smart-hire/types';

/** Browser storage adapter. Unavailable storage behaves like an empty store. */
export class WebStorageService implements StorageService {
  getItem(key: string): string | null {
    try {
      return window.localStorage.getItem(key);
    } catch {
      return null;
    }
  }

  setItem(key: string, value: string): void {
    try {
      window.localStorage.setItem(key, value);
    } catch {
      // Storage can be blocked or full. Persistence is best-effort.
    }
  }

  removeItem(key: string): void {
    try {
      window.localStorage.removeItem(key);
    } catch {
      // Storage can be blocked by browser policy.
    }
  }
}
