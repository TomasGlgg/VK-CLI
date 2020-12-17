class Thread:
    count = None
    items = None
    can_post = None
    show_reply_button = None
    groups_can_post = None


class Comment:
    _id = None
    from_id = None
    date = None
    text = None
    donut = None
    reply_to_user = None
    reply_to_comment = None
    attachments = None
    parents_stack = None
    thread = None
