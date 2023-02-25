from django.urls import path, include, re_path

from rest_framework.routers import SimpleRouter

from .views import CreateCheckAPIView, ListCheckAPIView, RetrieveUpdateCheckAPIViewSet, PrintCheckAPIView

app_name = "core"


router = SimpleRouter()
router.register("check", RetrieveUpdateCheckAPIViewSet, basename="check")


api_url_patterns = [
    path(
        "point/<int:point_id>/",
        include(
            [
                path("check/", CreateCheckAPIView.as_view(), name="create-check"),
            ]
        ),
    ),
    path("printer/<int:printer_id>/check/", ListCheckAPIView.as_view(), name="check-list-by-printer"),
    re_path(r'^print/(?P<filename>[^/]+)$', PrintCheckAPIView.as_view(), name="print-check"),
]

urlpatterns = router.urls + api_url_patterns
