from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _



class StatusChoices(TextChoices):

    NEW = 'NEW',_('NEW')
    IN_PROGRESS = 'IN_PROGRESS',_('IN_PROGRESS')
    ONBOARDED = 'ONBOARDED',_('ONBOARDED')
    DEACTIVATED = 'DEACTIVATED',_('DEACTIVATED')