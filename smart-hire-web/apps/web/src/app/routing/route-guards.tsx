import { Outlet } from 'react-router-dom';

/** Reserved for authentication integration; no authorization behavior yet. */
export function ProtectedRoute() {
  return <Outlet />;
}

export function GuestRoute() {
  return <Outlet />;
}
