// Form submission handler
// Configure your webhook URLs here or use environment variables

export interface FormSubmission {
    type: 'contact' | 'webinar';
    data: Record<string, string>;
    timestamp: string;
}

// Webhook configuration
// For n8n: Create a webhook node and paste the URL here
// For other services: Use their webhook URL
export const WEBHOOK_CONFIG = {
    contact: import.meta.env.PUBLIC_CONTACT_WEBHOOK_URL || 'https://your-n8n-instance.com/webhook/contact',
    webinar: import.meta.env.PUBLIC_WEBINAR_WEBHOOK_URL || 'https://your-n8n-instance.com/webhook/webinar',
};

// Email notification recipients (for backup/logging)
export const NOTIFICATION_EMAILS = {
    contact: ['david.fei@planwellfp.com', 'brennan.rhule@planwellfp.com'],
    webinar: ['david.fei@planwellfp.com', 'brennan.rhule@planwellfp.com'],
};

/**
 * Submit form data to webhook
 * Returns true on success, false on failure
 */
export async function submitToWebhook(
    type: 'contact' | 'webinar',
    data: Record<string, string>
): Promise<{ success: boolean; error?: string }> {
    const webhookUrl = WEBHOOK_CONFIG[type];

    const submission: FormSubmission = {
        type,
        data,
        timestamp: new Date().toISOString(),
    };

    try {
        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(submission),
        });

        if (!response.ok) {
            console.error(`Webhook submission failed: ${response.status}`);
            return { success: false, error: `HTTP ${response.status}` };
        }

        return { success: true };
    } catch (error) {
        console.error('Webhook submission error:', error);
        return {
            success: false,
            error: error instanceof Error ? error.message : 'Network error'
        };
    }
}

/**
 * Fallback: Log to console (useful during development)
 */
export function logSubmission(type: string, data: Record<string, string>): void {
    console.log(`[${new Date().toISOString()}] New ${type} submission:`, data);
}
