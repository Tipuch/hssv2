from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from sortedm2m.fields import SortedManyToManyField
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.conf import settings  

@python_2_unicode_compatible
class Categorie(models.Model):
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
    photos = SortedManyToManyField('photologue.Photo',
                                   related_name='categorie',
                                   verbose_name=_('photos'),
                                   blank=True)
    sites = models.ManyToManyField(Site, verbose_name=_(u'sites'),
                                   blank=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super(Photo, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def photo_count(self, public=True):
        """Return a count of all the photos in this gallery."""
        if public:
            return self.public().count()
        else:
            return self.photos.filter(sites__id=settings.SITE_ID).count()
    photo_count.short_description = _('count')

    def public(self):
        """Return a queryset of all the public photos in this gallery."""
        return self.photos.is_public().filter(sites__id=settings.SITE_ID)

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
post_save.connect(add_default_site, sender=Categorie)
