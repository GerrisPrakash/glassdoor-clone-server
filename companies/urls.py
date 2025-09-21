from django.urls import path
from .views import (
    CompanyListCreateAPIView, CompanyDetailAPIView,
    JobListCreateAPIView, JobDetailAPIView,
    ReviewListCreateAPIView, ReviewDetailAPIView
)

urlpatterns = [
    # Companies
    path("companies/", CompanyListCreateAPIView.as_view(), name="company-list-create"),
    path("companies/<int:pk>/", CompanyDetailAPIView.as_view(), name="company-detail"),

    # Jobs
    path("jobs/", JobListCreateAPIView.as_view(), name="job-list-create"),
    path("jobs/<int:pk>/", JobDetailAPIView.as_view(), name="job-detail"),

    # Reviews
    path("reviews/", ReviewListCreateAPIView.as_view(), name="review-list-create"),
    path("reviews/<int:pk>/", ReviewDetailAPIView.as_view(), name="review-detail"),
]
