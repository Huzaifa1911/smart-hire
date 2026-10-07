# SmartHire frontend

Nx/pnpm React workspace with responsive account and workspace screens. This implementation covers UI composition, form fields, validation and screen navigation only. There are no mock accounts, memberships, seeded data or simulated signup/login/invitation actions. No API endpoint methods, authentication requests or token refresh are implemented.

## Reference architecture review

The earlier baseline diverged from the reference in four material ways: API endpoint factories replaced its class hierarchy; `CoreProvider` replaced its app-wide injected context; grouped type/utility modules were flattened; and web adapters/route declarations were omitted. Those differences have been corrected. The reference's directory organization, declarations and dependency injection pattern are followed, with SmartHire package names and backend URL configuration. Reference business behavior and endpoint contracts are not copied.

```text
apps/web/src/
  main.tsx                         # BrowserRouter -> App
  styles.css                       # imports the shared Tailwind theme
  app/
    app.tsx                        # constructs platform adapters, injects provider
    config/env.ts
    services/
      storage.service.ts
      navigation.service.ts
      alert.service.ts
    routing/
      route-types.d.ts             # augments RootParamList
      routes.ts                    # named route registry and path builder
      route-guards.tsx             # authentication integration extension points
    layouts/auth-layout.tsx
    pages/
      home/home-page.tsx            # account-path selection
      home/workspace-pages.tsx      # candidate/recruiter home, profile, workspace selection
      auth/                        # signup, login, organization creation, invitations

packages/api/src/
  index.ts
  lib/
    axios-client/
      index.ts                     # APIClient facade
      request-handler.ts           # abstract Axios transport base
      clients/iamApi.client.ts     # empty subclass, no endpoint methods
    auth/
      index.ts
      authentication-handler.ts    # no-op init/dispose extension points
      auth-store.ts                # vanilla Zustand identity placeholder
      token-refresher.ts           # type declaration only
    utils/index.ts                 # empty transport helper extension point

packages/core/src/
  index.ts
  lib/
    context/index.ts               # IContextState, AppCoreContext, useAppCoreContext
    provider/provider.tsx          # AppCoreProvider
    query-client/index.ts          # AppQueryClient singleton
    hooks/
      index.ts
      auth-api-hooks/index.ts       # empty API hook extension point

packages/types/src/
  index.ts                         # type and enum barrel exports
  lib/
    api/auth.types.ts              # AccountInfo placeholder
    common/response.types.ts       # SmartHire success envelope
    common/onboarding.types.ts     # UI display/form contracts, routes and enums
    services/
      storage-service.types.ts
      navigation-service.types.ts
      alert-service.types.ts

packages/utils/src/
  index.ts
  lib/
    common/{constants,utils}.ts
    common/phone.ts                # international phone helpers
    schemas/auth-schemas.ts         # future authentication validation extension point
    schemas/onboarding-validation.ts # plain form validation functions
```

`packages/components/src/lib/onboarding` contains account forms, workspace selection, invitation and home panels. Feature forms use React Hook Form with shared `Form`/`FormInput` controls and validation from utils, following the reference architecture. `packages/ui` uses the reference ui-web layout: per-component folders/barrels under src/lib/components, shared utils/styles, and adapted components.json. It implements shared buttons, cards, inputs, labels, form wrappers, phone inputs, icons, themed toast infrastructure and AlertActions. OTP input is excluded. Web pages compose those feature components inside the shared account layout. The reference's OTP behavior is not a SmartHire requirement and has not been added.

## How the layers connect

1. `main.tsx` mounts `BrowserRouter` and `App`.
2. `App` creates stable `WebStorageService`, `WebNavigationService`, and `WebAlertService` instances. Their contracts live in types; their platform implementations belong to web. Storage uses browser localStorage with graceful handling of blocked/full storage. Navigation uses the named route registry and injected React Router navigation. Alerts use Sonner toasts and browser confirmation dialogs.
3. `AppCoreProvider` receives those adapters, platform metadata and `baseUrl`. It constructs the `APIClient` facade and shares it through `AppCoreContext`.
4. `APIClient.iamApiClient` lazily constructs and caches `IamApiClient`, which extends `RequestHandler`. The base configures an Axios instance; it makes no request by itself. Context/tenant options reserve future interceptor wiring; no headers, auth or refresh behavior is implemented yet.
5. The provider constructs the bootstrap-only `AuthenticationHandler` with IAM and storage dependencies. Its `init()` and `dispose()` are no-op lifecycle placeholders. It performs no session restoration or persistence.
6. The provider reads the placeholder identity from the vanilla Zustand `authStore` and publishes `accountInfo`, adapters, metadata and API facade together. `AppQueryClient` is supplied through `QueryClientProvider`, following the reference's singleton pattern.
7. Feature forms and panels receive display data and callbacks through props; web pages compose them and wire screen navigation. Future API hooks read `useAppCoreContext()`, call service-client endpoint methods and manage server state. Future feature components consume those hooks. Web pages only compose features and register routes.

