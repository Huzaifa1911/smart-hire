/** Apps augment this interface with their own named routes. */
// eslint-disable-next-line @typescript-eslint/no-empty-interface, @typescript-eslint/no-empty-object-type
export interface RootParamList {}

export type RouteArgs<Name extends keyof RootParamList> =
  undefined extends RootParamList[Name]
    ? [params?: RootParamList[Name]]
    : [params: RootParamList[Name]];

export interface NavigationService {
  navigate<Name extends keyof RootParamList>(
    name: Name,
    ...args: RouteArgs<Name>
  ): void;
  replace<Name extends keyof RootParamList>(
    name: Name,
    ...args: RouteArgs<Name>
  ): void;
  reset<Name extends keyof RootParamList>(
    name: Name,
    ...args: RouteArgs<Name>
  ): void;
  goBack(): void;
  canGoBack(): boolean;
}
