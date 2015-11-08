from django.db import models


class Person(models.Model):
    lahmanID = models.CharField(
        unique=True,
        db_index=True,
        max_length=10,
        blank=True,
        help_text=u'ID used in Lahman Database version 4.0')
    lahman40ID = models.CharField(
        unique=True,
        db_index=True,
        max_length=10,
        blank=True,
        help_text=u'ID used in Lahman Database version 4.0')
    lahman45ID = models.CharField(
        unique=True,
        db_index=True,
        max_length=10,
        blank=True,
        help_text=u'ID used in Lahman database version 4.5')
    retroID = models.CharField(
        unique=True,
        db_index=True,
        max_length=10,
        blank=True,
        help_text=u'ID used by retrosheet')
    holtzID = models.CharField(
        unique=True,
        db_index=True,
        max_length=10,
        blank=True,
        help_text=u'ID used by Sean Holtz\'s Baseball Almanac')
    bbrefID = models.CharField(
        unique=True,
        db_index=True,
        max_length=10,
        blank=True,
        help_text=u'ID used by Baseball Reference website')
    mlbamID = models.CharField(
        unique=True,
        db_index=True,
        max_length=10,
        blank=True,
        help_text=u'ID used by MLB Advanced Media')

    birth = models.DateField(null=True, blank=True)
    birth_country = models.CharField(max_length=255, blank=True)
    birth_state = models.CharField(max_length=255, blank=True)
    birth_city = models.CharField(max_length=255, blank=True)

    death = models.DateField(null=True, blank=True)
    death_country = models.CharField(max_length=255, blank=True)
    death_state = models.CharField(max_length=255, blank=True)
    death_city = models.CharField(max_length=255, blank=True)

    given_name = models.CharField(max_length=255, blank=True)
    family_name = models.CharField(max_length=255, blank=True)

    debut = models.DateField(null=True, blank=True)
    final_game = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('family_name', 'given_name', 'birth')

    @property
    def full_name(self):
        return u'{} {}'.format(self.given_name, self.family_name)

    def __str__(self):
        return self.full_name

    def __unicode__(self):
        return unicode(str(self))
