import time
import hashlib
import hmac
import base64
import formencode


class HmacValidator(formencode.validators.FancyValidator):
    """
    """

    hashalg = hashlib.sha512

    messages = {
        'malformed': 'Malformed challenge hash.'
    }

    def __init__(self, key, *args, **kwa):
        for k in ('hashalg', ):
            if k in kwa:
                setattr(self, k, kwa.pop(k))
        self.key = key
        self.digest_size = self.hashalg().digest_size
        formencode.validators.FancyValidator.__init__(self, *args, **kwa)

    def _convert_to_python(self, value, state):
        value = base64.urlsafe_b64decode(value)
        return value[self.digest_size:]

    def _convert_from_python(self, value, state):
        alg = hmac.new(self.key, msg=value, digestmod=self.hashalg)
        return base64.urlsafe_b64encode(alg.digest() + value)

    def _validate_other(self, value, state):
        value = base64.urlsafe_b64decode(value)
        challenge_digest = value[:self.digest_size]

        alg = hmac.new(self.key, msg=value[self.digest_size:], digestmod=self.hashalg)

        if len(challenge_digest) < self.digest_size:
            raise formencode.Invalid(self.message('malformed', state), value,
                                     state)

        if not hmac.compare_digest(alg.digest(), challenge_digest) is True:
            raise formencode.Invalid(self.message('malformed', state), value,
                                     state)


class DelayValidator(formencode.validators.FancyValidator):
    """
    """
    min = 0
    max = float("+inf")

    messages = {
        'min': 'Not enough time has elapsed.',
        'max': 'Too much time has elapsed.'
    }

    def _convert_to_python(self, value, state):
        try:
            return float(value)
        except ValueError:
            raise formencode.Invalid(self.message('invalid', state), value,
                                     state)

    def _convert_from_python(self, value, state):
        return str(time.time()).encode()

    def _validate_python(self, value, state):
        delta = time.time() - value

        if delta > self.max:
            raise formencode.Invalid(self.message('max', state), value, state)

        if delta < self.min:
            raise formencode.Invalid(self.message('min', state), value, state)