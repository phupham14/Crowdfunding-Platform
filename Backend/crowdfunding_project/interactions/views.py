from django.shortcuts import render
from httpx import Response
from interactions.models import UserInteraction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# interactions/views.py

class TrackInteractionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        UserInteraction.objects.create(
            user=request.user,
            project_id=request.data["project_id"],
            interaction_type=request.data["type"],
            source=request.data.get("source")
        )
        return Response({"status": "ok"})