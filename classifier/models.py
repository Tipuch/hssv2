from logging import getLogger
from uuid import uuid4

from django.db import models, transaction
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from photologue.models import Photo, Gallery
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.conf import settings

from classifier.constants import CATEGORIES_LIMIT

logger = getLogger(__file__)


class Category(models.Model):
    date_added = models.DateTimeField(_('date published'),
                                      default=now)
    title = models.CharField(_('title'),
                             max_length=250,
                             unique=True)
    slug = models.SlugField(_('title slug'),
                            unique=True,
                            max_length=250,
                            help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField(_('description'),
                                   blank=True)
    is_public = models.BooleanField(_('is public'),
                                    default=True,
                                    help_text=_('Public categories will be displayed '
                                                'in the default views.'))
    gallery = models.OneToOneField(Gallery, verbose_name=_("gallery"), related_name='category',
                                   on_delete=models.CASCADE)

    sites = models.ManyToManyField(Site, verbose_name=_('sites'), blank=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not hasattr(self, 'gallery'):
            gallery_slug = f"{self.slug}-{uuid4()}"
            self.gallery = Gallery.objects.create(title=gallery_slug, slug=gallery_slug)
        if Category.objects.count() < CATEGORIES_LIMIT:
            super().save(*args, **kwargs)
        else:
            logger.warning(f"{self.title} was not created because there are already {CATEGORIES_LIMIT}")

    def __str__(self):
        return self.title


class PhotoSet(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    title = models.CharField(_('title'), max_length=250, unique=True)
    slug = models.SlugField(_('title slug'), unique=True, max_length=250,
                            help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField(_('description'), blank=True)
    gallery = models.OneToOneField(Gallery, verbose_name=_("gallery"), related_name='photo_set',
                                   on_delete=models.CASCADE)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not hasattr(self, 'gallery'):
            gallery_slug = f"{self.slug}-{uuid4()}"
            self.gallery = Gallery.objects.create(title=gallery_slug, slug=gallery_slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


def add_default_site(instance, created, **kwargs):
    """
    Called via Django's signals when an instance is created.
    In case PHOTOLOGUE_MULTISITE is False, the current site (i.e.
    ``settings.SITE_ID``) will always be added to the site relations if none are
    present.
    """
    if not created:
        return
    if getattr(settings, 'PHOTOLOGUE_MULTISITE', False):
        return
    if instance.sites.exists():
        return
    instance.sites.add(Site.objects.get_current())
post_save.connect(add_default_site, sender=Category)
