from django.urls import path

from .views import BugReportView, BugReportViewDetail

urlpatterns = [
    path("bug_report/", BugReportView.as_view()),
    path("bug_report/<uuid:pk>/", BugReportViewDetail.as_view()),
]
