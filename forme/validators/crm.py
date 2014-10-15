import re
import formencode


re_number_only = re.compile('[\W_]+', re.UNICODE)


class PhoneValidator(formencode.validators.String):
    def _convert_to_python(self, value, state):
        value = re_number_only.sub('', str(value))
        return value