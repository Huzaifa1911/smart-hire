import {
  CandidateHomePanel,
  CandidateProfileForm,
  EnableCandidatePanel,
  RecruiterHomePanel,
  WorkspacePicker,
} from '@smart-hire/components';
import { useAppCoreContext } from '@smart-hire/core';

import { AuthLayout } from '../../layouts/auth-layout';

export function WorkspacesPage() {
  const { navigationService } = useAppCoreContext();

  return (
    <AuthLayout
      eyebrow="Your workspaces"
      title="Where would you like to go?"
      description="Select an organization to recruit, or use your personal candidate profile."
    >
      <WorkspacePicker
        onSelect={() => navigationService.navigate('RecruiterHome')}
        onCandidate={() => navigationService.navigate('CandidateHome')}
      />
    </AuthLayout>
  );
}

export function ProfilePage() {
  return (
    <AuthLayout
      eyebrow="Candidate profile"
      title="Introduce yourself."
      description="Add a few details to start your candidate profile."
    >
      <CandidateProfileForm />
    </AuthLayout>
  );
}

export function EnableCandidatePage() {
  const { navigationService } = useAppCoreContext();

  return (
    <AuthLayout
      eyebrow="Personal account"
      title="Find opportunities, too."
      description="Add candidate access to your existing account. Keep recruiting with all your current organizations."
    >
      <EnableCandidatePanel
        onBack={() => navigationService.navigate('Workspaces')}
      />
    </AuthLayout>
  );
}

export function CandidateHomePage() {
  const { navigationService } = useAppCoreContext();

  return (
    <AuthLayout
      eyebrow="Your opportunities"
      title="Ready for your next role."
      description="Discover opportunities and track your applications."
    >
      <CandidateHomePanel
        onEditProfile={() => navigationService.navigate('Profile')}
        onSwitchWorkspace={() => navigationService.navigate('Workspaces')}
      />
    </AuthLayout>
  );
}

export function RecruiterHomePage() {
  const { navigationService } = useAppCoreContext();

  return (
    <AuthLayout
      eyebrow="Hiring workspace"
      title="Your hiring workspace."
      description="Manage your organization's job postings and hiring pipeline."
    >
      <RecruiterHomePanel
        onSwitchWorkspace={() => navigationService.navigate('Workspaces')}
        onCandidate={() => navigationService.navigate('EnableCandidate')}
      />
    </AuthLayout>
  );
}
