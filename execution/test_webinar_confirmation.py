"""
Unit tests for the webinar confirmation path: calendar file, signed links,
the confirmation email content, and the Mailchimp "recipients not ready" retry.

Run:  cd execution && python -m unittest test_webinar_confirmation -v
No network access is used; Mailchimp and the email send are mocked.
Needs execution/requirements.txt installed (the endpoint test imports webhook_server).
"""

import os
import unittest
from datetime import datetime, timezone
from unittest import mock
from urllib.parse import urlparse, parse_qs

os.environ.setdefault('ZOOM_CLIENT_SECRET', 'unit-test-secret')

import webinar_calendar as wc  # noqa: E402

JOIN = 'https://us06web.zoom.us/w/88664320406?tk=abc123DEF.xyz&uuid=WN_B7jROJ2URo'
OCT16 = datetime(2026, 10, 16, 15, 0, tzinfo=timezone.utc)   # 11:00 EDT
NOV06 = datetime(2026, 11, 6, 16, 0, tzinfo=timezone.utc)    # 11:00 EST


def _unfold(ics):
    return ics.replace('\r\n ', '')


class CalendarFileTests(unittest.TestCase):

    def test_new_york_conversion_handles_dst(self):
        self.assertEqual(wc.to_new_york(OCT16), datetime(2026, 10, 16, 11, 0))
        self.assertEqual(wc.to_new_york(NOV06), datetime(2026, 11, 6, 11, 0))
        # Around the November switch (Nov 1 2026, 06:00Z)
        self.assertEqual(wc.to_new_york(datetime(2026, 11, 1, 5, 59, tzinfo=timezone.utc)).hour, 1)
        self.assertEqual(wc.to_new_york(datetime(2026, 11, 1, 6, 0, tzinfo=timezone.utc)).hour, 1)
        # March switch (Mar 8 2026, 07:00Z)
        self.assertEqual(wc.to_new_york(datetime(2026, 3, 8, 6, 59, tzinfo=timezone.utc)).hour, 1)
        self.assertEqual(wc.to_new_york(datetime(2026, 3, 8, 7, 0, tzinfo=timezone.utc)).hour, 3)

    def test_ics_contents(self):
        ics = wc.build_ics('fers', OCT16, JOIN, '057007')
        flat = _unfold(ics)
        self.assertTrue(ics.startswith('BEGIN:VCALENDAR\r\n'))
        self.assertTrue(ics.endswith('END:VCALENDAR\r\n'))
        self.assertIn('METHOD:PUBLISH', flat)
        self.assertIn('DTSTART;TZID=America/New_York:20261016T110000', flat)
        self.assertIn('DTEND;TZID=America/New_York:20261016T140000', flat)
        self.assertIn('BEGIN:VTIMEZONE', flat)
        self.assertIn('LOCATION:' + JOIN, flat)
        self.assertIn('URL:' + JOIN, flat)
        self.assertIn(JOIN, flat.split('DESCRIPTION:', 1)[1])
        self.assertIn('057007', flat)
        self.assertNotIn('ORGANIZER', flat)   # PUBLISH, not a meeting request

    def test_ics_winter_session(self):
        flat = _unfold(wc.build_ics('fers', NOV06, JOIN))
        self.assertIn('DTSTART;TZID=America/New_York:20261106T110000', flat)

    def test_ics_lines_are_folded(self):
        ics = wc.build_ics('fers', OCT16, JOIN + '&pad=' + 'x' * 200, '057007')
        for line in ics.split('\r\n'):
            self.assertLessEqual(len(line.encode('utf-8')), 75, line)

    def test_ics_without_join_link(self):
        flat = _unfold(wc.build_ics('fers', OCT16, ''))
        self.assertIn('LOCATION:Online via Zoom', flat)
        self.assertNotIn('URL:', flat)

    def test_uid_stable_per_registrant(self):
        a = wc.build_ics('fers', OCT16, JOIN)
        b = wc.build_ics('fers', OCT16, JOIN)
        c = wc.build_ics('fers', OCT16, JOIN + 'other')
        uid = lambda x: [l for l in x.split('\r\n') if l.startswith('UID:')][0]
        self.assertEqual(uid(a), uid(b))
        self.assertNotEqual(uid(a), uid(c))


class SignedLinkTests(unittest.TestCase):

    def test_link_round_trip_and_tamper(self):
        url = wc.ics_link('fers', OCT16, JOIN, '057007')
        q = {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}
        self.assertEqual(q['j'], JOIN)
        self.assertEqual(q['s'], '20261016T150000Z')
        self.assertTrue(wc.verify(q['t'], q['s'], q['j'], q.get('p', ''), q['sig']))
        self.assertFalse(wc.verify(q['t'], q['s'], 'https://evil.example/', q.get('p', ''), q['sig']))
        self.assertFalse(wc.verify(q['t'], q['s'], q['j'], q.get('p', ''), ''))
        self.assertEqual(wc.parse_start(q['s']), OCT16)

    def test_parse_start_formats(self):
        self.assertEqual(wc.parse_start('2026-10-16T15:00:00.000Z'), OCT16)
        self.assertEqual(wc.parse_start('2026-10-16T11:00:00-04:00'), OCT16)
        with self.assertRaises(ValueError):
            wc.parse_start('2026-10-16T11:00:00')

    def test_google_and_outlook_links_carry_join_url(self):
        from urllib.parse import unquote
        self.assertIn(JOIN, unquote(wc.google_link('fers', OCT16, JOIN)))
        o = wc.outlook_web_link('fers', OCT16, JOIN)
        self.assertTrue(o.startswith('https://outlook.office.com/calendar/0/deeplink/compose?'))
        self.assertIn('startdt=2026-10-16T15%3A00%3A00Z', o)
        self.assertIn(JOIN, unquote(o))


