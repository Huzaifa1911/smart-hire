import {
  WorkspaceRole,
  type CandidateProfile,
  type WorkspaceSummary,
} from '@smart-hire/types';
import { Button } from '@smart-hire/ui';

export function SignupChoices({
  onCandidate,
  onOrganization,
  onLogin,
}: {
  onCandidate: () => void;
  onOrganization: () => void;
  onLogin: () => void;
}) {
  return (
    <div className="grid gap-4">
      <Button
        variant="outline"
        className="h-auto justify-between whitespace-normal p-5 text-left"
        onClick={onCandidate}
      >
        <span>
          <span className="block text-base font-semibold">Find a job</span>
          <span className="mt-1 block text-sm font-normal text-muted-foreground">
            Create your candidate profile and apply for roles.
          </span>
        </span>
        <span aria-hidden="true">↗</span>
      </Button>
      <Button
        variant="outline"
        className="h-auto justify-between whitespace-normal p-5 text-left"
        onClick={onOrganization}
      >
        <span>
          <span className="block text-base font-semibold">
            Hire for your organization
          </span>
          <span className="mt-1 block text-sm font-normal text-muted-foreground">
            Create a workspace for your hiring team.
          </span>
        </span>
        <span aria-hidden="true">＋</span>
      </Button>
      <Button variant="link" onClick={onLogin}>
        Already have an account? Sign in
      </Button>
    </div>
  );
}

export function WorkspacePicker({
  workspaces = [],
  onSelect,
  onCandidate,
}: {
  workspaces?: WorkspaceSummary[];
  onSelect?: (workspace: WorkspaceSummary) => void;
  onCandidate?: () => void;
}) {
  return (
    <div className="grid gap-3">
      {workspaces.length === 0 && (
        <p className="rounded-lg bg-muted p-5 text-sm text-muted-foreground">
          No organization workspaces yet.
        </p>
      )}
      {workspaces.map((workspace) => (
        <Button
          key={workspace.id}
          variant="outline"
          className="h-auto justify-between whitespace-normal p-5 text-left"
          disabled={!onSelect}
          onClick={() => onSelect?.(workspace)}
        >
          <span>
            <span className="block text-base font-semibold">
              {workspace.name}
            </span>
            <span className="mt-1 block text-sm font-normal capitalize text-muted-foreground">
              {workspace.role} · Organization workspace
            </span>
          </span>
          <span aria-hidden="true">→</span>
        </Button>
      ))}
      <div className="mt-2 border-t pt-5">
        <Button
          variant="secondary"
          className="h-auto w-full justify-between whitespace-normal p-5 text-left"
          disabled={!onCandidate}
          onClick={onCandidate}
        >
          <span>
            <span className="block font-semibold">
              Personal candidate profile
            </span>
            <span className="mt-1 block text-sm font-normal text-muted-foreground">
              Find opportunities and track your applications.
            </span>
          </span>
          <span aria-hidden="true">↗</span>
        </Button>
      </div>
    </div>
  );
}

export function InvitationPanel({
  accept = false,
  organizationName,
  invitedEmail,
  onAccept,
  onRegister,
  onLogin,
}: {
  accept?: boolean;
  organizationName?: string;
  invitedEmail?: string;
  onAccept?: () => void;
  onRegister?: () => void;
  onLogin?: () => void;
}) {
  return (
    <div className="grid gap-5">
      <div className="rounded-lg bg-muted p-4 text-sm">
        <p className="font-medium">
          {organizationName ?? 'Organization workspace'}
        </p>
        <p className="mt-2 text-muted-foreground">
          Recruiter invitation{invitedEmail ? ` for ${invitedEmail}` : ''}
        </p>
      </div>
      {accept ? (
        <>
          <p className="text-sm text-muted-foreground">
            Accepting adds this workspace to your account.
          </p>
          <Button className="h-11" disabled={!onAccept} onClick={onAccept}>
            Accept invitation
          </Button>
        </>
      ) : (
        <>
          <Button className="h-11" disabled={!onRegister} onClick={onRegister}>
            Create an account to join
          </Button>
          <Button variant="link" disabled={!onLogin} onClick={onLogin}>
            Already have an account? Sign in to join
          </Button>
        </>
      )}
    </div>
  );
}

