import { LoginForm } from '@smart-hire/components';
import { useAppCoreContext } from '@smart-hire/core';
import { Button } from '@smart-hire/ui';

import { AuthLayout } from '../../layouts/auth-layout';

export function LoginPage() {
  const { navigationService } = useAppCoreContext();

  return (
    <AuthLayout
      eyebrow="Welcome back"
      title="Sign in to SmartHire."
      description="Your account connects your candidate profile and organization workspaces."
      back={() => navigationService.navigate('Home')}
      footer={
        <Button
          variant="link"
          onClick={() => navigationService.navigate('Home')}
        >
          New here? Create an account
        </Button>
      }
    >
      <LoginForm />
    </AuthLayout>
  );
}
