from django.urls import resolve

from feed.models import ServiceFeed


def get_viewed_qs(request):
    return (
        ServiceFeed.objects.filter(type=ServiceFeed.Type.VIEWED)
        .filter(user=request.user)
        .first()
    )


def queue_mark_viewed(get_response):
    def try_mark_as_temp_viewed(request, pk):
        viewed_qs = get_viewed_qs(request)
        if viewed_qs:
            viewed_qs.feed_items.add(pk)

    def get_processed_response(request):
        resolved = resolve(request.path)
        if resolved.url_name == "api_feed_detail":
            try_mark_as_temp_viewed(request, resolved.kwargs.get("pk"))
        return get_response(request)

    def middleware(request):
        if request.user.is_authenticated:
            return get_processed_response(request)
        return get_response(request)

    return middleware


def get_viewed(get_response):
    def try_process_viewed_session(request, url_name):
        session_key = f"viewed_{request.path}"

        if session_key not in request.session:
            for key in request.session.keys():
                if key.startswith("viewed_"):
                    request.session.delete(key)
            request.session[session_key] = []
            viewed = get_viewed_qs(request)
            if viewed:
                for item in viewed.feed_items.all():
                    request.session[session_key].append(item.pk)

    def get_processed_response(request):
        resolved = resolve(request.path)
        if resolved.url_name != "api_feed_detail":
            try_process_viewed_session(request, resolved.url_name)
        return get_response(request)

    def middleware(request):
        if request.user.is_authenticated:
            return get_processed_response(request)
        return get_response(request)

    return middleware
