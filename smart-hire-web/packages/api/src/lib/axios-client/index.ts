import { IamApiClient } from './clients/iamApi.client.js';

export interface BaseURL {
  iamApiBaseUrl?: string;
}

export interface APIClientOptions {
  contextHeaders?: Record<string, unknown> | null;
  tenantId?: string | null;
  useCredentials?: boolean;
}

/** App-facing facade with lazy, cached service clients. */
export class APIClient {
  private readonly clients: { iamApiClient?: IamApiClient } = {};

  constructor(
    private readonly baseUrl: BaseURL,
    private readonly options: APIClientOptions = {},
  ) {}

  get iamApiClient(): IamApiClient {
    const url = this.baseUrl.iamApiBaseUrl;

    if (!url) throw new Error('IAM API base URL is not configured');

    return (this.clients.iamApiClient ??= new IamApiClient(url, {
      ...this.options,
      contentType: 'application/json',
    }));
  }
}