Service contracts use TypeScript interfaces. Shared onboarding route names extend `RootParamList`; apps can augment it further; `RouteArgs` makes navigation parameters follow the selected route. The route registry is checked against those names. Fixed value sets such as AlertVariant and AlertActionStyle use string enums exported by the types package. Other contracts remain type-only exports. Implementations use enum members rather than repeating string literals.

API owns the reference's transport/auth modules; core owns React context, provider and API/business hooks; utils owns general helper/validation module slots. Nx scope rules retain the permitted package dependency direction. Imports go through package barrels, while files within a package use relative imports.

`AccountInfo.user` remains `unknown | null` until concrete IAM identity contracts are introduced. No sample signup, OTP, user or refresh shapes are assumed. The response type matches SmartHire's success envelope rather than the reference backend's envelope.

## Local setup and validation

From this directory:

```sh
pnpm install
cp apps/web/.env.example apps/web/.env.local
pnpm exec nx dev web
pnpm exec nx sync
pnpm exec nx run-many -t lint typecheck
pnpm exec nx build web
```

The development URL is `http://localhost:4200`. `VITE_API_HOST` defaults to `http://localhost:8000`; the provider derives `/iam-service/v1/`. Configuration is public build-time configuration, not a place for secrets. No endpoint is contacted on startup.

All UI routes can be opened directly. Protected/guest guards remain unwired extension points; there is no simulated authentication or access control. Refresh/interceptor hooks and IAM integration are still required for real authentication. Web adapter tests cover persistence failures, safe back navigation, replace/reset behavior, toast variants/actions/dismissal and confirmation results. Tests live in `__test__` folders beside the relevant source modules. Run `pnpm exec nx run-many -t test -p ui core web`.

## Code style and adapter semantics

Imports are grouped as third-party libraries, workspace packages, then local files, with one blank line between groups. ESLint enforces import grouping, spacing around declarations/returns and separation of class members. Recommended JSX accessibility rules apply to React files, including accessible content for headings and `CardTitle`. Prettier handles indentation and wrapping.

Web navigation `reset` replaces the current entry; browsers do not permit clearing earlier history. `canGoBack` checks BrowserRouter's history index rather than the browser's total history length. See [React Router navigation](https://reactrouter.com/6.30.3/hooks/use-navigate).

Alerts use the shared [Sonner toast host](https://github.com/emilkowalski/sonner). All supplied actions are displayed in a wrapping button group. Cancel, default and destructive actions use shared Button variants and theme tokens. Clicking an action invokes its callback and dismisses the toast. Toasts receive string IDs so targeted dismissal uses the same ID. Confirmation uses the native browser dialog. Storage operations are best-effort; blocked reads return null and blocked/full writes do not interrupt callers.

Import boundaries cover TS/JS, JSX, and MTS/CTS/MJS/CJS files. Provider context dependencies are individual injected services and metadata, preserving the context value when those references remain unchanged. Regression tests cover context stability, metadata updates and all alert actions. `ApiResponse<T>` is the success envelope with `success: true`; error responses are a separate contract.

## UI screens

The route registry includes account-path selection (`/`), signup (`/register`), login (`/login`), organization creation (`/organizations/new`), invitations (`/invitation`, `/invitation/accept`), workspace selection (`/workspaces`), candidate profile setup (`/candidate/profile`), candidate access (`/candidate/enable`), candidate home (`/candidate`) and recruiter home (`/organization`).

Forms use React Hook Form and shared UI fields with accessible errors. They accept optional submission callbacks; submit controls remain disabled until a caller supplies one. No data is saved, no credentials are checked and submission does not simulate success. Display components accept optional profile/workspace/invitation data rather than supplying fictional records. Empty states render when data is absent. Candidate workspace switching is controlled by the `hasOrganizationAccess` presentation prop and is hidden by default.

Pages wire navigation between existing screens. Invitation acceptance, candidate access changes, job creation, job browsing and resume upload have no behavior until a caller provides the appropriate callbacks. There are no preview controls, seeded identities, account-flow state or demonstration toasts. The layout uses semantic landmarks, labeled controls, keyboard focus on each new screen heading and theme tokens.
