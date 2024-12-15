from feed.views.feed import FeedView


class Subscription(FeedView):
    def get_regular_template_names(self):
        return "feed/subscription.html"

    def get_loader_template_names(self):
        return "blocks/feed/loaders/subscription.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "slug" in self.kwargs:
            slug = self.kwargs.get("slug")
            context["feed"] = self.model.objects.get(slug=slug)
        return context
