from django.db import models

class ContactDetail(models.Model):
    DOMAIN_CHOICES = [
        ('PR', 'krati@elan.org.in'),
        ('Sponsorship', 'ashutosh.t@elan.org.in'),
        ('Shows', 'adyasa.m@elan.org.in'),
        ('Workshop', 'mahesh.s@elan.org.in'),
        ('Culti', 'sharanya@elan.org.in'),
        ('Biggies', 'sharanya@elan.org.in'),
        ('Techy', 'mahesh.s@elan.org.in'),
        ('Social Cause', 'sharanya@elan.org.in'),
        ('Informals', 'krati@elan.org.in'),
        ('Miscellaneous', 'info@elan.org.in'),
        ('Finance', 'finance.head@elan.org.in'),
        ('Merch', 'finance.head@elan.org.in')
    ]
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=200)
    institute = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    domain = models.CharField(max_length=45, choices=DOMAIN_CHOICES)

    def __str__(self):
        return self.name

