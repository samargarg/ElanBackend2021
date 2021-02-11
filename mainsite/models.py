from django.db import models

class ContactDetail(models.Model):
    DOMAIN_CHOICES = [
        ('PR', 'PR'),
        ('Sponsorship', 'Sponsorship'),
        ('Shows', 'Shows'),
        ('Workshop', 'Workshop'),
        ('Culti', 'Culti'),
        ('Biggies', 'Biggies'),
        ('Techy', 'Techy'),
        ('Social Cause', 'Social Cause'),
        ('Informals', 'Informals'),
        ('Miscellaneous', 'Miscellaneous'),
        ('Finance', 'Finance'),
        ('Merch', 'Merch')
    ]
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)
    domain = models.CharField(max_length=45, choices=DOMAIN_CHOICES)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class ELANRegistration(models.Model):
    name = models.CharField(max_length=45)
    institute = models.CharField(max_length=50)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

