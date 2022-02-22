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
)

app_name = "app"


urlpatterns = [
    path("", LeadListView.as_view(), name="lead-list"),
    path("<int:pk>", LeadDetailView.as_view(), name="lead-detail"),
    path("<int:pk>/update/", LeadUpdateView.as_view(), name="lead-update"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="lead-delete"),
    path("create/", LeadCreateView.as_view(), name="lead-create"),
    path("<int:pk>/assign-agent/", AssignAgentView.as_view(), name="lead-assign"),
    path(
        "<int:pk>/category/",
        LeadCategoryUpdateView.as_view(),
        name="lead-category-update",
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
]
