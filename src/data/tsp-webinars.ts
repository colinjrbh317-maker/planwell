/**
 * TSP Webinar Schedule Configuration
 * 1-hour tactical TSP training sessions hosted by David Fei
 */

export interface Webinar {
    id: string;
    date: Date;
    title: string;
    startTime: string;
    endTime: string;
    timezone: string;
    host: string;
    zoomLink?: string;
}

// All scheduled TSP webinars - add new dates here
export const tspWebinars: Webinar[] = [
    {
        id: 'jan-23-2026',
        date: new Date('2026-01-23T12:00:00-05:00'),
        title: 'TSP Investment Strategies',
        startTime: '12:00 PM',
        endTime: '1:00 PM',
        timezone: 'EST',
        host: 'David Fei, CFP®, ChFEBC℠'
    },
    {
        id: 'feb-20-2026',
        date: new Date('2026-02-20T12:00:00-05:00'),
        title: 'TSP Investment Strategies',
        startTime: '12:00 PM',
        endTime: '1:00 PM',
        timezone: 'EST',
        host: 'David Fei, CFP®, ChFEBC℠'
    },
    {
        id: 'mar-27-2026',
        date: new Date('2026-03-27T12:00:00-04:00'), // EDT
        title: 'TSP Investment Strategies',
        startTime: '12:00 PM',
        endTime: '1:00 PM',
        timezone: 'EDT',
        host: 'David Fei, CFP®, ChFEBC℠'
    },
];

/**
 * Get the next upcoming TSP webinar
 */
export function getNextTSPWebinar(): Webinar | null {
    const now = new Date();
    const upcoming = tspWebinars
        .filter(w => w.date > now)
        .sort((a, b) => a.date.getTime() - b.date.getTime());
    return upcoming[0] || null;
}

/**
 * Get multiple upcoming TSP webinars
 */
export function getUpcomingTSPWebinars(count: number = 3): Webinar[] {
    const now = new Date();
    return tspWebinars
        .filter(w => w.date > now)
        .sort((a, b) => a.date.getTime() - b.date.getTime())
        .slice(0, count);
}

/**
 * Format TSP webinar date in human-readable format
 */
export function formatTSPWebinarDate(webinar: Webinar): string {
    const options: Intl.DateTimeFormatOptions = {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
    };
    return webinar.date.toLocaleDateString('en-US', options);
}

/**
 * Get days until TSP webinar
 */
export function getDaysUntilTSP(webinar: Webinar): number {
    const now = new Date();
    const diff = webinar.date.getTime() - now.getTime();
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

/**
 * Generate ICS calendar content for TSP webinar
 */
export function generateTSPICS(webinar: Webinar): string {
    const startDate = webinar.date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    const endDate = new Date(webinar.date.getTime() + 1 * 60 * 60 * 1000) // 1 hour later
        .toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';

    return `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//PlanWell//TSP Webinar//EN
BEGIN:VEVENT
UID:${webinar.id}@planwellfp.com
DTSTAMP:${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}Z
DTSTART:${startDate}
DTEND:${endDate}
SUMMARY:${webinar.title} - PlanWell TSP Webinar
DESCRIPTION:1-hour TSP training covering investment strategies, fund allocation, and withdrawal planning.\\n\\nHosted by ${webinar.host}\\n\\nTopics: Traditional vs Roth TSP, C/S/I/F/G funds, withdrawal strategies, and live Q&A.
LOCATION:Online (Zoom link will be emailed)
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR`;
}
