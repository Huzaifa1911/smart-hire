import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { useForm } from 'react-hook-form';

import { Form } from '../form';
import { FormInput } from '../../input';
import { PhoneFormInput } from '../../phone-input';
import { Button } from '../../button';

function Example({
  onSubmit,
}: {
  onSubmit: (values: { email: string; phone: string }) => void;
}) {
  const methods = useForm({ defaultValues: { email: '', phone: '' } });

  return (
    <Form {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        <p id="email-hint">Use your work email.</p>
        <FormInput
          name="email"
          label="Email"
          id="email-field"
          aria-describedby="email-hint"
          rules={{ required: 'Email is required' }}
        />
        <PhoneFormInput name="phone" label="Phone" />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  );
}

test('connects labels, validation errors, focus and controlled form values', async () => {
  const onSubmit = jest.fn();

  render(<Example onSubmit={onSubmit} />);
  fireEvent.click(screen.getByRole('button', { name: 'Submit' }));
  const error = await screen.findByRole('alert');
  const email = screen.getByRole('textbox', {
    name: 'Email',
  }) as HTMLInputElement;

  expect(error.textContent).toBe('Email is required');
  expect(email.id).toBe('email-field');
  expect(email.getAttribute('aria-invalid')).toBe('true');
  expect(email.getAttribute('aria-describedby')).toBe(`email-hint ${error.id}`);
  await waitFor(() => expect(document.activeElement).toBe(email));
  expect(onSubmit).not.toHaveBeenCalled();
  fireEvent.change(email, { target: { value: 'user@example.com' } });
  fireEvent.change(screen.getByRole('textbox', { name: 'Phone' }), {
    target: { value: '+92 300 1234567' },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Submit' }));
  await waitFor(() =>
    expect(onSubmit).toHaveBeenCalledWith(
      { email: 'user@example.com', phone: '+923001234567' },
      expect.anything(),
    ),
  );
  expect(email.getAttribute('aria-invalid')).toBe('false');
  expect(email.getAttribute('aria-describedby')).toBe('email-hint');
});
