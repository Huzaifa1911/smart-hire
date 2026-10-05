import { fireEvent, render, screen } from '@testing-library/react';

import { Button } from '../button';

test('ordinary buttons do not submit their surrounding form', () => {
  const submit = jest.fn();

  render(
    <form
      onSubmit={(event) => {
        event.preventDefault();
        submit();
      }}
    >
      <Button>Cancel</Button>
      <Button type="submit">Save</Button>
    </form>,
  );
  fireEvent.click(screen.getByRole('button', { name: 'Cancel' }));
  expect(submit).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: 'Save' }));
  expect(submit).toHaveBeenCalledTimes(1);
});

test('asChild composes a link without a nested button', () => {
  render(
    <Button asChild>
      <a href="/jobs">Jobs</a>
    </Button>,
  );
  expect(screen.getByRole('link', { name: 'Jobs' }).getAttribute('href')).toBe(
    '/jobs',
  );
  expect(screen.queryByRole('button')).toBeNull();
});
