from django import forms

from .models import A001, Agent


from django.contrib.auth.forms import UserCreationForm, UsernameField

from django.contrib.auth import get_user_model

User = get_user_model()


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
        )


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