class EndpointTests(unittest.TestCase):

    def setUp(self):
        import webhook_server
        self.client = webhook_server.app.test_client()

    def test_serves_signed_ics(self):
        url = wc.ics_link('fers', OCT16, JOIN, '057007')
        path = url[url.index('/api/'):]
        r = self.client.get(path)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.headers['Content-Type'].startswith('text/calendar'))
        self.assertIn('attachment', r.headers['Content-Disposition'])
        self.assertIn('.ics', r.headers['Content-Disposition'])
        self.assertIn('METHOD:PUBLISH', r.get_data(as_text=True))

    def test_rejects_unsigned(self):
        r = self.client.get('/api/webinar/calendar.ics?t=fers&s=20261016T150000Z&j=https://evil.example')
        self.assertEqual(r.status_code, 400)


class ConfirmationEmailTests(unittest.TestCase):

    def _render(self, **kw):
        import webinar_emails
        with mock.patch.object(webinar_emails, 'send_email', return_value=True) as m:
            ok = webinar_emails.send_webinar_confirmation(
                'test@example.com', 'Pat', 'Friday, October 16', 'ET', **kw)
        self.assertTrue(ok)
        args, kwargs = m.call_args
        return args[2], args[3], kwargs

    def test_join_link_and_calendar_options(self):
        links = wc.calendar_links('fers', OCT16, JOIN, '057007')
        plain, html, kwargs = self._render(
            calendar_link=links['google'], zoom_link=JOIN, ics_link=links['ics'],
            outlook_link=links['outlook_web'], passcode='057007', retry_delays=(1, 2))
        self.assertIn(JOIN, plain)
        self.assertIn('href="' + JOIN + '"', html)
        self.assertIn('Join the Workshop on Zoom', html)
        self.assertIn('href="' + links['ics'] + '"', html)
        self.assertIn('Add to Outlook / Apple Calendar', html)
        self.assertIn('Google Calendar', html)
        self.assertIn('Outlook on the web', html)
        self.assertIn('057007', html)
        self.assertIn('11:00 AM &ndash; 2:00 PM ET', html)
        self.assertEqual(kwargs.get('mailchimp_retry_delays'), (1, 2))
        # The join button comes before the calendar button.
        self.assertLess(html.index('Join the Workshop on Zoom'),
                        html.index('Add to Outlook / Apple Calendar'))

    def test_without_join_link(self):
        plain, html, _ = self._render(calendar_link='https://calendar.google.com/x')
        self.assertIn('arrive the day before', plain)
        self.assertIn('Add to Calendar', html)
        self.assertNotIn('Join the Workshop on Zoom', html)


class MailchimpRetryTests(unittest.TestCase):

    def _resp(self, code, text=''):
        r = mock.Mock()
        r.status_code = code
        r.text = text
        r.json.return_value = {'id': 'camp1'}
        return r

    def test_retries_until_recipients_ready(self):
        import mailchimp_client as mc
        not_ready = self._resp(400, '{"detail":"Your Campaign is not ready to send. recipients not ready"}')
        with mock.patch.object(mc.requests, 'post', side_effect=[
                self._resp(200), not_ready, not_ready, self._resp(204)]) as post, \
             mock.patch.object(mc.requests, 'put', return_value=self._resp(200)), \
             mock.patch('time.sleep') as sleep:
            ok = mc.send_email_via_mailchimp('a@b.com', 's', '<p>x</p>', retry_delays=(5, 10, 20))
        self.assertTrue(ok)
        self.assertEqual(post.call_count, 4)  # create + 3 sends
        self.assertEqual([c.args[0] for c in sleep.call_args_list], [5, 10])

    def test_gives_up_after_delays(self):
        import mailchimp_client as mc
        not_ready = self._resp(400, 'recipients not ready')
        with mock.patch.object(mc.requests, 'post', side_effect=[self._resp(200)] + [not_ready] * 3), \
             mock.patch.object(mc.requests, 'put', return_value=self._resp(200)), \
             mock.patch('time.sleep'):
            self.assertFalse(mc.send_email_via_mailchimp('a@b.com', 's', 'x', retry_delays=(1, 1)))

    def test_no_retry_by_default_or_on_other_errors(self):
        import mailchimp_client as mc
        with mock.patch.object(mc.requests, 'post', side_effect=[
                self._resp(200), self._resp(400, 'recipients not ready')]) as post, \
             mock.patch.object(mc.requests, 'put', return_value=self._resp(200)), \
             mock.patch('time.sleep') as sleep:
            self.assertFalse(mc.send_email_via_mailchimp('a@b.com', 's', 'x'))
        self.assertEqual(post.call_count, 2)
        sleep.assert_not_called()
        with mock.patch.object(mc.requests, 'post', side_effect=[
                self._resp(200), self._resp(401, 'unauthorized')]) as post, \
             mock.patch.object(mc.requests, 'put', return_value=self._resp(200)), \
             mock.patch('time.sleep') as sleep:
            self.assertFalse(mc.send_email_via_mailchimp('a@b.com', 's', 'x', retry_delays=(1,)))
        sleep.assert_not_called()


if __name__ == '__main__':
    unittest.main()
