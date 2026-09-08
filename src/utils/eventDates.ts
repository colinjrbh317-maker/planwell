/**
 * Timezone-aware ISO strings for schema.org Event markup.
 *
 * Date.toISOString() always emits UTC ("...T15:00:00.000Z"). Google accepts
 * that, but an explicit Eastern offset ("...T11:00:00-04:00") reads as the
 * advertised local time in Rich Results and never drifts if someone edits a
 * data entry without touching the ISO output.
 */

const OFFSETS: Record<string, string> = {
    EST: '-05:00',
    EDT: '-04:00',
    ET: '-05:00',
};

const OFFSET_MINUTES: Record<string, number> = {
    '-05:00': -300,
    '-04:00': -240,
};

/** Format a Date as ISO 8601 with the given Eastern timezone label (EST or EDT). */
export function toEasternISO(date: Date, timezone: string): string {
    const offset = OFFSETS[timezone] || '-05:00';
    const shifted = new Date(date.getTime() + OFFSET_MINUTES[offset] * 60 * 1000);
    return shifted.toISOString().replace(/\.\d{3}Z$/, '') + offset;
}

/** Whole days from now until the date, never negative. */
export function daysUntil(date: Date): number {
    return Math.max(0, Math.ceil((date.getTime() - Date.now()) / (1000 * 60 * 60 * 24)));
}
