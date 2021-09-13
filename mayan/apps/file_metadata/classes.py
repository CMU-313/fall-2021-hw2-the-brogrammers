from __future__ import unicode_literals

import logging

from django.apps import apps

from .events import event_file_metadata_document_version_finish
from .exceptions import FileMetadataDriverError
from .signals import post_document_version_file_metadata_processing

logger = logging.getLogger(__name__)


class FileMetadataDriver(object):
    _registry = {}

    @classmethod
    def register(cls, mimetypes):
        for mimetype in mimetypes:
            cls._registry.setdefault(mimetype, []).append(cls)

    @classmethod
    def process_document_version(cls, document_version):
        for driver_class in cls._registry.get(document_version.mimetype, ()):
            try:
                driver = driver_class()
                driver.process(document_version=document_version)
            except FileMetadataDriverError:
                # If driver raises error, try next in the list
                pass
            else:
                # If driver was successfull there is no need to try
                # others in the list for this mimetype

                event_file_metadata_document_version_finish.commit(
                    action_object=document_version.document,
                    target=document_version
                )

                post_document_version_file_metadata_processing.send(
                    sender=document_version.__class__,
                    instance=document_version
                )
                return

    def process(self, document_version):
        logger.info(
            'Starting processing document version: %s', document_version
        )

        StoredDriver = apps.get_model(
            app_label='file_metadata', model_name='StoredDriver'
        )

        driver_path = '.'.join([self.__module__, self.__class__.__name__])

        driver, created = StoredDriver.objects.get_or_create(
            driver_path=driver_path, defaults={
                'internal_name': self.internal_name
            }
        )

        driver.driver_entries.filter(
            document_version=document_version
        ).delete()

        document_version_driver_entry = driver.driver_entries.create(
            document_version=document_version
        )

        for key, value in self._process(document_version=document_version).items():
            document_version_driver_entry.entries.create(
                key=key, value=value
            )

    def _process(self, document_version):
        raise NotImplementedError(
            'Your %s class has not defined the required '
            'process_document_version() method.' % self.__class__.__name__
        )
