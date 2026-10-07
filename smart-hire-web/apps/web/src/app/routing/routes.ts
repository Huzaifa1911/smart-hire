import type { ComponentType } from 'react';

import type { RootParamList, RouteArgs } from '@smart-hire/types';

import { HomePage } from '../pages/home/home-page';
import { LoginPage } from '../pages/auth/login-page';
import { RegisterPage } from '../pages/auth/register-page';
import { OrganizationPage } from '../pages/auth/organization-page';
import {
  InvitationPage,
  AcceptInvitationPage,
} from '../pages/auth/invitation-page';
import {
  WorkspacesPage,
  ProfilePage,
  EnableCandidatePage,
  CandidateHomePage,
  RecruiterHomePage,
} from '../pages/home/workspace-pages';

interface RouteConfig {
  path: string;
  Component: ComponentType;
  toPath: (params?: unknown) => string;
}

export const ROUTES = {
  Home: { path: '/', Component: HomePage, toPath: () => '/' },
  Login: { path: '/login', Component: LoginPage, toPath: () => '/login' },
  Register: {
    path: '/register',
    Component: RegisterPage,
    toPath: () => '/register',
  },
  CreateOrganization: {
    path: '/organizations/new',
    Component: OrganizationPage,
    toPath: () => '/organizations/new',
  },
  Invitation: {
    path: '/invitation',
    Component: InvitationPage,
    toPath: () => '/invitation',
  },
  AcceptInvitation: {
    path: '/invitation/accept',
    Component: AcceptInvitationPage,
    toPath: () => '/invitation/accept',
  },
  Workspaces: {
    path: '/workspaces',
    Component: WorkspacesPage,
    toPath: () => '/workspaces',
  },
  Profile: {
    path: '/candidate/profile',
    Component: ProfilePage,
    toPath: () => '/candidate/profile',
  },
  EnableCandidate: {
    path: '/candidate/enable',
    Component: EnableCandidatePage,
    toPath: () => '/candidate/enable',
  },
  CandidateHome: {
    path: '/candidate',
    Component: CandidateHomePage,
    toPath: () => '/candidate',
  },
  RecruiterHome: {
    path: '/organization',
    Component: RecruiterHomePage,
    toPath: () => '/organization',
  },
} satisfies Record<keyof RootParamList, RouteConfig>;

export function buildPath<Name extends keyof RootParamList>(
  name: Name,
  args: RouteArgs<Name>,
): string {
  return (ROUTES[name].toPath as (params?: unknown) => string)(args[0]);
}
