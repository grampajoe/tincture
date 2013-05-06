"""
Unit tests for session generic views
"""
import unittest
import mock

from tincture.views.generic.session import SessionMixin


class TestSessionMixin(unittest.TestCase):
    """Tests for SessionMixin."""
    def test_get_session(self):
        """Test getting a session."""
        mixin = SessionMixin()
        mixin.session = mock.sentinel.session

        session = mixin.get_session()

        self.assertIs(session, mixin.session)

    def test_get_session_default(self):
        """Test the default for the session attribute."""
        mixin = SessionMixin()

        session = mixin.get_session()

        self.assertIsNone(session)
