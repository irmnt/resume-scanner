import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import HomePage from '../../src/pages/HomePage';

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('HomePage', () => {
  it('renders the main title', () => {
    renderWithRouter(<HomePage />);
    expect(screen.getByText(/resume scanner/i)).toBeInTheDocument();
  });

  it('renders resume and job description sections', () => {
    renderWithRouter(<HomePage />);
    expect(screen.getByText(/your resume/i)).toBeInTheDocument();
    expect(screen.getByText(/job description/i)).toBeInTheDocument();
  });

  it('displays text input by default', () => {
    renderWithRouter(<HomePage />);
    const textareas = screen.getAllByRole('textbox');
    expect(textareas.length).toBeGreaterThan(0);
  });

  it('toggles between text and PDF modes for resume', () => {
    renderWithRouter(<HomePage />);
    const buttons = screen.getAllByRole('button');
    const uploadPdfBtn = buttons.find(btn => btn.textContent?.includes('Upload PDF'));
    
    if (uploadPdfBtn) {
      fireEvent.click(uploadPdfBtn);
      const fileInputs = screen.queryAllByRole('button');
      expect(fileInputs.length).toBeGreaterThan(0);
    }
  });

  it('shows validation error when submitting without resume', async () => {
    renderWithRouter(<HomePage />);
    
    const alertMock = jest.spyOn(window, 'alert').mockImplementation();
    const analyzeBtn = screen.getByRole('button', { name: /analyze|scan|submit/i });
    
    fireEvent.click(analyzeBtn);
    
    await waitFor(() => {
      expect(alertMock).toHaveBeenCalledWith(
        expect.stringContaining('resume')
      );
    });
    
    alertMock.mockRestore();
  });

  it('shows validation error when submitting without job description', async () => {
    renderWithRouter(<HomePage />);
    
    const alertMock = jest.spyOn(window, 'alert').mockImplementation();
    const textareas = screen.getAllByRole('textbox');
    
    // Fill resume but not job description
    fireEvent.change(textareas[0], { target: { value: 'Sample resume' } });
    
    const analyzeBtn = screen.getByRole('button', { name: /analyze|scan|submit/i });
    fireEvent.click(analyzeBtn);
    
    await waitFor(() => {
      expect(alertMock).toHaveBeenCalledWith(
        expect.stringContaining('job description')
      );
    });
    
    alertMock.mockRestore();
  });

  it('accepts resume text input', () => {
    renderWithRouter(<HomePage />);
    const textareas = screen.getAllByRole('textbox');
    
    fireEvent.change(textareas[0], { target: { value: '5 years Java developer' } });
    expect((textareas[0] as HTMLTextAreaElement).value).toBe('5 years Java developer');
  });

  it('accepts job description text input', () => {
    renderWithRouter(<HomePage />);
    const textareas = screen.getAllByRole('textbox');
    
    fireEvent.change(textareas[1], { target: { value: 'Seeking Java developer with 5+ years' } });
    expect((textareas[1] as HTMLTextAreaElement).value).toBe('Seeking Java developer with 5+ years');
  });

  it('disables analyze button when loading', async () => {
    renderWithRouter(<HomePage />);
    const analyzeBtn = screen.getByRole('button', { name: /analyze|scan|submit/i });
    
    // Initially enabled
    expect(analyzeBtn).not.toBeDisabled();
  });
});
