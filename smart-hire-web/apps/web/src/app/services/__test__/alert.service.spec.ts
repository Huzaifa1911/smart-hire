import { toast } from 'sonner';
import { fireEvent, render, screen } from '@testing-library/react';

import { AlertVariant, AlertActionStyle } from '@smart-hire/types';

import { WebAlertService } from '../alert.service';

jest.mock('sonner', () => ({
  toast: {
    info: jest.fn(),
    success: jest.fn(),
    warning: jest.fn(),
    error: jest.fn(),
    dismiss: jest.fn(),
  },
}));

const service = new WebAlertService();

afterEach(() => {
  jest.clearAllMocks();
  jest.restoreAllMocks();
});

test.each(Object.values(AlertVariant))(
  'supports %s alerts and stable dismissal ids',
  (variant) => {
    const id = service.show({
      title: 'Title',
      message: 'Details',
      variant,
      duration: 1000,
    });

    expect(toast[variant]).toHaveBeenCalledWith(
      'Title',
      expect.objectContaining({ id, description: 'Details', duration: 1000 }),
    );
    service.hide(id);
    expect(toast.dismiss).toHaveBeenCalledWith(id);
    service.hide();
    expect(toast.dismiss).toHaveBeenLastCalledWith(undefined);
  },
);

test('renders every action, styles destructive actions, and forwards callbacks', () => {
  const onPress = jest.fn();
  const onCancel = jest.fn();
  const onDelete = jest.fn();
  const onExtra = jest.fn();

  service.show({
    message: 'Message',
    actions: [
      { label: 'Undo', onPress },
      { label: 'Cancel', style: AlertActionStyle.Cancel, onPress: onCancel },
      {
        label: 'Delete',
        style: AlertActionStyle.Destructive,
        onPress: onDelete,
      },
      { label: 'Another action', onPress: onExtra },
    ],
  });
  const call = (toast.info as jest.Mock).mock.calls[0];

  expect(call[0]).toBe('Message');
  render(call[1].action);
  const remove = screen.getByRole('button', { name: 'Delete' });

  expect(remove.classList.contains('bg-destructive')).toBe(true);
  expect(remove.classList.contains('text-destructive-foreground')).toBe(true);
  expect(
    screen
      .getByRole('button', { name: 'Undo' })
      .classList.contains('bg-primary'),
  ).toBe(true);
  expect(
    screen
      .getByRole('button', { name: 'Cancel' })
      .classList.contains('bg-background'),
  ).toBe(true);
  expect(screen.getAllByRole('button')).toHaveLength(4);
  for (const label of ['Undo', 'Cancel', 'Delete', 'Another action']) {
    fireEvent.click(screen.getByRole('button', { name: label }));
  }
  expect(onPress).toHaveBeenCalledTimes(1);
  expect(onCancel).toHaveBeenCalledTimes(1);
  expect(onDelete).toHaveBeenCalledTimes(1);
  expect(onExtra).toHaveBeenCalledTimes(1);
  expect(toast.dismiss).toHaveBeenCalledTimes(4);
  expect(toast.dismiss).toHaveBeenLastCalledWith(call[1].id);
});

test.each([true, false])(
  'returns the browser confirmation result %s',
  async (result) => {
    const confirm = jest.spyOn(window, 'confirm').mockReturnValue(result);

    await expect(
      service.confirm({ title: 'Continue?', message: 'Details' }),
    ).resolves.toBe(result);
    expect(confirm).toHaveBeenCalledWith('Continue?\n\nDetails');
  },
);
