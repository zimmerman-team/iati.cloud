import collections
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.fields import is_simple_callable


def get_attribute(instance, attrs):
    """
    Similar to rest_framework.fields.py.get_attribute but returns none if
    a nested attribute hasvalue of None.
    """
    for attr in attrs:
        try:
            if isinstance(instance, collections.Mapping):
                instance = instance[attr]
            else:
                instance = getattr(instance, attr)
            if instance is None:
                return None
        except ObjectDoesNotExist:
            return None
        if is_simple_callable(instance):
            try:
                instance = instance()
            except (AttributeError, KeyError) as exc:
                # If we raised an Attribute or KeyError here it'd get treated
                # as an omitted field in `Field.get_attribute()`. Instead we
                # raise a ValueError to ensure the exception is not masked.
                raise ValueError('Exception raised in callable attribute "{0}"; original exception was: {1}'.format(attr, exc))

    return instance
