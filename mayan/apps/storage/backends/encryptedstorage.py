from __future__ import unicode_literals

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.encoding import force_text

from ..classes import BufferedFile, PassthroughStorage

from .literals import (
    ENCRYPTION_FILE_CHUNK_SIZE, ENCRYPTION_KEY_DERIVATION_ITERATIONS,
    ENCRYPTION_KEY_SIZE
)


class BufferedEncryptedFile(BufferedFile):
    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key')

        super(BufferedEncryptedFile, self).__init__(*args, **kwargs)

        self.initial_vector = self.file_object.read(16)
        self.cipher = AES.new(
            key=self.key, mode=AES.MODE_CBC, iv=self.initial_vector
        )
        self.binary_mode = 'b' in self.mode

    def _get_file_object_chunk(self):
        chunk = self.file_object.read(ENCRYPTION_FILE_CHUNK_SIZE)

        if chunk:
            data = unpad(
                padded_data=self.cipher.decrypt(chunk),
                block_size=AES.block_size
            )
            if self.binary_mode:
                return data
            else:
                return force_text(data)


class EncryptedPassthroughStorage(PassthroughStorage):
    def __init__(self, *args, **kwargs):
        password = kwargs.pop('password')
        super(EncryptedPassthroughStorage, self).__init__(*args, **kwargs)
        self.key = PBKDF2(
            count=ENCRYPTION_KEY_DERIVATION_ITERATIONS,
            dkLen=ENCRYPTION_KEY_SIZE,
            hmac_hash_module=SHA256,
            password=password,
            salt=settings.SECRET_KEY
        )

    def open(self, name, mode='rb', _direct=False):
        next_kwargs = {'name': name}
        if _direct:
            next_kwargs['mode'] = mode

            if issubclass(self.next_storage_class, PassthroughStorage):
                next_kwargs.update({'_direct': _direct})

            return self._call_backend_method(
                method_name='open', kwargs=next_kwargs
            )
        else:
            # Mode is always 'rb' when reading the encrypted file
            next_kwargs['mode'] = 'rb'
            storage_file = self._call_backend_method(
                method_name='open', kwargs=next_kwargs
            )
            return BufferedEncryptedFile(
                file_object=storage_file, key=self.key, mode=mode
            )

    def save(self, name, content, max_length=None, _direct=False):
        next_kwargs = {'max_length': max_length, 'name': name}
        if _direct:
            next_kwargs['content'] = content

            if issubclass(self.next_storage_class, PassthroughStorage):
                next_kwargs.update({'_direct': _direct})

            return self._call_backend_method(
                method_name='save', kwargs=next_kwargs
            )
        else:
            cipher = AES.new(key=self.key, mode=AES.MODE_CBC)
            name = self._call_backend_method(
                method_name='save', kwargs={
                    'content': ContentFile(content=''), 'name': name
                }
            )
            with self._call_backend_method(
                method_name='open', kwargs={
                    'name': name, 'mode': 'wb'
                }
            ) as file_object:
                file_object.write(cipher.iv)
                while True:
                    chunk = content.read(ENCRYPTION_FILE_CHUNK_SIZE)
                    if chunk:
                        chunk = pad(
                            data_to_pad=chunk, block_size=AES.block_size
                        )
                    else:
                        break

                    file_object.write(cipher.encrypt(chunk))

            return name
