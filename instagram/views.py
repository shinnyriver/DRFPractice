from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer
from .models import Post


# class PublicPostListAPIView(generics.ListAPIView):
#     queryset = Post.objects.all().filter(is_public=True)
#     serializer_class = PostSerializer
#


# class PublicPostListAPIView(APIView): # by CBV
#     def get(self, request):
#         qs = Post.objects.filter(is_public=True)
#         serializer = PostSerializer(qs, many=True)
#         return Response(serializer.data)
#
#
# public_post_list = PublicPostListAPIView.as_view()


@api_view(["GET"])  # by FBV
def public_post_list(request):
    qs = Post.objects.filter(is_public=True)
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=["GET"])
    def public(self, request):
        qs = self.get_queryset().filter(is_public=True)
        serializer = self.get_serializer(qs, many=True)
        # serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["PATCH"])
    def set_public(self, request, pk):
        instance = self.get_object()
        instance.is_public = True
        instance.save(update_fields=["is_public"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# def post_list(request):   #원래는 이런 식으로 구현해야 함
#     pass
#
# def post_detial(request, pk):
#     pass


# @csrf_exempt
# def post_list(request):
#     pass


def post_list(request):
    pass


post_list = csrf_exempt(post_list)  # 교차 컴포넌트 (Higher Order Component)
