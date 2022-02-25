from django.urls import path
from .views import (
    LeadListView,
    LeadCreateView,
    LeadDetailView,
    LeadUpdateView,
    LeadDeleteView,
    AssignAgentView,
    CategoryListView,
    CategoryDetailView,
    LeadCategoryUpdateView,
    LeadJsonView,
    FollowUpCreateView,
    FollowUpUpdateView,
    FollowUpDeleteView,
)

app_name = "app"


urlpatterns = [
    path("", LeadListView.as_view(), name="lead-list"),
    path("json/", LeadJsonView.as_view(), name="lead-list-json"),
    path("<int:pk>", LeadDetailView.as_view(), name="lead-detail"),
    path("<int:pk>/update/", LeadUpdateView.as_view(), name="lead-update"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="lead-delete"),
    path("<int:pk>/assign-agent/", AssignAgentView.as_view(), name="lead-assign"),
    path(
        "<int:pk>/category/",
        LeadCategoryUpdateView.as_view(),
        name="lead-category-update",
    ),
    path(
        "<int:pk>/followups/create/",
        FollowUpCreateView.as_view(),
        name="lead-followup-create",
    ),
    path(
        "followups/<int:pk>/", FollowUpUpdateView.as_view(), name="lead-followup-update"
    ),
    path(
        "followups/<int:pk>/delete/",
        FollowUpDeleteView.as_view(),
        name="lead-followup-delete",
    ),
    path("create/", LeadCreateView.as_view(), name="lead-create"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
]
