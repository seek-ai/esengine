# -*- coding: utf-8 -*-
import math
from six.moves import range
from esengine.exceptions import PaginationError, StopPagination


class Pagination(object):

    def __init__(self, iterable, page=1, per_page=10):
        """
        Initialize an iterator
        :param iterable: Payload (recommended), ResultSet or an iterator
        :param page:
        :param per_page:
        :return:
        """
        self.init(iterable, page, per_page)

    def init(self, iterable, page, per_page):
        if page < 1:
            raise PaginationError("Page is lower than 1")
        self.iterable = iterable  # noqa
        self.page = page  # noqa
        self.per_page = per_page  # noqa
        if hasattr(iterable, 'count'):
            self.total = iterable.count()
        else:
            self.total = len(iterable)  # noqa
        start_index = (page - 1) * per_page
        end_index = page * per_page
        if hasattr(iterable, 'search'):
            self.items = iterable.search(from_=start_index, size=per_page)  # noqa
        else:
            self.items = iterable[start_index:end_index]  # noqa
        if not self.items and page != 1:
            raise StopPagination("There is no items to paginate")

    def count(self):
        return self.total

    @property
    def pages(self):
        """The total number of pages"""
        return int(math.ceil(self.total / float(self.per_page)))

    def prev_page(self, inplace=False):
        """Returns a :class:`Pagination` object for the previous page."""
        if self.iterable is None:
            raise PaginationError('iterable is needed')
        if not self.has_prev:
            raise StopPagination("There is no previous page")
        return (
            self.__class__
            if not inplace else
            self.init
        )(self.iterable, self.page - 1, self.per_page)

    def backward(self):
        return self.prev_page(inplace=True)

    @property
    def prev_num(self):
        """Number of the previous page."""
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    def next_page(self, inplace=False):
        """Returns a :class:`Pagination` object for the next page."""
        if self.iterable is None:
            raise PaginationError('iterable is needed')
        if not self.has_next:
            raise StopPagination("There is no next page")
        return (
            self.__class__
            if not inplace else
            self.init
        )(self.iterable, self.page + 1, self.per_page)

    def forward(self):
        self.next_page(inplace=True)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:

        .. sourcecode:: html+jinja

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
