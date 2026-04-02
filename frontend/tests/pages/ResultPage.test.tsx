import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ResultPage from '../../src/pages/ResultPage';

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('ResultPage', () => {
  it('shows no analysis data message when location state is empty', () => {
    renderWithRouter(<ResultPage />);
    expect(screen.getByText(/no analysis data found/i)).toBeInTheDocument();
    expect(screen.getByText(/go back to home page/i)).toBeInTheDocument();
  });

  it('renders back button link', () => {
    renderWithRouter(<ResultPage />);
    const backButton = screen.getByText(/go back to home page/i);
    expect(backButton).toBeInTheDocument();
  });

  it('back button is clickable', () => {
    renderWithRouter(<ResultPage />);
    const backButton = screen.getByRole('button', { name: /go back/i });
    expect(backButton).toBeInTheDocument();
  });
});

// Note: Full data rendering tests would require router state setup via navigation
// These are tested via component integration or E2E tests
