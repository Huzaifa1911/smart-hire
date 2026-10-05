# @smart-hire/ui

Shared web UI package, organized like the supplied ui-web reference.

```text
src/
  index.ts
  lib/
    utils.ts
    styles/globals.css
    components/
      alert-actions/{alert-actions.tsx,index.ts}
      button/{button.tsx,index.ts}
      card/{card.tsx,index.ts}
      form/{form.tsx,index.ts}
      icons/index.ts
      input/{input.tsx,form-input.tsx,index.ts}
      label/{label.tsx,index.ts}
      phone-input/{phone-input.tsx,phone-form-input.tsx,index.ts}
      sonner/{sonner.tsx,index.ts}
```

Each component has its own folder and local barrel; the package barrel exposes its public API. Consumers import from `@smart-hire/ui`, and apps import `@smart-hire/ui/globals.css` once for shared styles. `cn` combines class names and resolves Tailwind conflicts.

Implemented primitives: Button (variants, sizes and asChild), Card and its sections, Input, Label, Form/FieldShell, FormInput, PhoneInput/PhoneFormInput, icon exports, themed Toaster/ThemeProvider and AlertActions. OTP input is deliberately excluded.

Form is React Hook Form's provider, not an HTML form element. Use it around a `<form>` with handleSubmit. FormInput and PhoneFormInput read the surrounding form context, support field rules, preserve caller IDs/help-text associations, show validation errors, and forward refs for focus management. Form wrappers own their value/change/ref bindings; plain Input/PhoneInput remain independently usable. Button defaults to type="button"; set type="submit" for submission.

Phone inputs expect an international country calling code. They emit a normalized plus-prefixed value and format partial input for display; normalization does not prove validity. `isValidPhone` is the separate validation helper. Phone helpers live in utils; no country-selection UI or automatic country inference is added.

Tailwind 4 is compiled through the web Vite plugin. The shared stylesheet defines light/dark design tokens and scans UI, feature and web sources. ThemeProvider at the web entry point selects system/light/dark appearance via the HTML class; Toaster consumes that theme and exports the reference icon set. Add new app source paths to the stylesheet as apps are introduced.

`components.json` records the shared stylesheet and aliases. Keep generated primitives in their component folder with a local barrel. Styling helper cn lives here to match the reference; feature/business hooks belong to core.

Validation: `pnpm exec nx run-many -t test -p ui core web`, `pnpm exec nx run-many -t lint typecheck`, and `pnpm exec nx build web`. UI tests cover form validation/focus/value submission and button composition/submission behavior. Tests live in __test__ folders.

References: [shadcn Vite setup](https://ui.shadcn.com/docs/installation/vite), [React Hook Form](https://react-hook-form.com/docs/usecontroller), [theme provider](https://github.com/pacocoursey/next-themes).

UI may import only types/utils from this workspace. Styling helpers such as cn live here to match the reference package; reusable non-UI utilities remain in utils. Existing Nx source exports and TypeScript/Jest configuration are retained instead of copying the reference's build configuration.

See the [frontend README](../../README.md) for architecture and validation commands.
