import rules


@rules.predicate
def is_feed_owner(user, feed):
    return feed.created_by == user
