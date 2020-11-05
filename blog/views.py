from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError

from .models import Blog
from .forms import BlogForm


# Create your views here.

def home(request):

    all_posts = Blog.objects.all()

    return render(request, 'home.html', {'all_posts':all_posts})


def create(request):

    if request.method == "POST":
        form = BlogForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Blog published successfully!")
            return redirect('home')
        else:
            messages.info(request, "Blog not published!")
            return render(request, 'create.html')

    else:
        print("HI")
        return render(request, 'create.html')


def post(request, id):

    desc = Blog.objects.filter(pk=id)
    return render(request, 'post.html', {'desc':desc})


def search(request):
    try:
        query = request.GET['query']
    except MultiValueDictKeyError:
        query = False

    desc = Blog.objects.filter(title__icontains=query)

    if Blog.objects.filter(title__icontains=query).exists():
        return render(request, 'post.html', {'desc':desc})


def edit(request, id):

    if request.method == "POST":

        eitem = Blog.objects.get(pk=id)
        form = BlogForm(request.POST or None, instance=eitem)

        if form.is_valid():
            form.save()
            messages.success(request, "Blog edited successfully!")
            return redirect('home')
        else:
            messages.info(request, "Blog not edited!")
            return render(request, 'edit.html')

    else:
        eitem = Blog.objects.get(pk=id)
        return render(request, 'edit.html', {'eitem':eitem})


def delete(request, id):

    ditem = Blog.objects.get(pk=id)
    ditem.delete()
    messages.success(request, "post deleted successfully!")
    return redirect('home')


from .serializers import BlogSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


class ModelBlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()


#  Generic ViewSets
# class GenericBlogViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
#                          mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
#     serializer_class = BlogSerializer
#     queryset = Blog.objects.all()


#  ViewSet
# class BlogViewSet(viewsets.ViewSet):
#
#     def list(self, request):
#         blog_posts = Blog.objects.all()
#         serializer = BlogSerializer(blog_posts, many=True)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = BlogSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self, request, pk=None):
#         queryset= Blog.objects.all()
#         blog_post = get_object_or_404(queryset, pk=pk)
#         serializer = BlogSerializer(blog_post)
#         return Response(serializer.data)
#
#     def update(self, request, pk=None):
#         article = Blog.objects.get(pk=pk)
#         serializer = BlogSerializer(article, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def destroy(self, request, pk=None):
#         article = Blog.objects.get(pk=pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# GenericAPI
# class GenericBlogAPI(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
#                      mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
#     serializer_class = BlogSerializer
#     queryset = Blog.objects.all()
#
#     lookup_field = 'id'
#
#         # SessionAuthentication and BasicAuthentication usage
#         # authentication_classes = [SessionAuthentication, BasicAuthentication]
#         # TokenAuthentication usage
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self,request, id=None):
#
#         if id:
#             return self.retrieve(request)
#         else:
#             return self.list(request, id)
#
#     def post(self, request):
#         return self.create(request)
#
#     def put(self, request, id=None):
#         return self.update(request, id)
#
#     def delete(self, request, id):
#         return self.destroy(request, id)


#Class Based APIview
# class BlogAPIView(APIView):
#
#     def get(self, request):
#         blog_posts = Blog.objects.all()
#         serializer = BlogSerializer(blog_posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = BlogSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Class Based APIview
# class BlogDetailsAPIView(APIView):
#
#     def get_obj(self, id):
#         try:
#             return Blog.objects.get(pk=id)
#         except Blog.DoesNotExist:
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#     def get(self, request, id):
#         article = self.get_obj(id)
#         serializer = BlogSerializer(article)
#         return Response(serializer.data)
#
#     def put(self, request, id):
#         article = self.get_obj(id)
#         serializer = BlogSerializer(article, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id):
#         article = self.get_obj(id)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# Function Based API using Decorators
# @api_view(['GET', 'POST'])
# def blog_list(request):
#
#     if request.method=="GET":
#         blog_posts = Blog.objects.all()
#         serializer = BlogSerializer(blog_posts, many=True)
#         return Response(serializer.data)
#
#     elif request.method=="POST":
#         serializer = BlogSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Function Based API
# @csrf_exempt
# def blog_list(request):
#
#     if request.method=="GET":
#         blog_posts = Blog.objects.all()
#         serializer = BlogSerializer(blog_posts, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method=="POST":
#         data = JSONParser().parse(request)
#         serializer = BlogSerializer(data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#
#         return JsonResponse(serializer.errors, status=400)


# Function Based API using Decorators
# @api_view(['GET', 'PUT', 'DELETE'])
# def details_list(request, id):
#     try:
#         article = Blog.objects.get(pk=id)
#     except Blog.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method=="GET":
#         serializer = BlogSerializer(article)
#         return Response(serializer.data)
#
#     elif request.method=="PUT":
#         serializer = BlogSerializer(article, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method=="DELETE":
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#Function Based API
# @csrf_exempt
# def details_list(request, id):
#        try:
#          article = Blog.objects.get(pk=id)
#        except Blog.DoesNotExist:
#          return HttpResponse(status=404)
#
#     if request.method=="GET":
#         serializer = BlogSerializer(article)
#         return JsonResponse(serializer.data)
#
#     elif request.method=="PUT":
#         data = JSONParser().parse(request)
#         serializer = BlogSerializer(article, data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method=="DELETE":
#         article.delete()
#         return HttpResponse(status=204)

    # To render remaining existed list
    #
    # blog_posts = Blog.objects.all()
    # serializer = BlogSerializer(blog_posts, many=True)
    # return JsonResponse(serializer.data, safe=False, status=204)


