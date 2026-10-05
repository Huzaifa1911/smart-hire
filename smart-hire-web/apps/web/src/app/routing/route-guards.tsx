import { Outlet } from 'react-router-dom';

/** Passthrough placeholders: these do not enforce authentication. */
export function ProtectedRoute() {
  return <Outlet />;
}

export function GuestRoute() {
  return <Outlet />;
}
