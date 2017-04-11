from __future__ import unicode_literals

from query_builder.config.app import settings

class Pagination(object):
    DEFAULT_RESULTS_LIMIT = settings.app_settings["results_limit_default"]
    PAGE_SIZE_DEFAULT = settings.app_settings["page_size_default"]

    def __init__(self, limit, offset):
        self._limit = int(limit) if limit else None
        self._offset = int(offset) if offset else 0

    @property
    def page_size(self):
        return min(abs(self.response_limit - self._offset), self.PAGE_SIZE_DEFAULT)

    @property
    def page_offset(self):
        # e.g. if the max response limit is 500 and page size is 50, the
        # max offset is 450
        max_possible_offset = abs(self.response_limit - self.PAGE_SIZE_DEFAULT)
        return min(self._offset, max_possible_offset)

    @property
    def response_limit(self):
        return self._calculate_limit(self.DEFAULT_RESULTS_LIMIT, self.DEFAULT_RESULTS_LIMIT)

    def _calculate_limit(self, default_limit, max_limit):
        """Returns default if no limit set, else returns minimum of requested
        limit and max allowed limit."""
        if self._limit is None:
            return default_limit

        return min(self._limit, max_limit)
