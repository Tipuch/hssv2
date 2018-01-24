from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import ugettext
from photologue.models import Photo

from .models import Category, PhotoSet


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = 'title',


class PhotoAssociationForm(forms.Form):
    photo_set = forms.ModelChoiceField(PhotoSet.objects.all())
    category = forms.ModelChoiceField(Category.objects.all())
    photo = forms.ModelChoiceField(Photo.objects.all())

    def clean(self):
        photo_set = self.cleaned_data.get('photo_set')
        photo = self.cleaned_data.get('photo')
        if photo_set and photo:
            # validate that the photo belongs to the photo_set
            if not photo_set.gallery.photos.filter(id=photo.id).exists():
                raise ValidationError(ugettext(f"the photo:{photo} does not belong to photo_set:{photo_set}"))

    @transaction.atomic
    def associate_photo(self):
        if self.is_valid():
            photo_set = self.cleaned_data['photo_set']
            photo = self.cleaned_data['photo']
            category = self.cleaned_data['category']
            photo_set.gallery.photos.remove(photo)
            category.gallery.photos.add(photo)