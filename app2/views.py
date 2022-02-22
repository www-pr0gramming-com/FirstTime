from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from app.models import Agent

from django.urls import reverse

from .forms import AgentModelForm

from .mixins import OrganisorAndLoginRequiredMixin

from django.core.mail import send_mail

import random


class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("app2:agent-list")

    def form_valid(self, form):
        # agent = form.save(commit=False)
        # agent.organisaion = self.request.user.userprofile
        # agent.save()
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()

        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile,
        )

        send_mail(
            subject="エージェントに招待されました。",
            message="あなたはエージェントになりました。ログインが可能です。",
            from_email="admin@test.com",
            recipient_list=[user.email],
        )

        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("app2:agent-list")

    def get_queryset(self):
        return Agent.objects.all()


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("app2:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
