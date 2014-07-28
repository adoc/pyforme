"""
"""

import os
import cgi
import tempfile

import PIL

import forme.util
import forme.validators.upload


class ImageUpload(forme.validators.upload.PersistentUpload):
    """
    """

    dir = os.path.join(tempfile.gettempdir(), 'image_upload')
    format = "JPEG"
    quality = 95

    def __init__(self, *args, **kwa):
        for attr in ('format', 'quality'):
            if attr in kwa:
                setattr(self, attr, kwa.pop(kwa))

        forme.validators.upload.PersistentUpload.__init__(self, *args, **kwa)

    def _persist(self, fieldobj):
        image = PIL.Image.open(fieldobj.file)
        image.convert("RGB")

        image.save(os.path.join(self.dir, fieldobj.filename), self.format,
                   quality=self.quality)

        return fieldobj