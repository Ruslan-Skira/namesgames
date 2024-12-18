from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class UserDetailView(APIView):  # pragma: no cover
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"email": request.user.email})
