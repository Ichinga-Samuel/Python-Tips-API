from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import viewsets
from tips.models import Tips, Tags
from .serializer import TipsSerializer, TagsSerializer


class TipViewSet(viewsets.ModelViewSet):
    queryset = Tips.objects.all()
    serializer_class = TipsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TipsCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TipsSerializer


class TipsEditView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = TipsSerializer
    queryset = Tips.objects.all()


class TipsSearchView(generics.ListAPIView):
    serializer_class = TipsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        q = self.request.GET.get('q', 'python')
        # search query in tips
        res = Tips.objects.filter(Q(tip__iregex=r'.*%s.*' %q)|Q(tags__name__iregex=r'.*%s.*' %q))
        return [*{*res}]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
