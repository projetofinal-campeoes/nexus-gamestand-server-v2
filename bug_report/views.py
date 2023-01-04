from rest_framework import generics
from .serializers import BugReportSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import BugReport
from .permissions import WriteOnlyOrAdmin

class BugReportView(generics.ListCreateAPIView):
    serializer_class = BugReportSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [WriteOnlyOrAdmin, IsAuthenticated]
    queryset = BugReport.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BugReportViewDetail(generics.DestroyAPIView):
    serializer_class = BugReportSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [WriteOnlyOrAdmin, IsAuthenticated]
    queryset = BugReport.objects.all()

