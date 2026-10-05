import { createStore } from 'zustand/vanilla';

import type { AccountInfo } from '@smart-hire/types';

/** Reactive identity placeholder. No tokens or session mutations are implemented. */
export const authStore = createStore<AccountInfo>(() => ({ user: null }));
