import type { StorageService } from '@smart-hire/types';

import type { IamApiClient } from '../axios-client/clients/iamApi.client.js';

export interface AuthenticationHandlerDeps {
  iamApiClient: IamApiClient;
  storageService: StorageService;
}

/** Lifecycle extension point only; no storage reads or authentication requests. */
export class AuthenticationHandler {
  constructor(protected readonly deps: AuthenticationHandlerDeps) {}

  async init(): Promise<void> {
    /* Session restoration is not implemented. */
  }

  dispose(): void {
    /* No subscriptions exist yet. */
  }
}
