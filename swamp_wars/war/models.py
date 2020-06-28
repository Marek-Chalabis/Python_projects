from django.db import models
from django.core.exceptions import ValidationError
from django import forms


def validate_zero(value):
    # checks if number is greater then 0
    if value < 0:
        raise ValidationError('You need to put at least 1 point into each statistic')


class BaseStats(models.Model):
    DMG = models.IntegerField(validators=[validate_zero])
    DEX = models.IntegerField(validators=[validate_zero])
    DEF = models.IntegerField(validators=[validate_zero])

    class Meta:
        abstract = True


class Hero(BaseStats):
    name = models.CharField(max_length=15, unique=True)
    race = models.CharField(max_length=15)
    HP = models.IntegerField()
    LVL = models.IntegerField()

    def __str__(self):
        return self.name

    def call(self):
        dmg = 'mighty' if self.DMG >= 8 else 'week'
        dx = 'agile' if self.DEX >= 8 else 'slow'
        de = 'resistant' if self.DEF >= 8 else 'soft'
        return f"{dmg}, {dx}, {de}-{self.race}"


class Beast(BaseStats):
    name = models.CharField(max_length=15, unique=False)
    race = models.CharField(max_length=15)
    opponent = models.ForeignKey(Hero, on_delete=models.CASCADE, default=1)
    HP = models.IntegerField()

    def __str__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     if self.race == 'human':
    #         self.DMG += 5
    #     elif self.race == 'elf':
    #         self.DEX += 5
    #     elif self.race == 'orc':
    #         self.DEF += 5
    #     super(Hero, self).save(*args, **kwargs)
