from django import forms
from crispy_forms.helper import FormHelper
from django import forms
import random
from django.forms import ModelForm
from .models import Hero


class LvlUp(forms.Form):
    STAT = [('DMG', 'DMG'), ('DEF', 'DEF'), ('DEX', 'DEX')]
    stat = forms.ChoiceField(choices=STAT, widget=forms.RadioSelect)


class AvatarCreation(ModelForm):
    # creates avatar

    RACE = [('human', 'HUMAN(+ 5 DMG)'), ('orc', 'ORC(+ 5 DEF)'), ('elf', 'ELF(+ 5 DEX)')]
    race = forms.ChoiceField(choices=RACE, widget=forms.RadioSelect)
    # random points to distribute
    points = random.randint(10, 30)

    class Meta:
        model = Hero
        fields = '__all__'
        exclude = ('HP', 'LVL')

    def clean(self):
        cleaned_data = super().clean()
        DMG = cleaned_data['DMG']
        DEX = cleaned_data['DEX']
        DEF = cleaned_data['DEF']
        current_points = DMG + DEX + DEF
        if current_points > self.points:
            raise forms.ValidationError(f"Hey there is limit for your points. "
                                        f"\nSubtract {current_points - self.points} points from your statistics")
        elif current_points < self.points:
            raise forms.ValidationError(f"Hey you have undistributed {self.points - current_points} points.")


# class AvatarCreation(forms.Form):
#     # creates avatar
#     class Meta():
#         model =
#     RACE = [('human', 'HUMAN(+ 5 DMG)'), ('orc', 'ORC(+ 5 HP)'), ('elf', 'ELF(+ 5 DEF)')]
#     name = forms.CharField(max_length=15)
#     race = forms.ChoiceField(choices=RACE, widget=forms.RadioSelect)
#     DMG = forms.IntegerField(validators=[validate_zero])
#     HP = forms.IntegerField(validators=[validate_zero])
#     DEF = forms.IntegerField(validators=[validate_zero])
#     # random points to distribute
#     points = random.randint(10, 30)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         DMG = cleaned_data['DMG']
#         HP = cleaned_data['HP']
#         DEF = cleaned_data['DEF']
#         current_points = DMG + HP + DEF
#         if current_points > self.points:
#             raise forms.ValidationError(f"Hey there is limit for your points. "
#                                         f"\nSubtract {current_points - self.points} points from your statistics")
#         elif current_points < self.points:
#             raise forms.ValidationError(f"Hey you have undistributed {self.points - current_points} points.")
