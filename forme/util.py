"""
"""

import os
import hashlib
import base64


def random_filename(length):
    assert length<=16

    def randstr(length):
        return base64.b64encode(
                    hashlib.sha256(
                        os.urandom(length*2))
                    .digest(), altchars=b"_-")

    rnd_name = randstr(length)
    while rnd_name.startswith(b'-'):
        rnd_name = randstr(length)

    return rnd_name[:length].decode()