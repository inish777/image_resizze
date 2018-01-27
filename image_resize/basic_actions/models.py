import os

from django.db import models
from django.utils.crypto import get_random_string
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Image(models.Model):
    class Meta:
        db_table = 'images'

    image_field = models.ImageField(upload_to='upload_images')
    key = models.CharField(unique=True, max_length=32, editable=False)

    def __str__(self):
        return '%s' % self.key

    def save(self, *args, **kwargs):
        if self.pk:
            old_self = Image.objects.get(pk=self.pk)
            if self.image_field != old_self.image_field:
                old_self.image_field.delete(save=False)
        if not self.key:
            self.key = get_random_string(32)
        return super(Image, self).save(*args, **kwargs)


@receiver(signal=post_delete, sender=Image)
def delete_image_with_model(sender, instance, using, **kwargs):
    if instance.image_field:
        try:
            os.remove(instance.image_field.path)
        except OSError:
            pass
