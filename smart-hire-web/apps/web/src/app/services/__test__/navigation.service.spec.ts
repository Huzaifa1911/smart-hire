import { WebNavigationService } from '../navigation.service';

const navigate = jest.fn();

const service = new WebNavigationService(navigate);

beforeEach(() => {
  navigate.mockClear();
  window.history.replaceState({ idx: 0 }, '');
});

test('pushes named routes and replaces the current entry for replace/reset', () => {
  service.navigate('Home');
  expect(navigate).toHaveBeenLastCalledWith('/', { state: undefined });
  service.replace('Home');
  expect(navigate).toHaveBeenLastCalledWith('/', {
    replace: true,
    state: undefined,
  });
  service.reset('Home');
  expect(navigate).toHaveBeenLastCalledWith('/', {
    replace: true,
    state: undefined,
  });
});

test('only goes back when the router has an earlier entry', () => {
  expect(service.canGoBack()).toBe(false);
  service.goBack();
  expect(navigate).not.toHaveBeenCalled();
  window.history.replaceState({ idx: 1 }, '');
  expect(service.canGoBack()).toBe(true);
  service.goBack();
  expect(navigate).toHaveBeenCalledWith(-1);
  window.history.replaceState(null, '');
  expect(service.canGoBack()).toBe(false);
});
