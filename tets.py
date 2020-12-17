import unittest

import vk

from vkapi.user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        with open('test_token.txt', 'r') as f:
            token = f.readline().rstrip()
        session = vk.Session(token)
        self.api = vk.API(session)
        self.v = "5.126"

    def test_getUserInfo(self):
        user = User("5.126", self.api, "278714389")
        user.getUserInfo()
        fields = ["photo_id", "verified", "sex", "bdate", "city", "country", "home_town", "has_photo", "photo_50",
                  "photo_100", "photo_200_orig", "photo_200", "photo_400_orig", "photo_max", "photo_max_orig", "online",
                  "domain", "has_mobile", "contacts", "site", "education", "universities", "schools", "status",
                  "last_seen", "followers_count", "common_count", "occupation", "nickname", "relatives", "relation",
                  "personal", "connections", "exports", "activities", "interests", "music", "movies", "tv", "books",
                  "games", "about", "quotes", "can_post", "can_see_all_posts", "can_see_audio",
                  "can_write_private_message", "can_send_friend_request", "is_favorite", "is_hidden_from_feed",
                  "timezone", "screen_name", "maiden_name", "crop_photo", "is_friend", "friend_status", "career",
                  "military", "blacklisted", "blacklisted_by_me", "can_be_invited_group"]
        data = self.api.users.get(user_ids=["278714389"], fields=fields, v=self.v)[0]
        self.assertEqual(user.id, data['id'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.is_closed, data['is_closed'])
        self.assertEqual(user.can_access_closed, data['can_access_closed'])


if __name__ == '__main__':
    unittest.main()
