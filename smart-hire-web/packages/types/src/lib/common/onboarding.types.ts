/** Presentation contracts for account and workspace screens. */
export enum SignupMode {
  Candidate = 'candidate',
  Organization = 'organization',
  Invitation = 'invitation',
}

export enum WorkspaceRole {
  Owner = 'owner',
  Recruiter = 'recruiter',
}

export interface WorkspaceSummary {
  id: string;
  name: string;
  role: WorkspaceRole;
}

export interface CandidateProfile {
  headline: string;
  location: string;
  experience: number;
}

export interface SignupValues {
  name: string;
  email: string;
  organization?: string;
}

export interface SignupFormValues extends SignupValues {
  password: string;
}

export interface LoginFormValues {
  email: string;
  password: string;
}

export interface OnboardingRoutes {
  Home: undefined;
  Login: undefined;
  Register: undefined;
  CreateOrganization: undefined;
  Invitation: undefined;
  AcceptInvitation: undefined;
  Profile: undefined;
  CandidateHome: undefined;
  RecruiterHome: undefined;
  Workspaces: undefined;
  EnableCandidate: undefined;
}
