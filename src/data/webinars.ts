/**
 * Webinar Schedule Configuration
 * Update this file when scheduling new webinars
 * The system will automatically display the next upcoming session
 */

export interface Webinar {
    id: string;
    date: Date;
    title: string;
    startTime: string;
    endTime: string;
    timezone: string;
    zoomLink?: string;
}

// All scheduled webinars - add new dates here
export const webinars: Webinar[] = [
    {
        id: 'feb-06-2026',
        date: new Date('2026-02-06T11:00:00-05:00'),
        title: 'FERS Retirement Workshop',
        startTime: '11:00 AM',
        endTime: '2:00 PM',
        timezone: 'EST',
        zoomLink: 'https://us06web.zoom.us/webinar/register/WN_8BewKDfGTHGQjil5--I0Wg',
    },
    {
        id: 'feb-27-2026',
        date: new Date('2026-02-27T11:00:00-05:00'),
        title: 'FERS Retirement Workshop',
        startTime: '11:00 AM',
        endTime: '2:00 PM',
        timezone: 'EST',
        zoomLink: 'https://us06web.zoom.us/webinar/register/WN_AgC4CznVT6O_CnRWL99vtg',
    },
    {
        id: 'mar-20-2026',
        date: new Date('2026-03-20T11:00:00-04:00'),
        title: 'FERS Retirement Workshop',
        startTime: '11:00 AM',
        endTime: '2:00 PM',
        timezone: 'EDT',
        zoomLink: 'https://us06web.zoom.us/webinar/register/WN_NItY3v8yQtyfwjYzNWn3TA',
    },
    {
        id: 'apr-10-2026',
        date: new Date('2026-04-10T11:00:00-04:00'),
        title: 'FERS Retirement Workshop',
        startTime: '11:00 AM',
        endTime: '2:00 PM',
        timezone: 'EDT',
        zoomLink: 'https://us06web.zoom.us/webinar/register/WN_wQtHJWYZTWy8GDUdz0gFtg',
    },
    {
        id: 'may-01-2026',
        date: new Date('2026-05-01T11:00:00-04:00'),
        title: 'FERS Retirement Workshop',
        startTime: '11:00 AM',
        endTime: '2:00 PM',
        timezone: 'EDT',
        zoomLink: 'https://us06web.zoom.us/webinar/register/WN_sOVCAOVPSHCI-B1OJCvqeA',
    },
    {
        id: 'may-22-2026',
        date: new Date('2026-05-22T11:00:00-04:00'),
        title: 'FERS Retirement Workshop',
        startTime: '11:00 AM',
        endTime: '2:00 PM',
        timezone: 'EDT',
        zoomLink: 'https://us06web.zoom.us/webinar/register/WN_FwNEY1MrSsOHRCldaC1-pw',
    },
    {
        id: 'jun-12-2026',
        date: new Date('2026-06-12T11:00:00-04:00'),
        title: 'FERS Retirement Workshop',
        startTime: '11:00 AM',
        endTime: '2:00 PM',
        timezone: 'EDT',
        zoomLink: 'https://us06web.zoom.us/webinar/register/WN_vFS6fCRNQZKUn5qpYTG1jw',
    },
    {
        id: 'jul-03-2026',
        date: new Date('2026-07-03T11:00:00-04:00'),
        title: 'FERS Retirement Workshop',
        startTime: '11:00 AM',
        endTime: '2:00 PM',
        timezone: 'EDT',
        zoomLink: 'https://us06web.zoom.us/webinar/register/WN_u4UdZlAfSwatECiAqmxwbA',
    },

];

/**
 * Get the next upcoming webinar (first one after current time)
 */
export function getNextWebinar(): Webinar | null {
    const now = new Date();
    const upcoming = webinars
        .filter(w => w.date > now)
        .sort((a, b) => a.date.getTime() - b.date.getTime());
    return upcoming[0] || null;
}

/**
 * Get multiple upcoming webinars
 */
export function getUpcomingWebinars(count: number = 3): Webinar[] {
    const now = new Date();
    return webinars
        .filter(w => w.date > now)
        .sort((a, b) => a.date.getTime() - b.date.getTime())
        .slice(0, count);
}

/**
 * Format webinar date in human-readable format
 */
export function formatWebinarDate(webinar: Webinar): string {
    const options: Intl.DateTimeFormatOptions = {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
    };
    return webinar.date.toLocaleDateString('en-US', options);
}

/**
 * Get days until webinar
 */
export function getDaysUntil(webinar: Webinar): number {
    const now = new Date();
    const diff = webinar.date.getTime() - now.getTime();
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

/**
 * Get all webinars (newest first) — for event listing pages and sitemaps
 */
export function getAllWebinars(): Webinar[] {
    return [...webinars].sort((a, b) => b.date.getTime() - a.date.getTime());
}

/**
 * Find a specific webinar by ID — for individual event pages
 */
export function getWebinarById(id: string): Webinar | null {
    return webinars.find(w => w.id === id) || null;
}

/**
 * Check if a webinar date has passed
 */
export function isPastWebinar(webinar: Webinar): boolean {
    return webinar.date < new Date();
}

/**
 * Generate ICS calendar content for a webinar
 */
export function generateICS(webinar: Webinar): string {
    const startDate = webinar.date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    const endDate = new Date(webinar.date.getTime() + 3 * 60 * 60 * 1000) // 3 hours later
        .toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';

    return `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//PlanWell//Webinar//EN
BEGIN:VEVENT
UID:${webinar.id}@planwellfp.com
DTSTAMP:${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}Z
DTSTART:${startDate}
DTEND:${endDate}
SUMMARY:${webinar.title} - PlanWell Financial Planning
DESCRIPTION:Free 3-hour FERS retirement workshop covering pension, TSP, FEHB, Medicare, and survivor benefits.\\n\\nHosted by Certified Financial Planners who specialize in federal benefits.
LOCATION:Online (Zoom link will be emailed)
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR`;
}
