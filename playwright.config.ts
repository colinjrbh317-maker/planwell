import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for testing Federal Employee Retirement Calculators
 * Tests mobile-first design on iOS Safari and Chrome Android simulations
 */
export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  timeout: 45000, // Increase timeout to 45 seconds for slower mobile tests

  use: {
    baseURL: 'http://localhost:4321',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    actionTimeout: 15000, // Individual action timeout
    navigationTimeout: 15000, // Navigation timeout
  },

  projects: [
    {
      name: 'Desktop Chrome',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'Mobile Safari',
      use: {
        ...devices['iPhone 13'],
        // iOS Safari simulation
      },
    },
    {
      name: 'Mobile Chrome',
      use: {
        ...devices['Pixel 5'],
        // Android Chrome simulation
      },
    },
    {
      name: 'Tablet',
      use: {
        ...devices['iPad Pro'],
      },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:4321',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
