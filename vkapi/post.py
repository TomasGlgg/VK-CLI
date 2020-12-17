class Comments:
    count = None
    can_post = None
    groups_can_post = None
    can_close = None
    can_open = None


class Copyright:
    _id = None
    link = None
    name = None
    type = None


class Views:
    count = None


class Post:
    _id = None
    owner_id = None
    from_id = None
    created_by = None
    date = None
    text = None
    reply_owner_id = None
    reply_post_id = None
    friends_only = None
    comments = None
    copyright = None
    likes = None
    reposts = None
    views = None
    post_type = None
    post_source = None
    attachments = None
    geo = None
    signer_id = None
    copy_history = None
    can_pin = None
    can_delete = None
    can_edit = None
    is_pinned = None
    marked_as_ads = None
    is_favorite = None
    donut = None
    postponed_id = None
