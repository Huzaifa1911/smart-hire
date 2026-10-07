import { SignupForm } from '@smart-hire/components';
import { useAppCoreContext } from '@smart-hire/core';
import { SignupMode } from '@smart-hire/types';
import { Button } from '@smart-hire/ui';

import { AuthLayout } from '../../layouts/auth-layout';

export function OrganizationPage() {
  const { navigationService } = useAppCoreContext();

  return (
    <AuthLayout
      eyebrow="Organization signup"
      title="Start your hiring workspace."
      description="Create your account and your organization together. You will be the workspace owner."
      back={() => navigationService.navigate('Home')}
      footer={
        <Button
          variant="link"
          onClick={() => navigationService.navigate('Login')}
        >
          Already registered? Sign in
        </Button>
      }
    >
      <SignupForm mode={SignupMode.Organization} />
    </AuthLayout>
  );
}
