from __future__ import unicode_literals, absolute_import
from django.utils.text import slugify
from string import digits, ascii_lowercase
from random import choice


def generate_random_string(length=5):
    digit_len = length // 2
    alpha_len = length - digit_len
    return "".join(
        [choice(digits) for _ in range(digit_len)]
        + [choice(ascii_lowercase) for _ in range(alpha_len)]
    )


def optimized_queryset(self, request):
    fields = self.__class__.model._meta.get_fields()
    fks = [field.name for field in fields if field.many_to_one and field.concrete]
    m2m = [field.name for field in fields if field.many_to_many and field.concrete]
    return (
        super(self.__class__, self)
            .get_queryset(request)
            .select_related(*fks)
            .prefetch_related(*m2m)
    )



def create_slug(instance, new_slug=None, append_string=None):
    if new_slug is not None:
        slug = new_slug
    elif instance.slug:
        slug = instance.slug
    elif hasattr(instance, "title"):
        slug = slugify(instance.title)
    elif hasattr(instance, "name"):
        slug = slugify(instance.name)
    else:
        slug = None
    if append_string and slug:
        slug = slugify(append_string + slug)
    if slug:
        qs = instance.__class__.objects.filter(slug=slug).order_by("-id")
        exists = True if qs.exists() and qs.first().id != instance.id else False
        if exists:
            new_slug = "%s-%s" % (slug, generate_random_string(length=5))
            return create_slug(instance, new_slug=new_slug)
        if len(slug) > 50:
            slug = slug[:44] + "-" + generate_random_string(length=5)
        if not slug:
            slug = generate_random_string(length=5)
        return slug
    else:
        return None
