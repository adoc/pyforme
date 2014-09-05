
import formencode


class FilteredForEach(formencode.ForEach):
    """Strips `None` values from list returned by formencode.ForeEach.
    Also adds a min and max items validation.
    """

    min = 0
    max = float("+inf")
    convert_to_list = True

    messages = {'min': 'Requires at least %(min)s items.',
                'max': 'Requires at most %(max)s items.'}

    def _foreach_generator(self, value, state, validate):
        for value in formencode.ForEach._attempt_convert(self, value, state,
                                                         validate):
            if any([validator.is_empty(value)
                        for validator in self.validators]) is not True:
                yield value

    def _attempt_convert(self, value, state, validate):
        return list(self._foreach_generator(value, state, validate))

    def _convert_to_python(self, value, state):
        value = formencode.ForEach._convert_to_python(self, value, state)

        aslist_len = len(value)
        if aslist_len > self.max:
            raise formencode.Invalid(self.message('max', state, max=self.max), value,
                                     state)
        if aslist_len < self.min:
            raise formencode.Invalid(self.message('min', state, min=self.min), value,
                                     state)

        return value


class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class UniqueForEach(FilteredForEach):
    """
    """
    #def __init__(self, *args, **kwa):
    #    FilteredForEach.__init__(self, *args, **kwa)

    def _foreach_generator(self, value, state, validate):
        index = set()

        for item in FilteredForEach._foreach_generator(self, value, state, validate):
            try:
                itemhash = hash(hashabledict(item))
            except TypeError:
                itemhash = hash(item)
            if itemhash not in index:
                index.add(itemhash)
                yield item
            else:
                raise formencode.Invalid('Item was not unique', value, state)