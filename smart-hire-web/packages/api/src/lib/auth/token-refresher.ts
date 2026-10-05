/** Refresh coordination will be implemented after the backend contract is settled. */
export type TokenRefresher = () => Promise<string | null>;
