# Frontend Testing with Jest

## Quick Start

```bash
# Run all tests once
npm test

# Run tests in watch mode (re-runs on file changes)
npm run test:watch

# Run tests with coverage report
npm run test:coverage
```

## Project Structure

Test files are organized in a separate `tests/` folder:

```
frontend/
├── src/                    # Source code
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   └── ResultPage.tsx
│   └── ...
├── tests/                  # All test files
│   ├── pages/
│   │   ├── HomePage.test.tsx
│   │   └── ResultPage.test.tsx
│   └── setup/
│       └── setupTests.ts
├── jest.config.js
└── TESTING.md
```

## Configuration Files

- **`jest.config.js`** - Jest configuration optimized for React + TypeScript + Vite
  - Points to `tests/` folder for all test files
  - Configured for `tests/**/*.test.tsx` pattern
- **`tests/setup/setupTests.ts`** - Test environment setup
  - Imports testing utilities
  - Configures TextEncoder polyfill
  - Mocks window.matchMedia
- **`tsconfig.test.json`** - TypeScript config for test files

## Writing Tests

### Basic Test Template

```typescript
import { render, screen } from '@testing-library/react';
import MyComponent from '../src/components/MyComponent';

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />);
    expect(screen.getByText('Expected text')).toBeInTheDocument();
  });
});
```

### File Naming Convention

- Test files go in `tests/` folder (mirrors src structure)
- Filename: `ComponentName.test.tsx`
- Example: `tests/pages/HomePage.test.tsx`

### Common Test Patterns

**Testing text content:**
```typescript
expect(screen.getByText(/hello/i)).toBeInTheDocument();
```

**Testing form inputs:**
```typescript
const input = screen.getByRole('textbox');
fireEvent.change(input, { target: { value: 'new value' } });
expect(input).toHaveValue('new value');
```

**Testing button clicks:**
```typescript
const button = screen.getByRole('button', { name: /submit/i });
fireEvent.click(button);
```

**Testing async operations:**
```typescript
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});
```

**Testing with Router:**
```typescript
import { BrowserRouter } from 'react-router-dom';

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

renderWithRouter(<MyComponent />);
```

## Useful Query Methods

Use semantic queries (in order of preference):
- `getByRole('button', { name: /submit/i })` - Most accessible
- `getByLabelText('Username')` - For labeled inputs
- `getByPlaceholderText('Enter name')` - For placeholder text
- `getByText(/hello/i)` - For text content
- `getByTestId('custom-element')` - Last resort

All queries have variants:
- `getBy*` - Throws if not found (use for elements that should exist)
- `queryBy*` - Returns null if not found (use to check element doesn't exist)
- `findBy*` - Async, waits for element (use for async operations)
- `getAllBy*` / `queryAllBy*` / `findAllBy*` - Returns array

## Testing Best Practices

✅ **DO:**
- Test user-visible behavior, not implementation details
- Use descriptive test names
- Keep tests focused (one assertion per test is ideal)
- Use semantic queries (`getByRole`, `getByLabelText`)
- Group related tests with `describe()`
- Mock external APIs
- Test form validation
- Test error states

❌ **DON'T:**
- Query by random class names or IDs
- Test library internals
- Create expensive setup/teardown
- Over-mock dependencies
- Test React itself

## Coverage

View coverage:
```bash
npm run test:coverage
```

Coverage reports are generated in `coverage/` directory.

## Debugging Tests

### See what's rendered:
```typescript
import { render, screen } from '@testing-library/react';

render(<MyComponent />);
screen.debug(); // Prints the DOM
```

### Use `screen.logTestingPlaygroundURL()`:
```typescript
render(<MyComponent />);
screen.logTestingPlaygroundURL(); // Get interactive query suggestions
```

### Run single test:
```bash
npm test -- HomePage.test.tsx
```

### Run tests matching pattern:
```bash
npm test -- --testNamePattern="validation"
```

## Adding More Tests

1. Create a folder structure in `tests/` that mirrors `src/`
   - Example: For `src/components/Button.tsx`, create `tests/components/Button.test.tsx`
2. Import the component using relative paths: `../../src/components/Button`
3. Write your tests
4. Run `npm test` to verify

Example structure for new tests:
```
tests/
├── pages/
│   ├── HomePage.test.tsx
│   └── ResultPage.test.tsx
├── components/           ← New folder for component tests
│   └── Button.test.tsx
└── setup/
    └── setupTests.ts
```

## Next Steps

1. ✅ Basic setup complete
2. Run existing tests: `npm test`
3. Add more tests as you build features
4. Aim for >80% coverage
5. Integrate into CI/CD pipeline

## Resources

- [React Testing Library Docs](https://testing-library.com/docs/react-testing-library/intro/)
- [Jest Docs](https://jestjs.io/)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
