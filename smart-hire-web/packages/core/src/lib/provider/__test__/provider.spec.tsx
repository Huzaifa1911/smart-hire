import { render, waitFor } from '@testing-library/react';

import { useAppCoreContext } from '../../context/index';
import { AppCoreProvider } from '../provider';

const services = {
  baseUrl: 'https://example.com',
  platformName: 'SmartHire',
  contextAwareness: { experience: 'web' },
  storageService: {
    getItem: jest.fn().mockReturnValue(null),
    setItem: jest.fn(),
    removeItem: jest.fn(),
  },
  navigationService: {
    navigate: jest.fn(),
    replace: jest.fn(),
    reset: jest.fn(),
    goBack: jest.fn(),
    canGoBack: jest.fn().mockReturnValue(false),
  },
  alertService: {
    show: jest.fn().mockReturnValue('alert-id'),
    hide: jest.fn(),
    confirm: jest.fn().mockResolvedValue(false),
  },
};

test('keeps context stable for unchanged props and publishes changed metadata', async () => {
  const observe = jest.fn();

  function Consumer() {
    observe(useAppCoreContext());

    return null;
  }

  const child = <Consumer />;
  const { rerender } = render(
    <AppCoreProvider {...services}>{child}</AppCoreProvider>,
  );

  await waitFor(() => expect(observe).toHaveBeenCalledTimes(1));
  const original = observe.mock.calls[0][0];

  rerender(<AppCoreProvider {...services}>{child}</AppCoreProvider>);
  expect(observe).toHaveBeenCalledTimes(1);

  rerender(
    <AppCoreProvider {...services} platformName="Updated">
      {child}
    </AppCoreProvider>,
  );
  expect(observe).toHaveBeenCalledTimes(2);
  expect(observe.mock.calls[1][0]).not.toBe(original);
  expect(observe.mock.calls[1][0].platformName).toBe('Updated');
});
