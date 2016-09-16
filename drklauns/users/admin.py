import random

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from slugify import slugify

from drklauns.users.utils import generate_temp_password
from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"), strip=False, )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password1'].initial = generate_temp_password()

    def save(self, commit=True):
        user = super().save(commit=False)

        while not user.username or User.objects.filter(username=user.username).count() > 0:
            if not user.username:
                user.username = slugify(user.full_name, only_ascii=True).replace("-", ".")
            else:
                user.username = "%s%s" % (user.username, random.randint(0, 9))

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_filter = ('is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'ssn', 'address', 'bank_account')}),
        (_('Contract'), {'fields': ('contract_no', 'contract_rate')}),
        (_('Permissions'), {'fields': ('is_active', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'password1' ),
        }),
    )
    list_display = ('username', 'name', 'is_superuser', 'is_active', 'ssn', 'contract_no', 'contract_rate')
    search_fields = ['name']
    readonly_fields = ('last_login', 'date_joined')

    def has_delete_permission(self, request, obj=None):
        return False
