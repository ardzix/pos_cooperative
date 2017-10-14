import os
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_unicode, smart_str
from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage

def generate_name(instance, filename):
    if getattr(settings, "FLATTEN_PATH_NAME", False):
        form = '%Y-%m-%d-%H%M%S'
    else:
        form = '%Y/%m/%d/%H%M%S'

    extension   = os.path.splitext(filename)[1]
    prefix      = os.path.normpath(
        force_unicode(
            timezone.now().strftime(
                smart_str(form)
            )
        )
    )
    suffix     = '%s%s' % (get_random_string(), extension)
    
    return '%s-%s' % (prefix, suffix)

STORAGE_PHOTO = FileSystemStorage(
    location = settings.MEDIA_ROOT + settings.PHOTO_FOLDER,
    base_url = settings.MEDIA_URL + settings.PHOTO_FOLDER
)
STORAGE_BARCODE = FileSystemStorage(
    location = settings.MEDIA_ROOT + settings.BARCODE_FOLDER,
    base_url = settings.MEDIA_URL + settings.BARCODE_FOLDER
)
STORAGE_VIDEO = FileSystemStorage(
    location = settings.MEDIA_ROOT + settings.VIDEO_FOLDER,
    base_url = settings.MEDIA_URL + settings.VIDEO_FOLDER
)
STORAGE_BACKGROUND_COVER = FileSystemStorage(
    location = settings.MEDIA_ROOT + settings.BACKGROUND_COVER_FOLDER,
    base_url = settings.MEDIA_URL + settings.BACKGROUND_COVER_FOLDER
)
STORAGE_AVATAR = FileSystemStorage(
    location = settings.MEDIA_ROOT + settings.AVATAR_FOLDER,
    base_url = settings.MEDIA_URL + settings.AVATAR_FOLDER
)
STORAGE_LOGO = FileSystemStorage(
    location = settings.MEDIA_ROOT + settings.LOGO_FOLDER,
    base_url = settings.MEDIA_URL + settings.LOGO_FOLDER
)
# STORAGE_IDENTITY = FileSystemStorage(
#     location = settings.SECURE_ROOT + settings.IDENTITY_FOLDER
# )