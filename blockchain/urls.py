from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="BlockChain Voting System API",
        default_version="v1",
        description="API for BlockChain Voting System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nyamburanjorogejames@students.uonbi.ac.ke"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


from . import views

urlpatterns = [
    # api docs
    path(
        "api/v1/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
