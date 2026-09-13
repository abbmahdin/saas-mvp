import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Chat from '@/components/Chat';

// Mock fetch globally
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('Chat Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockFetch.mockReset();
  });

  it('renders chat component with welcome message', () => {
    render(<Chat />);
    expect(screen.getByText('Hello! How can I help you today?')).toBeInTheDocument();
  });

  it('renders input and send button', () => {
    render(<Chat />);
    expect(screen.getByPlaceholderText('Type a message...')).toBeInTheDocument();
    expect(screen.getByText('Send')).toBeInTheDocument();
  });

  it('updates input value when typing', () => {
    render(<Chat />);
    const input = screen.getByPlaceholderText('Type a message...');
    fireEvent.change(input, { target: { value: 'Hello AI' } });
    expect(input).toHaveValue('Hello AI');
  });

  it('disables send button when input is empty', () => {
    render(<Chat />);
    expect(screen.getByText('Send')).toBeDisabled();
  });

  it('enables send button when input has text', () => {
    render(<Chat />);
    const input = screen.getByPlaceholderText('Type a message...');
    fireEvent.change(input, { target: { value: 'Test' } });
    expect(screen.getByText('Send')).toBeEnabled();
  });

  it('sends message and displays response', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ content: 'AI response here' }),
    });

    render(<Chat />);
    const input = screen.getByPlaceholderText('Type a message...');
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(screen.getByText('Send'));

    await waitFor(() => {
      expect(screen.getByText('AI response here')).toBeInTheDocument();
    });
  });

  it('shows loading state while sending', async () => {
    let resolvePromise: (value: any) => void;
    mockFetch.mockImplementationOnce(
      () => new Promise((resolve) => { resolvePromise = resolve; })
    );

    render(<Chat />);
    const input = screen.getByPlaceholderText('Type a message...');
    fireEvent.change(input, { target: { value: 'Test' } });
    fireEvent.click(screen.getByText('Send'));

    await waitFor(() => {
      expect(screen.getByText('Typing...')).toBeInTheDocument();
    });

    resolvePromise!({ ok: true, json: async () => ({ content: 'Response' }) });
  });
});