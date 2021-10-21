# Core Django Imports
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Third-party app imports
from model_utils.models import TimeStampedModel


class ImageModel(TimeStampedModel):
    image = models.ImageField(_("Image"), upload_to="images")
    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, blank=True, null=True, related_name="user_image"
    )
    # task = models.ForeignKey(
    #     "task_app.Task", on_delete=models.SET_NULL, blank=True, null=True, related_name="task_imagemodel"
    # )

    def __str__(self):
        return str(self.id)
