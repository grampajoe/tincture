class SessionMixin(object):
    """Provides facilities for retrieving a SQLAlchemy session."""
    session = None

    def get_session(self):
        """Return a SQLAlchemy session.

        Override this method to provide custom logic for session retrieval."""
        return self.session
