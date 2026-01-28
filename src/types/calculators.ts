/**
 * TypeScript interfaces for federal employee retirement calculators
 * Used across FERS, High-3, Sick Leave, and Supplement calculators
 */

// ============================================================================
// FERS Pension Calculator Types
// ============================================================================

export interface FERSCalculatorData {
  retirementType: 'normal' | 'vera';
  high3: number;
  birthDate: string; // ISO date string
  scd: string; // Service Calculation Date - ISO date string
  retirementDate: string; // ISO date string
  sickLeaveHours: number;
  militaryYears: number;
  militaryMonths: number;
}

export interface FERSResult {
  annualPension: number;
  monthlyPension: number;
  multiplier: number;
  age: number;
  totalYearsOfService: number;
  eligible: boolean;
  eligibilityMessage: string;
}

// ============================================================================
// High-3 Salary Calculator Types
// ============================================================================

export interface SalaryPeriod {
  startDate: Date;
  endDate: Date;
  salary: number;
}

export interface High3CalculatorData {
  retirementDate: string; // ISO date string
  periods: Array<{
    startDate: string;
    endDate: string;
    salary: number;
  }>;
  calculatedHigh3: number;
}

export interface High3Result {
  high3Average: number;
  periodsUsed: number;
  totalMonthsAnalyzed: number;
  breakdown: Array<{
    period: {
      startDate: string;
      endDate: string;
      salary: number;
    };
    monthsInWindow: number;
    contribution: number;
  }>;
}

// ============================================================================
// Sick Leave Conversion Calculator Types
// ============================================================================

export interface SickLeaveCredit {
  years: number;
  months: number;
  days: number;
  totalMonths: number; // Total months for pension calculations
}

export interface SickLeaveData {
  hours: number;
  converted: SickLeaveCredit;
}

export interface SickLeaveChartEntry {
  minHours: number;
  maxHours: number;
  months: number;
  days: number;
}

// ============================================================================
// Special Retirement Supplement Calculator Types
// ============================================================================

export interface SupplementData {
  retirementDate: string; // ISO date string
  serviceDate: string; // ISO date string
  ssEstimate: number; // Social Security estimate at age 62
  monthlyAmount: number;
  annualAmount: number;
}

export interface SupplementResult {
  monthlyAmount: number;
  annualAmount: number;
  yearsOfService: number;
  eligible: boolean;
  eligibilityMessage: string;
}

// ============================================================================
// Cross-Calculator Storage (for Phase 2)
// ============================================================================

export interface CalculatorStorage {
  fers?: FERSCalculatorData;
  high3?: High3CalculatorData;
  sickLeave?: SickLeaveData;
  supplement?: SupplementData;
  lastUpdated?: string;
}

// ============================================================================
// Validation Types
// ============================================================================

export interface ValidationResult {
  valid: boolean;
  message?: string;
  errors?: string[];
}

export interface EligibilityResult {
  eligible: boolean;
  message: string;
}

// ============================================================================
// Date Range Validation
// ============================================================================

export interface DateRangeValidation {
  valid: boolean;
  error?: string;
}
