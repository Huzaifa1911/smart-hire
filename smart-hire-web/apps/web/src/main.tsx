import { StrictMode } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { createRoot } from 'react-dom/client';

import { ThemeProvider } from '@smart-hire/ui';

import App from './app/app';
import './styles.css';

const root = document.getElementById('root');

if (!root) throw new Error('Root element is missing');

createRoot(root).render(
  <StrictMode>
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ThemeProvider>
  </StrictMode>,
);
