/**
 * Indian localized formatting utilities for FRAUD-X.
 * Adheres strictly to Indian numbering system (Lakhs / Crores) and INR (₹).
 */

export function formatINR(amount: number | null | undefined, includeDecimals: boolean = false): string {
  if (amount === null || amount === undefined || isNaN(amount)) {
    return '₹0';
  }

  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: includeDecimals ? 2 : 0,
    maximumFractionDigits: 2,
  }).format(amount);
}

export const formatCurrency = formatINR;

export function formatNumberIN(val: number | null | undefined): string {
  if (val === null || val === undefined || isNaN(val)) {
    return '0';
  }
  return new Intl.NumberFormat('en-IN').format(val);
}

export function formatIndianDate(isoString: string): string {
  try {
    const d = new Date(isoString);
    return d.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  } catch {
    return isoString;
  }
}

export function formatIndianDateTime(isoString: string): string {
  try {
    const d = new Date(isoString);
    return `${d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short' })} ${d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })} IST`;
  } catch {
    return isoString;
  }
}
