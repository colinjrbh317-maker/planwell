/**
 * Shared calculation utilities for federal employee retirement calculators
 * Used across FERS, High-3, Sick Leave, and Supplement calculators
 */

import type {
  SickLeaveCredit,
  SalaryPeriod,
  EligibilityResult,
  DateRangeValidation,
} from '../types/calculators';
import { findConversionEntry, SICK_LEAVE_CHART } from '../data/sick-leave-chart';

// ============================================================================
// Date Calculations
// ============================================================================

/**
 * Calculate age in years at a target date
 * @param birthDate - Date of birth
 * @param targetDate - Date to calculate age at (usually retirement date)
 * @returns Age in years
 */
export function calculateAge(birthDate: Date, targetDate: Date): number {
  let age = targetDate.getFullYear() - birthDate.getFullYear();
  const monthDiff = targetDate.getMonth() - birthDate.getMonth();

  // Adjust if birthday hasn't occurred yet this year
  if (monthDiff < 0 || (monthDiff === 0 && targetDate.getDate() < birthDate.getDate())) {
    age--;
  }

  return age;
}

/**
 * Calculate years of service between two dates
 * Rounds to nearest 0.5 years per federal calculation standards
 * @param startDate - Service start date
 * @param endDate - Service end date (usually retirement date)
 * @returns Years of service (rounded to nearest 0.5)
 */
export function calculateYearsOfService(startDate: Date, endDate: Date): number {
  const diffTime = endDate.getTime() - startDate.getTime();
  const diffDays = diffTime / (1000 * 60 * 60 * 24);
  const years = diffDays / 365.25; // Account for leap years

  // Round to nearest 0.5 years
  return Math.round(years * 2) / 2;
}

/**
 * Calculate months of service between two dates
 * Used for High-3 weighted average calculations
 * @param startDate - Period start date
 * @param endDate - Period end date
 * @returns Total months (decimal)
 */
export function calculateMonthsOfService(startDate: Date, endDate: Date): number {
  const yearDiff = endDate.getFullYear() - startDate.getFullYear();
  const monthDiff = endDate.getMonth() - startDate.getMonth();
  const dayDiff = endDate.getDate() - startDate.getDate();

  // Calculate total months including partial months
  let totalMonths = yearDiff * 12 + monthDiff;

  // Add fraction of month based on days
  if (dayDiff > 0) {
    // Approximate: assume 30 days per month for simplicity
    totalMonths += dayDiff / 30;
  }

  return totalMonths;
}

/**
 * Get the maximum of two dates
 */
export function maxDate(date1: Date, date2: Date): Date {
  return date1 > date2 ? date1 : date2;
}

/**
 * Get the minimum of two dates
 */
export function minDate(date1: Date, date2: Date): Date {
  return date1 < date2 ? date1 : date2;
}

// ============================================================================
// Sick Leave Conversion
// ============================================================================

/**
 * Convert sick leave hours to service credit (years, months, days)
 * Implements USGS conversion chart with automatic day rounding
 * @param hours - Total unused sick leave hours
 * @returns Service credit breakdown
 *
 * Critical Rules:
 * 1. 2,087 hours = 1 work year
 * 2. Days are ALWAYS rounded UP to the next full month
 * 3. Only years and months count; days under 30 are omitted
 */
export function convertSickLeave(hours: number): SickLeaveCredit {
  if (hours < 0) {
    return { years: 0, months: 0, days: 0, totalMonths: 0 };
  }

  // Handle amounts over 2,087 hours (1+ years)
  const fullYears = Math.floor(hours / 2087);
  const remainingHours = hours % 2087;

  // Look up remaining hours in conversion chart
  const chartEntry = findConversionEntry(remainingHours);

  if (!chartEntry) {
    console.warn(`No chart entry found for ${remainingHours} hours`);
    return { years: fullYears, months: 0, days: 0, totalMonths: fullYears * 12 };
  }

  let months = chartEntry.months;
  let days = chartEntry.days;

  // CRITICAL: Auto-round all days UP to next month per OPM guidelines
  // "Only years and months count - round days over 30 to months, omit anything under 30 days"
  if (days > 0) {
    months += 1;
    days = 0; // Days always become 0 after rounding up
  }

  // Calculate total years and months
  const additionalYears = Math.floor(months / 12);
  const finalMonths = months % 12;
  const totalYears = fullYears + additionalYears;

  return {
    years: totalYears,
    months: finalMonths,
    days: 0, // Always 0 after rounding
    totalMonths: fullYears * 12 + months, // Total months before year conversion
  };
}

// ============================================================================
// High-3 Salary Calculation
// ============================================================================

/**
 * Calculate High-3 average salary (highest 36 consecutive months)
 * Uses weighted average based on time in each salary period
 * @param retirementDate - Planned retirement date
 * @param periods - Array of salary periods
 * @returns Weighted average High-3 salary
 *
 * Algorithm:
 * 1. Define 36-month window ending at retirement date
 * 2. For each salary period, calculate overlap with window
 * 3. Weighted average: Sum(Salary × Months in Window) ÷ Total Months
 */
