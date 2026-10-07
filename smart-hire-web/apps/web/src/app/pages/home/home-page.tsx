import { SignupChoices } from '@smart-hire/components';
import { useAppCoreContext } from '@smart-hire/core';

import { AuthLayout } from '../../layouts/auth-layout';

export function HomePage() {
  const { navigationService } = useAppCoreContext();

  return (
    <AuthLayout
      eyebrow="Get started"
      title="What brings you here?"
      description="Choose where to start. You can use the same account for both later."
    >
      <SignupChoices
        onCandidate={() => navigationService.navigate('Register')}
        onOrganization={() => navigationService.navigate('CreateOrganization')}
        onLogin={() => navigationService.navigate('Login')}
      />
    </AuthLayout>
  );
}
