/** SmartHire's existing success envelope; no sample backend contract is imported. */
export interface ApiResponse<T> {
  success: true;
  data: T;
}