export function calculateHigh3Average(
  retirementDate: Date,
  periods: SalaryPeriod[]
): number {
  if (periods.length === 0) return 0;

  // Define 36-month window ending at retirement
  const windowEnd = retirementDate;
  const windowStart = new Date(retirementDate);
  windowStart.setMonth(windowStart.getMonth() - 36);

  let totalWeightedSalary = 0;
  let totalMonths = 0;

  periods.forEach(period => {
    // Calculate overlap between period and 36-month window
    const overlapStart = maxDate(period.startDate, windowStart);
    const overlapEnd = minDate(period.endDate, windowEnd);

    // Only include if there's actual overlap
    if (overlapStart < overlapEnd) {
      const monthsInWindow = calculateMonthsOfService(overlapStart, overlapEnd);
      totalWeightedSalary += period.salary * monthsInWindow;
      totalMonths += monthsInWindow;
    }
  });

  // Return weighted average
  return totalMonths > 0 ? totalWeightedSalary / totalMonths : 0;
}

// ============================================================================
// FERS Eligibility Validation
// ============================================================================

/**
 * Validate Normal Retirement eligibility
 * Rules:
 * - Age 57+ with 30+ years, OR
 * - Age 60+ with 20+ years, OR
 * - Age 62+ with 5+ years
 */
export function validateNormalRetirement(age: number, years: number): EligibilityResult {
  // MRA (Minimum Retirement Age) = 57 for most employees
  if (age >= 57 && years >= 30) {
    return {
      eligible: true,
      message: '✓ Eligible: Age 57+ with 30 years of service (MRA)',
    };
  }

  if (age >= 60 && years >= 20) {
    return {
      eligible: true,
      message: '✓ Eligible: Age 60+ with 20 years of service',
    };
  }

  if (age >= 62 && years >= 5) {
    return {
      eligible: true,
      message: '✓ Eligible: Age 62+ with 5 years of service',
    };
  }

  return {
    eligible: false,
    message:
      '✗ Not eligible for Normal Retirement. Requirements: Age 57+ with 30 years, OR Age 60+ with 20 years, OR Age 62+ with 5 years.',
  };
}

/**
 * Validate VERA/Early Retirement eligibility
 * Rules:
 * - 25+ years of service (any age), OR
 * - Age 50+ with 20+ years of service
 */
export function validateVERARetirement(age: number, years: number): EligibilityResult {
  if (years >= 25) {
    return {
      eligible: true,
      message: '✓ Eligible: 25+ years of service (VERA)',
    };
  }

  if (age >= 50 && years >= 20) {
    return {
      eligible: true,
      message: '✓ Eligible: Age 50+ with 20 years of service (VERA)',
    };
  }

  return {
    eligible: false,
    message:
      '✗ Not eligible for VERA/Early Retirement. Requirements: 25+ years OR Age 50+ with 20 years.',
  };
}

/**
 * Validate Special Retirement Supplement eligibility
 * Rules:
 * - Age 57+ with 30+ years, OR
 * - Age 60+ with 20+ years
 * Note: Supplement stops at age 62
 */
export function validateSupplementEligibility(age: number, years: number): EligibilityResult {
  if (age >= 62) {
    return {
      eligible: false,
      message:
        '✗ Not eligible: Special Retirement Supplement stops at age 62. You may be eligible for Social Security instead.',
    };
  }

  if (age >= 57 && years >= 30) {
    return {
      eligible: true,
      message: '✓ Eligible: Age 57+ with 30 years of service',
    };
  }

  if (age >= 60 && years >= 20) {
    return {
      eligible: true,
      message: '✓ Eligible: Age 60+ with 20 years of service',
    };
  }

  return {
    eligible: false,
    message:
      '✗ Not eligible for Special Retirement Supplement. Requirements: Age 57+ with 30 years OR Age 60+ with 20 years.',
  };
}

// ============================================================================
// Date Range Validation
// ============================================================================

/**
 * Validate that start date is before end date
 */
export function validateDateRange(startDate: Date, endDate: Date): DateRangeValidation {
  if (startDate >= endDate) {
    return {
      valid: false,
      error: 'Start date must be before end date',
    };
  }

  return { valid: true };
}

/**
 * Validate that salary periods don't overlap
 */
export function validateSalaryPeriods(periods: SalaryPeriod[]): DateRangeValidation {
  // Sort periods by start date
  const sortedPeriods = [...periods].sort(
    (a, b) => a.startDate.getTime() - b.startDate.getTime()
  );

  // Check for overlaps
  for (let i = 0; i < sortedPeriods.length - 1; i++) {
    const current = sortedPeriods[i];
    const next = sortedPeriods[i + 1];

    if (current.endDate > next.startDate) {
      return {
        valid: false,
        error: `Period ending ${current.endDate.toLocaleDateString()} overlaps with period starting ${next.startDate.toLocaleDateString()}`,
      };
    }
  }

  return { valid: true };
}

// ============================================================================
// Formatting Utilities
// ============================================================================

/**
 * Format number as US currency
 */
export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  }).format(value);
}

/**
 * Format service time as "X years, Y months"
 */
export function formatServiceTime(years: number, months?: number): string {
  if (months === undefined || months === 0) {
    return `${years} year${years !== 1 ? 's' : ''}`;
  }

  const yearText = years > 0 ? `${years} year${years !== 1 ? 's' : ''}` : '';
  const monthText = `${months} month${months !== 1 ? 's' : ''}`;

  if (years === 0) return monthText;
  return `${yearText}, ${monthText}`;
}

/**
 * Parse currency string to number
 */
export function parseCurrency(value: string): number {
  // Remove currency symbols, commas, and whitespace
  const cleaned = value.replace(/[$,\s]/g, '');
  const parsed = parseFloat(cleaned);
  return isNaN(parsed) ? 0 : parsed;
}

/**
 * Format percentage
 */
export function formatPercentage(value: number, decimals: number = 1): string {
  return `${(value * 100).toFixed(decimals)}%`;
}
