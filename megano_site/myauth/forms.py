"""
Форма для профилей пользователей, подключение аватарок
"""
from django.forms import ModelForm
from .models import Profile


class ProfileForm(ModelForm):
    """Форма профиля - подключение аватара"""
    class Meta:
        model = Profile
        fields = ["avatar", "phone"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
