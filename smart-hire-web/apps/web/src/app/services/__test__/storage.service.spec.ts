import { WebStorageService } from '../storage.service';

const service = new WebStorageService();

afterEach(() => {
  jest.restoreAllMocks();
  window.localStorage.clear();
});

test('persists and removes values while missing values return null', () => {
  expect(service.getItem('session')).toBeNull();
  service.setItem('session', 'value');
  expect(service.getItem('session')).toBe('value');
  service.removeItem('session');
  expect(service.getItem('session')).toBeNull();
});

test('handles unavailable storage without interrupting callers', () => {
  for (const method of ['getItem', 'setItem', 'removeItem'] as const) {
    jest.spyOn(Storage.prototype, method).mockImplementation(() => {
      throw new DOMException('Blocked', 'SecurityError');
    });
  }

  expect(service.getItem('session')).toBeNull();
  expect(() => service.setItem('session', 'value')).not.toThrow();
  expect(() => service.removeItem('session')).not.toThrow();
});
