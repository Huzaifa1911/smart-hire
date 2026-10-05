import type { NavigateFunction } from 'react-router-dom';

import type {
  NavigationService,
  RootParamList,
  RouteArgs,
} from '@smart-hire/types';

import { buildPath } from '../routing/routes';

/** Named-route navigation backed by the router injected by App. */
export class WebNavigationService implements NavigationService {
  constructor(private readonly routerNavigate: NavigateFunction) {}

  navigate<Name extends keyof RootParamList>(
    name: Name,
    ...args: RouteArgs<Name>
  ): void {
    this.routerNavigate(buildPath(name, args), { state: args[0] });
  }

  replace<Name extends keyof RootParamList>(
    name: Name,
    ...args: RouteArgs<Name>
  ): void {
    this.routerNavigate(buildPath(name, args), {
      replace: true,
      state: args[0],
    });
  }

  reset<Name extends keyof RootParamList>(
    name: Name,
    ...args: RouteArgs<Name>
  ): void {
    // Browsers cannot erase earlier history entries; reset replaces this entry.
    this.replace(name, ...args);
  }

  goBack(): void {
    if (this.canGoBack()) this.routerNavigate(-1);
  }

  canGoBack(): boolean {
    // BrowserRouter tracks its own index; history.length can include other sites.
    const index: unknown = window.history.state?.idx;

    return typeof index === 'number' && index > 0;
  }
}
