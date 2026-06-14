import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from gws_gmail import is_destructive as is_destructive_gmail
from gws_calendar import is_destructive as is_destructive_calendar


class TestGmailDestructiveDetection:
    """Test destructive operation detection for Gmail."""

    def test_send_is_destructive(self):
        assert is_destructive_gmail(["+send", "--to", "user@example.com"])

    def test_reply_is_destructive(self):
        assert is_destructive_gmail(["+reply", "--to", "user@example.com"])

    def test_messages_delete_is_destructive(self):
        assert is_destructive_gmail(["messages.delete", "--params", '{"id": "1"}'])

    def test_messages_trash_is_destructive(self):
        assert is_destructive_gmail(["messages.trash", "--params", '{"id": "1"}'])

    def test_list_is_not_destructive(self):
        assert not is_destructive_gmail(["users.messages", "list"])

    def test_get_is_not_destructive(self):
        assert not is_destructive_gmail(["users.messages", "get"])


class TestCalendarDestructiveDetection:
    """Test destructive operation detection for Calendar."""

    def test_insert_is_destructive(self):
        assert is_destructive_calendar(["+insert", "--summary", "Meeting"])

    def test_events_delete_is_destructive(self):
        assert is_destructive_calendar(["events.delete", "--params", '{"eventId": "1"}'])

    def test_events_insert_is_destructive(self):
        assert is_destructive_calendar(["events.insert", "--json", '{"summary": "Test"}'])

    def test_calendars_clear_is_destructive(self):
        assert is_destructive_calendar(["calendars.clear"])

    def test_list_is_not_destructive(self):
        assert not is_destructive_calendar(["calendarList", "list"])

    def test_freebusy_query_is_not_destructive(self):
        assert not is_destructive_calendar(["freebusy.query"])
