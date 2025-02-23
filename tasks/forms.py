from .models import TextTasks, EntryTasks, ExitTasks, KontragentTasks, DeliveryTasks
from django.forms import ModelForm, TextInput, DateInput, Textarea, TimeInput, CharField, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, SetPasswordForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class TextTasksForm(ModelForm):
    class Meta:
        model = TextTasks
        fields = ['title', 'full_text', 'date', 'time']

        widgets = {
            'title': TextInput(attrs={
                'class': 'text-task-form',
                'placeholder': 'Заголовок...'
            }),

            'full_text': Textarea(attrs={
                'class': 'text-task-form',
                'placeholder': 'Текст задачи...'
            }),

            'date': DateInput(attrs={
                'class': 'text-task-form',
                'placeholder': 'Дата публикации'
            }),

            'time': TimeInput(attrs={
                'class': 'text-task-form',
                'placeholder': 'Время публикации'
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        task = super().save(commit=False)
        task.author = self.user
        if commit:
            task.save()
        return task

class EntryTasksForm(ModelForm):
    class Meta:
        model = EntryTasks
        fields = ['number_auto', 'marka_auto', 'name_organization', 'date', 'time', 'description', 'is_allowed']

        widgets = {
            'number_auto': TextInput(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Введите Гос.Номер авто'
            }),

            'marka_auto': TextInput(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Введите марку авто'
            }),

            'name_organization': TextInput(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Введите название организации'
            }),

            'date': DateInput(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Дата вьезда'
            }),

            'time': TimeInput(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Время вьезда'
            }),

            'description': Textarea(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Дополнительная информация...'
            }),

        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        task = super().save(commit=False)
        task.author = self.user
        if commit:
            task.save()
        return task
    
class ExitTasksForm(ModelForm):
    class Meta:
        model = ExitTasks
        fields = ['number_auto', 'marka_auto', 'name_organization', 'date', 'time', 'description', 'is_allowed']

        widgets = {
            'number_auto': TextInput(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Введите Гос.Номер авто'
            }),

            'marka_auto': TextInput(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Введите марку авто'
            }),

            'name_organization': TextInput(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Введите название организации'
            }),

            'date': DateInput(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Дата вьезда'
            }),

            'time': TimeInput(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Время вьезда'
            }),

            'description': Textarea(attrs={
                'class': 'entry-task-form',
                'placeholder': 'Дополнительная информация...'
            }),

        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        task = super().save(commit=False)
        task.author = self.user
        if commit:
            task.save()
        return task
    
class KontragentTasksForm(ModelForm):
    class Meta:
        model = KontragentTasks
        fields = ['number_auto', 'description']

        widgets = {
            'number_auto': TextInput(attrs={
                'class': 'kontragent-field',
                'placeholder': 'Введите Гос.Номер авто'
            }),

            'description': Textarea(attrs={
                'class': 'kontragent-field',
                'placeholder': 'Дополнительная информация...'
            }),

        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        task = super().save(commit=False)
        task.author = self.user
        if commit:
            task.save()
        return task
    
class DeliveryTasksForm(ModelForm):
    class Meta:
        model = DeliveryTasks
        fields = ['number_auto', 'description']

        widgets = {
            'number_auto': TextInput(attrs={
                'class': 'kontragent-field',
                'placeholder': 'Введите Гос.Номер авто'
            }),

            'description': Textarea(attrs={
                'class': 'kontragent-field',
                'placeholder': 'Дополнительная информация...'
            }),

        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        task = super().save(commit=False)
        task.author = self.user
        if commit:
            task.save()
        return task

class CustomProfileChangeForm(UserChangeForm):
    password = None  # Убираем стандартное поле пароля

    class Meta:
        model = User
        fields = ['username']  # Только имя пользователя

class CombinedProfileChangeForm(SetPasswordForm, CustomProfileChangeForm):
    # Добавляем свое поле для ввода текущего пароля
    current_password = CharField(
        label=_("Текущий пароль"),
        widget=PasswordInput(attrs={'autocomplete': 'current-password',
                                    'class': 'form-control',
                                    'placeholder': 'Введите текущий пароль...'}),
        strip=False,
    )

    def clean_current_password(self):
        # Проверка правильности введенного текущего пароля.

        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise ValidationError(_("Неверный текущий пароль."))
        return current_password

    def __init__(self, user, *args, **kwargs):
        super().__init__(user=user, *args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        
        # Если новый пароль был введен, сохраняем его
        if self.cleaned_data.get('new_password1'):
            user.set_password(self.cleaned_data['new_password1'])
            
        if commit:
            user.save()
        return user
    
    username = CharField(
        max_length=100,
        widget= TextInput(attrs={'class': 'form-control',
                                 'placeholder': 'Введите новое имя пользователя...'})
    )

    new_password1 = CharField(
        label='Введите новый пароль',
        max_length=100,
        widget=PasswordInput(attrs={'class': 'form-control',
                                    'placeholder': 'Введите новый пароль...'})
    )
    new_password2 = CharField(
        label='Подтвердите новый пароль',
        max_length=100,
        widget=PasswordInput(attrs={'class': 'form-control',
                                    'placeholder': 'Подтвердите новый пароль...'})
    )

class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите имя сотрудника...'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите пароль сотрудника...'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтвердите пароль сотрудника...'})
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите новое имя сотрудника...'})
    
    new_password1 = CharField(
        label='Новый пароль',
        required=False,
        help_text='Оставьте пустым, если не хотите менять пароль.',
        max_length=100,
        widget=PasswordInput(attrs={'class': 'form-control',
                                    'placeholder': 'Введите новый пароль сотрудника...'})
    )
    new_password2 = CharField(
        label='Подтвердите новый пароль',
        required=False,
        help_text='Введите тот же самый пароль для подтверждения.',
        max_length=100,
        widget=PasswordInput(attrs={'class': 'form-control',
                                    'placeholder': 'Подтвердите новый пароль сотрудника...'})
    )
        
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if bool(password1) != bool(password2):
            raise ValidationError("Пожалуйста, введите новый пароль и подтвердите его.")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["new_password1"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user