import axios, { type AxiosInstance } from 'axios';

export interface RequestHandlerOptions {
  tenantId?: string | null;
  contentType?: string;
  useCredentials?: boolean;
  contextHeaders?: Record<string, unknown> | null;
}

export interface NormalizedError {
  status: number;
  data: unknown;
}

/** Transport construction only. Interceptors/auth/error handling are not implemented. */
export abstract class RequestHandler {
  protected readonly requestHandler: AxiosInstance;

  constructor(baseUrl: string, options: RequestHandlerOptions = {}) {
    this.requestHandler = axios.create({
      baseURL: baseUrl,
      withCredentials: options.useCredentials ?? false,
      headers: { 'Content-Type': options.contentType ?? 'application/json' },
      responseType: 'json',
    });
  }
}
