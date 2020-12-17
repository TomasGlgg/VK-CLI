class Action:
    type = None
    member_id = None
    text = None
    email = None
    photo = None


class Message:
    _id = None
    date = None
    peer_id = None
    from_id = None
    text = None
    random_id = None
    ref = None
    ref_source = None
    attachments = None
    important = None
    geo = None
    payload = None
    keyboard = None
    fwd_messages = None
    reply_message = None
    action = None
    admin_author_id = None
    conversation_message_id = None
    is_cropped = None
    members_count = None
    update_time = None
    was_listened = None
    pinned_at = None
