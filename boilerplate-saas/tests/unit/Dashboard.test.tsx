import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Dashboard from '@/components/Dashboard';

describe('Dashboard Component', () => {
  it('renders dashboard title', () => {
    render(<Dashboard />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });

  it('displays all stat cards', () => {
    render(<Dashboard />);
    expect(screen.getByText('Total Users')).toBeInTheDocument();
    expect(screen.getByText('Active Subscriptions')).toBeInTheDocument();
    expect(screen.getByText('Monthly Revenue')).toBeInTheDocument();
    expect(screen.getByText('API Calls')).toBeInTheDocument();
  });

  it('shows stat values', () => {
    render(<Dashboard />);
    expect(screen.getByText('1,234')).toBeInTheDocument();
    expect(screen.getByText('89')).toBeInTheDocument();
    expect(screen.getByText('$12,450')).toBeInTheDocument();
    expect(screen.getByText('52,000')).toBeInTheDocument();
  });

  it('displays trend indicators', () => {
    render(<Dashboard />);
    expect(screen.getByText('+12%')).toBeInTheDocument();
    expect(screen.getByText('+5%')).toBeInTheDocument();
    expect(screen.getByText('+18%')).toBeInTheDocument();
    expect(screen.getByText('-2%')).toBeInTheDocument();
  });
});