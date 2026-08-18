/**
 * FEHB Open Season Webinar Schedule Configuration
 * Federal Employees Health Benefits (FEHB) Open Season sessions.
 *
 * Requested by Brennan Rhule 2026-08-07: the page exists primarily for SEO —
 * PlanWell does not advertise these, and has historically ranked #1 for
 * searches like "FEHB Open Season webinar". Traffic comes from search, so the
 * page must carry real, indexable content, not just a registration button.
 *
 * ⛔ EVERY ENTRY NEEDS A REAL `date` AND A REAL `zoomLink`.
 * A registration page that renders without a date is the exact failure that
 * killed the TSP funnel: src/data/tsp-webinars.ts ran dry on 2026-03-27 and
 * /webinar/tsp then served HTTP 200, a live "Reserve My Free Seat" button, and
 * no date anywhere, for 142 days. Nothing errored and nothing alarmed, because
 * scripts/check_webinar_runway.py only ever parsed webinars.ts.
 * ⇒ WHEN ADDING A DATE HERE, ALSO ADD THIS FILE TO THAT GUARD. A funnel nobody
 *   watches is a funnel that dies quietly.
 */

export interface FehbWebinar {
    id: string;
    date: Date;
    title: string;
    startTime: string;
    endTime: string;
    timezone: string;
    host: string;
    /** Zoom REGISTRATION url (not the join url — that is per-registrant). */
    zoomLink: string;
    /** Zoom webinar id, for scripts/sync_webinar.py style registrant sync. */
    zoomId: string;
}

// All scheduled FEHB webinars - add new dates here.
export const fehbWebinars: FehbWebinar[] = [
    {
        id: 'nov-11-2026',
        // 2026-11-11T19:30:00Z. US DST ends 2026-11-01, so this date is EST (UTC-5).
        // Verified against the Zoom record 2026-08-16: start_time 2026-11-11T19:30:00Z,
        // duration 120min, timezone America/New_York, topic "2027 FEHB Open Season Webinar".
        date: new Date('2026-11-11T14:30:00-05:00'),
        title: '2027 FEHB Open Season Webinar',
        startTime: '2:30 PM',
        endTime: '4:30 PM',
        timezone: 'EST',
        host: 'Brennan Rhule, CFP®, ChFEBC℠, AIF®',
        zoomLink: 'https://us06web.zoom.us/webinar/register/WN_G5xPNyMbTkKVRW_0RpDn7w',
        zoomId: '85418313825',
    },
];

/** The next upcoming FEHB webinar, or null when none is scheduled. */
export function getNextFEHBWebinar(): FehbWebinar | null {
    const now = new Date();
    const upcoming = fehbWebinars
        .filter(w => w.date > now)
        .sort((a, b) => a.date.getTime() - b.date.getTime());
    return upcoming[0] || null;
}

/** Upcoming FEHB webinars, soonest first. */
export function getUpcomingFEHBWebinars(count: number = 3): FehbWebinar[] {
    const now = new Date();
    return fehbWebinars
        .filter(w => w.date > now)
        .sort((a, b) => a.date.getTime() - b.date.getTime())
        .slice(0, count);
}

/** e.g. "Wednesday, November 11" */
export function formatFEHBWebinarDate(webinar: FehbWebinar): string {
    return webinar.date.toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        timeZone: 'America/New_York',
    });
}

/** e.g. "Wednesday, November 11, 2026 · 2:30 PM – 4:30 PM EST" */
export function formatFEHBWebinarDateTime(webinar: FehbWebinar): string {
    const d = webinar.date.toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric',
        timeZone: 'America/New_York',
    });
    return `${d} · ${webinar.startTime} – ${webinar.endTime} ${webinar.timezone}`;
}

export function getDaysUntilFEHB(webinar: FehbWebinar): number {
    return Math.ceil((webinar.date.getTime() - Date.now()) / (1000 * 60 * 60 * 24));
}

export function isPastFEHBWebinar(webinar: FehbWebinar): boolean {
    return webinar.date < new Date();
}

export function getFEHBWebinarById(id: string): FehbWebinar | null {
    return fehbWebinars.find(w => w.id === id) || null;
}

/** ICS calendar entry. Duration is derived from the entry, never hardcoded. */
export function generateFEHBICS(webinar: FehbWebinar): string {
    const stamp = (d: Date) => d.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    const parseClock = (t: string) => {
        const m = t.match(/(\d+):(\d+)\s*(AM|PM)/i);
        if (!m) return 0;
        let h = parseInt(m[1], 10) % 12;
        if (/PM/i.test(m[3])) h += 12;
        return h * 60 + parseInt(m[2], 10);
    };
    const mins = parseClock(webinar.endTime) - parseClock(webinar.startTime);
    const end = new Date(webinar.date.getTime() + mins * 60 * 1000);

    return `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//PlanWell//FEHB Webinar//EN
BEGIN:VEVENT
UID:${webinar.id}@planwellfp.com
DTSTAMP:${stamp(new Date())}
DTSTART:${stamp(webinar.date)}
DTEND:${stamp(end)}
SUMMARY:${webinar.title} - PlanWell
DESCRIPTION:FEHB Open Season webinar for federal employees and retirees. Plan comparison, Medicare coordination, and what changes for the new plan year.\\n\\nHosted by ${webinar.host}
LOCATION:Online (Zoom link will be emailed on registration)
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR`;
}
