from django import forms

from .models import A001, Agent, FollowUp


from django.contrib.auth.forms import UserCreationForm, UsernameField

from django.contrib.auth import get_user_model

User = get_user_model()

# from django.core.exceptions import ValidationError


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = A001
        fields = (
            "first_name",
            "last_name",
            "age",
            "agent",
            "description",
            "phone_number",
            "email",
            "profile_picture",
        )

    # def clean_first_name(self):
    #     data = self.cleaned_data["first_name"]
    #     if data != "john":
    #         raise ValidationError("Your name is not john")
    #     return data

    # def clean(self):
    #     first_name = self.cleaned_data["first_name"]
    #     last_name = self.cleaned_data["last_name"]

    #     if first_name + last_name != "john doe":
    #         raise ValidationError("Your name is not john doe")


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class AssignAgentForm(forms.Form):
    # agent = forms.ChoiceField(
    #     choices=(
    #         ("agent 1", "agent 1 full name"),
    #         ("agent 2", "agent 2 full name"),
    #     )
    # )

    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        # print(kwargs)
        request = kwargs.pop("request")
        # print(request.user)
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = A001
        fields = ("category",)


class FollowUpModelForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ("notes", "file")
