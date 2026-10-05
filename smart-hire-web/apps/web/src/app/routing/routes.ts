import type { ComponentType } from 'react';

import type { RootParamList, RouteArgs } from '@smart-hire/types';

import { HomePage } from '../pages/home/home-page';

interface RouteConfig {
  path: string;
  Component: ComponentType;
  toPath: (params?: unknown) => string;
}

export const ROUTES = {
  Home: { path: '/', Component: HomePage, toPath: () => '/' },
} satisfies Record<keyof RootParamList, RouteConfig>;

export function buildPath<Name extends keyof RootParamList>(
  name: Name,
  args: RouteArgs<Name>,
): string {
  return (ROUTES[name].toPath as (params?: unknown) => string)(args[0]);
}
