from rest_framework import routers

from core.limbo.viewsets import DependencyViewSet

router = routers.SimpleRouter()
router.register(r"dependencies", DependencyViewSet)
