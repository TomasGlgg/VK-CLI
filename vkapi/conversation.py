class Peer:
    _id = None
    type = None
    local_id = None


class CanWrite:
    allowed = None
    reason = None


class ChatSettings:
    members_count = None
    title = None
    pinned_message = None
    state = None
    photo = None
    active_ids = None
    is_group_channel = None


class Conversation:
    peer = None
    in_read = None
    out_read = None
    unread_count = None
    important = None
    unanswered = None
    push_settings = None
    can_write = None
    chat_settings = None
