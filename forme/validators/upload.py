import os
import shutil
import base64
import hashlib
import pickle
import cgi
import tempfile
import formencode

import forme.util

class PersistentUpload(formencode.validators.FieldStorageUploadConverter):
    """Validate an upload and store it.

    TODO: ! checksum_file is not exclusive.
            _retreive returns a FieldStorage object that is never closed.
    """

    messages = {
        'too_large': 'The image uploaded is too large.',
        'invalid_file': 'The stored file specified does not exist.'}

    min = 1024
    max = 10 * 1024 ** 2
    #max = 120 * 1024
    dir = tempfile.gettempdir()
    make_dir = True
    lower_ext = True

    random_name = True
    random_length = 8

    upload_key = "upload"
    stored_key = "stored"
    stored_path_key = "stored_path"

    @property
    def checksum_filepath(self):
        return os.path.join(self.dir, 'checksum.dat')
    
    checksum_blocksize = 8192
    allow_duplicate = True

    def __init__(self, *args, **kwa):
        for attr in ('min', 'max', 'dir','make_dir', 'lower_ext', 'random_name',
                     'random_length', 'upload_key', 'stored_key',
                     'checksum_filepath', 'checksum_blocksize',
                     'allow_duplicate'): # 'file_key'
            if attr in kwa:
                setattr(self, attr, kwa.pop(attr))

        if self.make_dir is True:
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)

        self.checksum_map = {}

        try:
            checksum_file = open(self.checksum_filepath, "rb")
        except FileNotFoundError:
            self.checksum_file = open(self.checksum_filepath, "wb")
        else:
            try:
                self.checksum_map = pickle.load(checksum_file)
            except EOFError:
                pass
            self.checksum_file = open(self.checksum_filepath, "r+b")

        (formencode.validators.FieldStorageUploadConverter.
            __init__(self, *args, **kwa))

    def __del__(self):
        self.checksum_file.close()

    def _checksum(self, fieldobj, rewind=True):
        md5 = hashlib.md5()
        fp = fieldobj.file
        for block in iter(
                lambda: fp.read(self.checksum_blocksize), ''):
            if not block:
                break
            md5.update(block)
        if rewind is True:
            fieldobj.file.seek(0)
        return md5.digest()

    def _checkdupe(self, fieldobj):
        digest = self._checksum(fieldobj)
        if digest in self.checksum_map:
            # We already have the file.
            fieldobj.filename = self.checksum_map[digest]
            return True
        else:
            self.checksum_map[digest] = fieldobj.filename
            pickle.dump(self.checksum_map, self.checksum_file)
            self.checksum_file.seek(0)

    def _persist(self, fieldobj):
        shutil.copyfileobj(fieldobj.file,
            open(os.path.join(self.dir, fieldobj.filename), 'wb'))

    def _checkpersist(self, filename):
        return os.path.exists(os.path.join(self.dir, filename))
        '''
        fieldobj = cgi.FieldStorage()
        fieldobj.file = open(os.path.join(self.dir, filename), 'rb')
        fieldobj.filename = filename
        #fieldobj.mimetype = ?
        return fieldobj'''

    def _convert_to_python(self, value, state):
        value = (formencode.validators.FieldStorageUploadConverter.
                    _convert_to_python(self, value, state))

        uploadobj = value.get(self.upload_key)
        fieldstored = value.get(self.stored_key)

        if isinstance(uploadobj, cgi.FieldStorage):
            # Do some validation here.

            # Check file upload size -after- the file is uploaded.
            # This doesn't check the file size as it's being uploaded yet.
            if uploadobj.bytes_read > self.max:
                raise formencode.Invalid(self.message('too_large', state),
                                         value, state)

            # Update filename if neccessary.
            filename, fileext = os.path.splitext(uploadobj.filename)

            if self.lower_ext is True:
                fileext = fileext.lower()

            if self.random_name is True:
                filename = forme.util.random_filename(self.random_length)

            uploadobj.filename = filename+fileext

            # Validate the filename.
            (formencode.validators.UnicodeString(max=256, min=3).
                to_python(uploadobj.filename))

            if self.allow_duplicate is not True:
                if self._checkdupe(uploadobj) is True:
                    print("remove upload key.")
                    del value['upload']
                else:
                    self._persist(uploadobj)
            else:
                self._persist(uploadobj)

            #value[self.file_key] = uploadobj
            value[self.stored_key] = uploadobj.filename


        elif fieldstored is not None:
            if self._checkpersist(fieldstored) is not True:
                raise formencode.Invalid(self.message('invalid_file', state),
                                         value, state)
            #fieldobj = self._retreive(fieldstored)
            #value[self.file_key] = fieldobj
            #value[self.stored_key] = fieldobj.filename

        else:
            return None

        value[self.stored_path_key] = os.path.join(self.dir, value[self.stored_key])

        return value