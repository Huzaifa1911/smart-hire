import { useMemo } from 'react';
import { Route, Routes, useNavigate } from 'react-router-dom';

import { AppCoreProvider } from '@smart-hire/core';
import { Toaster } from '@smart-hire/ui';

import { API_HOST, PLATFORM_NAME } from './config/env';
import { WebStorageService } from './services/storage.service';
import { WebNavigationService } from './services/navigation.service';
import { WebAlertService } from './services/alert.service';
import { ROUTES } from './routing/routes';

export function App() {
  const navigate = useNavigate();
  const storageService = useMemo(() => new WebStorageService(), []);
  const navigationService = useMemo(
    () => new WebNavigationService(navigate),
    [navigate],
  );
  const alertService = useMemo(() => new WebAlertService(), []);
  const contextAwareness = useMemo(
    () => ({ experience: 'web', application: 'smart-hire' }),
    [],
  );
  const { Home } = ROUTES;

  return (
    <AppCoreProvider
      baseUrl={API_HOST}
      platformName={PLATFORM_NAME}
      contextAwareness={contextAwareness}
      storageService={storageService}
      navigationService={navigationService}
      alertService={alertService}
    >
      <Routes>
        <Route path={Home.path} element={<Home.Component />} />
      </Routes>
      <Toaster />
    </AppCoreProvider>
  );
}

export default App;
