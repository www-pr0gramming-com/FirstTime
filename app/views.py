from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import A001, Agent, Category

from .forms import (
    LeadCategoryUpdateForm,
    LeadForm,
    LeadModelForm,
    CustomUserCreationForm,
    AssignAgentForm,
)

from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    FormView,
)

from django.urls import reverse

from django.core.mail import send_mail

from django.contrib.auth.mixins import LoginRequiredMixin

from app2.mixins import OrganisorAndLoginRequiredMixin


from django.contrib import messages


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = A001.objects.filter(
                organisation=user.userprofile, agent__isnull=False
            )
        else:
            queryset = A001.objects.filter(
                organisation=user.agent.organisation, agent__isnull=False
            )
            # filter
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        queryset = A001.objects.filter(
            organisation=user.userprofile, agent__isnull=True
        )
        context.update(
            {
                "unassigned_leads": queryset,
            }
        )

        return context


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = A001.objects.filter(organisation=user.userprofile)
        else:
            queryset = A001.objects.filter(organisation=user.agent.organisation)
            # filter
            queryset = queryset.filter(agent__user=user)

        return queryset


class LeadCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        # print(reverse("app:lead-list"))
        return reverse("app:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        # SEND EMAIl
        send_mail(
            subject="AAAAA",
            message="BBBBBBB",
            from_email="test@test.com",
            recipient_list=["test2@test2.com"],
        )
        messages.success(self.request, "message")
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = "leads/lead_update.html"
    context_object_name = "lead"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("app:lead-list")

    def get_queryset(self):
        user = self.request.user
        queryset = A001.objects.filter(organisation=user.userprofile)
        return queryset


class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"
    context_object_name = "lead"

    def get_success_url(self):
        return reverse("app:lead-list")

    def get_queryset(self):
        user = self.request.user
        queryset = A001.objects.filter(organisation=user.userprofile)
        return queryset


class AssignAgentView(OrganisorAndLoginRequiredMixin, FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update(
            {"request": self.request},
        )
        return kwargs

    def get_success_url(self):
        return reverse("app:lead-list")

    def form_valid(self, form):
        # form.save()
        # print(form.cleaned_data)
        agent = form.cleaned_data["agent"]
        lead = A001.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = A001.objects.filter(organisation=user.userprofile)

        else:
            queryset = A001.objects.filter(organisation=user.agent.organisation)

        context.update(
            {
                "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
            }
        )
        return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)

    #     # leads = A001.objects.filter(category=self.get_object())
    #     # leads = self.get_object().a001_set.all()
    #     leads = self.get_object().a001.all()

    #     context.update({"leads": leads})
    #     return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/lead_category_update.html"
    context_object_name = "lead"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = A001.objects.filter(organisation=user.userprofile)
        else:
            queryset = A001.objects.filter(organisation=user.agent.organisation)

            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_success_url(self):
        return reverse("app:lead-detail", kwargs={"pk": self.get_object().id})


# CRUD + List - Create, Retrieve, Update, and Delete + List

# class LandingView(TemplateView):
#     template_name = "landing.html"


# def landing(request):
#     return render(request, "landing.html")


# def lead_list(request):
#     # def home_page(request):
#     # return HttpResponse("hello world")
#     # a = A001.objects.first()
#     leads = A001.objects.all()
#     context = {
#         # "name": "john",
#         # "age": 35,
#         "leads": leads,
#     }

#     return render(request, "leads/lead_list.html", context)


# def lead_detail(request, pk):
#     print(pk)
#     detail = A001.objects.get(id=pk)

#     context = {
#         "lead": detail,
#     }

#     return render(request, "leads/lead_detail.html", context)


# def lead_create(request):
#     form = LeadModelForm()
#     if request.method == "POST":
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/app")
#     context = {"form": form}
#     return render(request, "leads/lead_create.html", context)


# def lead_update(request, pk):
#     lead = A001.objects.get(id=pk)
#     form = LeadModelForm(instance=lead)
#     if request.method == "POST":
#         form = LeadModelForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect("/app")
#     context = {
#         "form": form,
#         "lead": lead,
#     }
#     return render(request, "leads/lead_update.html", context)


# def lead_delete(request, pk):
#     lead = A001.objects.get(id=pk)
#     lead.delete()
#     return redirect("/app")


# def lead_update(request, pk):
#     lead = A001.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data["first_name"]
#             last_name = form.cleaned_data["last_name"]
#             age = form.cleaned_data["age"]
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect("/app")
#     context = {
#         "form": form,
#         "lead": lead,
#     }
#     return render(request, "leads/lead_update.html", context)


# def lead_create(request):
#     # print(request.POST)
#     form = LeadForm()
#     if request.method == "POST":
#         # print("OK 000001")
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             # print("OK 0000002")
#             # print(form.cleaned_data)
#             first_name = form.cleaned_data["first_name"]
#             last_name = form.cleaned_data["last_name"]
#             age = form.cleaned_data["age"]
#             agent = Agent.objects.first()
#             A001.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent,
#             )
#             return redirect("/app")
#     context = {"form": form}
#     return render(request, "leads/lead_create.html", context)
