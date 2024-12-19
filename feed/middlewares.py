from django.urls import resolve

from feed.models import FeedItemAction


def get_viewed_qs(request):
    return FeedItemAction.objects.filter(type=FeedItemAction.Type.VIEW).filter(
        user=request.user
    )


def queue_mark_viewed(get_response):
    def try_mark_as_temp_viewed(request, pk):
        actions_qs = get_viewed_qs(request).filter(feed_item_id=pk)

        if not actions_qs.exists():
            FeedItemAction(
                user=request.user, type=FeedItemAction.Type.VIEW, feed_item_id=pk
            ).save()

    def get_processed_response(request):
        resolved = resolve(request.path)
        if resolved.url_name == "api_feed_detail":
            try_mark_as_temp_viewed(request, resolved.kwargs.get("pk"))
        return get_response(request)

    def middleware(request):
        is_admin_request = request.path.startswith("/admin/")
        if request.user.is_authenticated and is_admin_request:
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
            for item in viewed.all():
                request.session[session_key].append(item.pk)

    def get_processed_response(request):
        resolved = resolve(request.path)
        if resolved.url_name != "api_feed_detail":
            try_process_viewed_session(request, resolved.url_name)
        return get_response(request)

    def middleware(request):
        is_admin_request = request.path.startswith("/admin/")
        if request.user.is_authenticated and not is_admin_request:
            return get_processed_response(request)
        return get_response(request)

    return middleware
