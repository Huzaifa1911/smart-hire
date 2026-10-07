import { useForm } from 'react-hook-form';

import {
  SignupMode,
  type SignupFormValues,
  type LoginFormValues,
  type CandidateProfile,
} from '@smart-hire/types';
import { Button, Form, FormInput } from '@smart-hire/ui';
import {
  validateRequiredText,
  validateEmail,
  validateExperience,
} from '@smart-hire/utils';

export function SignupForm({
  mode,
  invitedEmail,
  onSubmit,
}: {
  mode: SignupMode;
  invitedEmail?: string;
  onSubmit?: (values: SignupFormValues) => void | Promise<void>;
}) {
  const organization = mode === SignupMode.Organization;
  const invitation = mode === SignupMode.Invitation;
  const form = useForm<SignupFormValues>({
    defaultValues: {
      name: '',
      email: invitedEmail ?? '',
      password: '',
      organization: '',
    },
  });

  return (
    <Form {...form}>
      <form
        noValidate
        className="grid gap-5"
        onSubmit={form.handleSubmit((values) => onSubmit?.(values))}
      >
        <FormInput<SignupFormValues>
          label="Full name"
          name="name"
          autoComplete="name"
          placeholder="Your full name"
          className="h-11"
          rules={{
            validate: validateRequiredText,
            maxLength: { value: 150, message: 'Use 150 characters or fewer.' },
          }}
        />
        <FormInput<SignupFormValues>
          label={organization ? 'Work email' : 'Email'}
          name="email"
          type="email"
          autoComplete="email"
          placeholder="name@example.com"
          className="h-11"
          readOnly={invitation && !!invitedEmail}
          rules={{ validate: validateEmail }}
        />
        <FormInput<SignupFormValues>
          label="Password"
          name="password"
          type="password"
          autoComplete="new-password"
          placeholder="At least 8 characters"
          className="h-11"
          rules={{
            required: 'Enter a password.',
            minLength: { value: 8, message: 'Use at least 8 characters.' },
          }}
        />
        {organization && (
          <FormInput<SignupFormValues>
            label="Organization name"
            name="organization"
            placeholder="Your organization"
            className="h-11"
            rules={{
              validate: validateRequiredText,
              maxLength: {
                value: 150,
                message: 'Use 150 characters or fewer.',
              },
            }}
          />
        )}
        <Button
          type="submit"
          className="h-11 w-full"
          disabled={!onSubmit || form.formState.isSubmitting}
        >
          {organization ? 'Create organization' : 'Create account'}
        </Button>
      </form>
    </Form>
  );
}

export function LoginForm({
  onSubmit,
}: {
  onSubmit?: (values: LoginFormValues) => void | Promise<void>;
} = {}) {
  const form = useForm<LoginFormValues>({
    defaultValues: { email: '', password: '' },
  });

  return (
    <Form {...form}>
      <form
        noValidate
        className="grid gap-5"
        onSubmit={form.handleSubmit((values) => onSubmit?.(values))}
      >
        <FormInput<LoginFormValues>
          label="Email"
          name="email"
          type="email"
          autoComplete="email"
          className="h-11"
          rules={{ validate: validateEmail }}
        />
        <FormInput<LoginFormValues>
          label="Password"
          name="password"
          type="password"
          autoComplete="current-password"
          className="h-11"
          placeholder="Enter your password"
          rules={{ required: 'Enter your password.' }}
        />
        <Button
          type="submit"
          className="h-11 w-full"
          disabled={!onSubmit || form.formState.isSubmitting}
        >
          Sign in
        </Button>
      </form>
    </Form>
  );
}

export function CandidateProfileForm({
  profile,
  onSubmit,
}: {
  profile?: CandidateProfile;
  onSubmit?: (values: CandidateProfile) => void | Promise<void>;
} = {}) {
  const form = useForm<CandidateProfile>({
    defaultValues: profile ?? {
      headline: '',
      location: '',
      experience: 0,
    },
  });

  return (
    <Form {...form}>
      <form
        noValidate
        className="grid gap-5"
        onSubmit={form.handleSubmit((values) =>
          onSubmit?.({
            headline: values.headline.trim(),
            location: values.location.trim(),
            experience: Number(values.experience),
          }),
        )}
      >
        <FormInput<CandidateProfile>
          label="Headline"
          name="headline"
          placeholder="Backend engineer"
          className="h-11"
          rules={{
            validate: validateRequiredText,
            maxLength: { value: 150, message: 'Use 150 characters or fewer.' },
          }}
        />
        <FormInput<CandidateProfile>
          label="Location"
          name="location"
          placeholder="Karachi"
          className="h-11"
          rules={{
            validate: validateRequiredText,
            maxLength: { value: 150, message: 'Use 150 characters or fewer.' },
          }}
        />
        <FormInput<CandidateProfile>
          label="Years of experience"
          name="experience"
          type="number"
          min={0}
          step="0.5"
          className="h-11"
          rules={{ validate: validateExperience }}
        />
        <Button
          type="submit"
          className="h-11 w-full"
          disabled={!onSubmit || form.formState.isSubmitting}
        >
          Save and continue
        </Button>
        <p className="text-xs text-muted-foreground">
          You can add skills and upload your resume from your profile later.
        </p>
      </form>
    </Form>
  );
}
