from django import forms
from .models import Player
from .validators import validate_password


class PlayerForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        validators=[validate_password]
    )
    correct_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Повтор пароля'})
    )

    class Meta:
        model = Player
        fields = ['nickname']  # Только поля модели, остальные - дополнительные

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        correct_password = cleaned_data.get('correct_password')

        if password and correct_password and password != correct_password:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        player = super().save(commit=False)
        player.set_password(self.cleaned_data['password'])
        if commit:
            player.save()

        return player
