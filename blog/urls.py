from django.urls import path, include
from . import views

#Import statement for Fuunction Based API
# from .views import blog_list, details_list

# Import statement using class based APIView
# from .views import BlogAPIView, BlogDetailsAPIView

# Import statements using Generic class based APIView
# from .views import GenericBlogAPI


# Import statements for ViewSets
# from .views import BlogViewSet
from rest_framework.routers import DefaultRouter

# Import statement for Generic ViewSet
# from .views import GenericBlogViewSet

from .views import ModelBlogViewSet


# router for ViewSet
# router = DefaultRouter()
# router.register('', BlogViewSet, basename="blog_list")

# Router for Generic ViewSet
# router = DefaultRouter()
# router.register('', GenericBlogViewSet, basename="blog_list")


router = DefaultRouter()
router.register('', ModelBlogViewSet, basename="blog_list")


urlpatterns = [
    path('create', views.create, name="create"),
    path('post/<int:id>', views.post, name="post"),
    path('', views.home, name="home"),
    path('search', views.search, name="search"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('delete/<int:id>', views.delete, name="delete"),

    # Function Based API URLS
    # path('blog_list/', blog_list),
    # path('details_list/<int:id>/', details_list)

#     Class Based API URLS
#     path('blog_list/', BlogAPIView.as_view()),
#     path('details_list/<int:id>/', BlogDetailsAPIView.as_view())

    # # Generic class based URlS
    # path('blog_list/', GenericBlogAPI.as_view()),
    # path('blog_list/<int:id>/', GenericBlogAPI.as_view()),


    #  ViewSet based URLS
    # path('blog_list/', include(router.urls)),
    # path('blog_list/<int:pk>/', include(router.urls))


    path('blog_list/', include(router.urls)),
    path('blog_list/<int:pk>/', include(router.urls))

]
