from core.models import Config, Category
from django.core.cache import cache


def getItems():
    if "categories_all" in cache:
        queryset = cache.get("categories_all")
        return queryset
    else:
        queryset = Category.objects.all()
        cache.set("categories_all", queryset)
        return queryset


def getConfig():
    if "web-config" in cache:
        queryset = cache.get("web-config")
        return queryset
    else:
        queryset = Config.objects.first()
        cache.set("web-config", queryset)
        return queryset


# def getProfiles():
#     if "user-profiles" in cache:
#         queryset = cache.get("user-profiles")
#         return queryset
#     else:
#         queryset = UserProfile.objects.all()
#         cache.set("user-profiles", queryset)
#         return queryset


def context(request):
    return {
        'config': getConfig(),
        'categories': Category.objects.all(),
    }
