import formencode


class FilteredForEach(formencode.ForEach):
    """Strips `None` values from list returned by formencode.ForeEach.
    """
    def _attempt_convert(self, value, state, validate):
        return [value 
                for value in formencode.ForEach._attempt_convert(self, 
                    value, state, validate)
                if value is not None]