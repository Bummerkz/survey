from django.conf.urls import include, url

from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from polls.views import PollViewSet, QuestionViewSet, SurveyViewSet


schema = get_schema_view(
   openapi.Info(
      title='API',
      description='Survey app',
      default_version='1'
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'polls', PollViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'survey', SurveyViewSet)

urlpatterns = [
    url(r'^docs/$', schema.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api/', include((router.urls, 'api'), namespace='api')),
]
