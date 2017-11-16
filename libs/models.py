from __future__ import unicode_literals
from itertools import chain
from libs.moment import to_timestamp
from libs.base62 import base62_encode
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class _BaseAbstract(models.Model):
    nonce = models.CharField(max_length=128, blank=True, null=True)
    id62 = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    
    created_at = models.DateTimeField(db_index=True)
    created_at_timestamp = models.PositiveIntegerField(db_index=True)
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created_by")

    updated_at = models.DateTimeField(db_index=True, blank=True, null=True)
    updated_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    updated_by = models.ForeignKey(User, blank=True, null=True, related_name="%(app_label)s_%(class)s_updated_by")
    
    published_at = models.DateTimeField(blank=True, null=True)
    published_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    published_by = models.ForeignKey(User, blank=True, null=True, related_name="%(app_label)s_%(class)s_published_by")
    
    unpublished_at = models.DateTimeField(blank=True, null=True)
    unpublished_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    unpublished_by = models.ForeignKey(User, blank=True, null=True, related_name="%(app_label)s_%(class)s_unpublished_by")
    
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    approved_by = models.ForeignKey(User, blank=True, null=True, related_name="%(app_label)s_%(class)s_approved_by")

    unapproved_at = models.DateTimeField(blank=True, null=True)
    unapproved_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    unapproved_by = models.ForeignKey(User, blank=True, null=True, related_name="%(app_label)s_%(class)s_unapproved_by")

    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    deleted_by = models.ForeignKey(User, db_index=True, blank=True, null=True, related_name="%(app_label)s_%(class)s_deleted_by")
    
    
    def is_owner(self, user):
        return self.created_by.pk == user.pk

    def save(self, *args, **kwargs):
        now = timezone.now()

        # create first time record
        if self.created_at is None:
            self.created_at = now
            self.created_at_timestamp = to_timestamp(self.created_at)

        # always update
        self.updated_at = now
        self.updated_at_timestamp = to_timestamp(self.updated_at)

        # save the first time record
        instance = super(_BaseAbstract, self).save(*args, **kwargs)

        # generate id62
        if self.id and not self.id62:
            self.id62 = base62_encode(self.id)
            instance = super(_BaseAbstract, self).save(*args, **kwargs)
        
        return instance
    
    def delete(self, *args, **kwargs):
        # mark when the record deleted
        self.deleted_at = timezone.now()
        self.deleted_at_timestamp = to_timestamp(self.deleted_at)

        # save it
        return super(_BaseAbstract, self).save(*args, **kwargs)

    def log(self, user, message):
        pass

    # Getter
    def get_created_at(self):
        return {
            'utc': self.created_at,
            'timestamp': self.created_at_timestamp
        }

    def get_deleted_at(self):
        return {
            'utc': self.deleted_at,
            'timestamp': self.deleted_at_timestamp
        }

    def get_lat_lng(self, field_name):
        point = getattr(self, field_name, None)

        if point is not None and hasattr(point, "x") and hasattr(point, "y"):
            return {
                'latitude': point.y,
                'longitude': point.x
            }
        else:
            return {
                'latitude': 0,
                'longitude': 0
            }

    def get_all_sizes(self, field_name, sizes=None):
        if field_name in self._meta.get_all_field_names():
            image = getattr(self, field_name)

            if hasattr(image, "path"):
                return generate_all_sizes(image.path, sizes=sizes)

    # Setter
    def set_lat_lng(self, field_name, value):
        point = None

        if hasattr(self, field_name) and "longitude" in value and "latitude" in value:
            point = Point(value["longitude"], value["latitude"])
            setattr(self, field_name, point)

        return point

    # Backward
    def get_all_field_names(self):
        return list(
            set(
                chain.from_iterable(
                    (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
                    for field in self._meta.get_fields()
                    # For complete backwards compatibility, you may want to exclude
                    # GenericForeignKey from the results.
                    if not (field.many_to_one and field.related_model is None)
                )
            )
        )

    class Meta:
        abstract = True

class BaseModelGeneric(_BaseAbstract):
    created_by = models.ForeignKey(User, db_index=True, related_name="%(app_label)s_%(class)s_created_by")

    class Meta:
        abstract = True

class BaseModelUnique(_BaseAbstract):

    def user_unicode(self):
        return  u'%s %s' % (self.first_name, self.last_name)
    User.__unicode__ = user_unicode

    created_by = models.OneToOneField(User, db_index=True, related_name="%(app_label)s_%(class)s_created_by")

    class Meta:
        abstract = True