export function EnableCandidatePanel({
  name,
  email,
  onEnable,
  onBack,
}: {
  name?: string;
  email?: string;
  onEnable?: () => void;
  onBack?: () => void;
}) {
  return (
    <div className="grid gap-5">
      {(name || email) && (
        <div className="rounded-lg bg-muted p-4">
          {name && <p className="font-medium">{name}</p>}
          {email && (
            <p className="mt-1 text-sm text-muted-foreground">{email}</p>
          )}
        </div>
      )}
      <Button className="h-11" disabled={!onEnable} onClick={onEnable}>
        Enable candidate access
      </Button>
      <Button variant="link" disabled={!onBack} onClick={onBack}>
        Return to workspace selection
      </Button>
    </div>
  );
}

export function CandidateHomePanel({
  profile,
  hasOrganizationAccess = false,
  onSwitchWorkspace,
  onEditProfile,
  onBrowseJobs,
  onAddResume,
}: {
  profile?: CandidateProfile;
  hasOrganizationAccess?: boolean;
  onSwitchWorkspace?: () => void;
  onEditProfile?: () => void;
  onBrowseJobs?: () => void;
  onAddResume?: () => void;
}) {
  return (
    <div className="grid gap-5">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b pb-4">
        <span className="text-sm text-muted-foreground">
          Personal · Candidate
        </span>
        {hasOrganizationAccess && (
          <Button
            variant="ghost"
            size="sm"
            disabled={!onSwitchWorkspace}
            onClick={onSwitchWorkspace}
          >
            Switch workspace ↓
          </Button>
        )}
      </div>
      <div className="rounded-lg bg-muted p-5">
        <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
          Your profile
        </p>
        <p className="mt-2 font-semibold">
          {profile?.headline ?? 'Complete your profile'}
        </p>
        <p className="mt-1 text-sm text-muted-foreground">
          {profile
            ? `${profile.location} · ${profile.experience} years of experience`
            : 'Add your experience and location.'}
        </p>
        <Button
          variant="link"
          className="mt-3 h-auto p-0"
          disabled={!onEditProfile}
          onClick={onEditProfile}
        >
          {profile ? 'Edit profile' : 'Create profile'}
        </Button>
      </div>
      <Button className="h-11" disabled={!onBrowseJobs} onClick={onBrowseJobs}>
        Browse jobs
      </Button>
      <Button
        variant="outline"
        className="h-11"
        disabled={!onAddResume}
        onClick={onAddResume}
      >
        Add your resume
      </Button>
      <p className="text-center text-xs text-muted-foreground">
        Your applications will appear here once you start applying.
      </p>
    </div>
  );
}

export function RecruiterHomePanel({
  workspace,
  onSwitchWorkspace,
  onCreateJob,
  onCandidate,
}: {
  workspace?: WorkspaceSummary;
  onSwitchWorkspace?: () => void;
  onCreateJob?: () => void;
  onCandidate?: () => void;
}) {
  return (
    <div className="grid gap-5">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b pb-4">
        <span className="text-sm capitalize text-muted-foreground">
          {workspace
            ? `${workspace.name} · ${workspace.role}`
            : 'Organization workspace'}
        </span>
        <Button
          variant="ghost"
          size="sm"
          disabled={!onSwitchWorkspace}
          onClick={onSwitchWorkspace}
        >
          Switch workspace ↓
        </Button>
      </div>
      <div className="rounded-lg bg-muted p-5">
        <p className="font-semibold">{workspace?.name ?? 'Your hiring team'}</p>
        <p className="mt-2 text-sm text-muted-foreground">
          {workspace?.role === WorkspaceRole.Owner
            ? 'You own this workspace. Bring your hiring team together.'
            : 'Bring your hiring team together and manage your postings.'}
        </p>
      </div>
      <Button className="h-11" disabled={!onCreateJob} onClick={onCreateJob}>
        Create your first job
      </Button>
      <div className="border-t pt-5">
        <p className="text-sm text-muted-foreground">
          Want to apply for jobs too?
        </p>
        <Button
          variant="link"
          className="mt-2 h-auto p-0"
          disabled={!onCandidate}
          onClick={onCandidate}
        >
          Set up candidate access →
        </Button>
      </div>
    </div>
  );
}
