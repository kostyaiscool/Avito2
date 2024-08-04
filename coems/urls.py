from rest_framework.routers import SimpleRouter

from coems.views import ProductViewSet, CategoryViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'product', ProductViewSet, basename='products')
router.register(r'category', CategoryViewSet, basename='categories')
urlpatterns = [
    *router.urls
]