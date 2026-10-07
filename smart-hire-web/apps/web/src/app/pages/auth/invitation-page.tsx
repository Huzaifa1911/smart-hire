import { InvitationPanel } from '@smart-hire/components';
import { useAppCoreContext } from '@smart-hire/core';

import { AuthLayout } from '../../layouts/auth-layout';

export function InvitationPage() {
  const { navigationService } = useAppCoreContext();

  return (
    <AuthLayout
      eyebrow="Team invitation"
      title="You’re invited to join a hiring team."
      description="Join an organization workspace as a recruiter."
      back={() => navigationService.navigate('Home')}
    >
      <InvitationPanel
        onRegister={() => navigationService.navigate('Register')}
        onLogin={() => navigationService.navigate('Login')}
      />
    </AuthLayout>
  );
}

export function AcceptInvitationPage() {
  return (
    <AuthLayout
      eyebrow="Account ready"
      title="Join the hiring team."
      description="Accept your invitation to access the organization workspace. Your personal profile stays with your account."
    >
      <InvitationPanel accept />
    </AuthLayout>
  );
}
