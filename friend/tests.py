import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import User

# Create your tests here.
ACCEPT_STATUS = "A"
REJECT_STATUS = "R"
UNFRIEND_STATUS = "R"
class FriendTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@email.com", username="user1", password="passqweruser1",
        )
        self.token1 = Token.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(
            email="user2@email.com", username="user2", password="passqweruser2",
        )
        self.token2 = Token.objects.create(user=self.user2)

        self.user3 = User.objects.create_user(
            email="user3@email.com", username="user3", password="passqweruser3",
        )
        self.token3 = Token.objects.create(user=self.user3)
        
    def test_send_get_friend_request(self):
        #send friend request from user1 to user2
        request_body = {
            "f2Id": "user2",
        }
        response = self.client.post(
            "/api/friend/friend_request/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #send friend request from user3 to user2
        request_body = {
            "f2Id": "user2",
        }
        response = self.client.post(
            "/api/friend/friend_request/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token3.key,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #get friend request list for user2
        response = self.client.get(
            "/api/friend/friend_request/",
            HTTP_AUTHORIZATION="Token " + self.token2.key,
        )
        data = json.loads(json.dumps(response.data))
        self.assertEqual(data[0]["f1Id"], self.user1.username)
        self.assertEqual(data[1]["f1Id"], self.user3.username)

    def test_accept_friend_request(self):
        #send friend request from user1 to user2
        request_body = {
            "f2Id": "user2",
        }
        response = self.client.post(
            "/api/friend/friend_request/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #user 2 accept the friend request from the user 1
        request_body = {
            "f1Id" : "user1",
            "status" : ACCEPT_STATUS
        }

        data = json.loads(json.dumps(response.data))
        friend_request_id = data['id']
        response = self.client.patch(
            f"/api/friend/friend_request/{friend_request_id}/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token2.key,
        )
        data = json.loads(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["f1Id"], self.user1.username)
        self.assertEqual(data["f2Id"], self.user2.username)
        self.assertEqual(data["status"], ACCEPT_STATUS)

    def test_reject_friend_request(self):
        #send friend request from user1 to user2
        request_body = {
            "f2Id": "user2",
        }
        response = self.client.post(
            "/api/friend/friend_request/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #user 2 reject the friend request from the user 1
        request_body = {
            "f1Id" : "user1",
            "status" : REJECT_STATUS
        }

        data = json.loads(json.dumps(response.data))
        friend_request_id = data['id']
        response = self.client.patch(
            f"/api/friend/friend_request/{friend_request_id}/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token2.key,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_unfriend(self):
        #send friend request from user1 to user2
        request_body = {
            "f2Id": "user2",
        }
        response = self.client.post(
            "/api/friend/friend_request/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #user 2 accept the friend request from the user 1
        request_body = {
            "f1Id" : "user1",
            "status" : ACCEPT_STATUS
        }

        data = json.loads(json.dumps(response.data))
        friend_id = data['id']
        response = self.client.patch(
            f"/api/friend/friend_request/{friend_id}/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token2.key,
        )

        #user 1 unfriend user2
        request_body = {
            "f1Id" : "user2",
            "status" : UNFRIEND_STATUS
        }

        response = self.client.patch(
            f"/api/friend/my_friends/{friend_id}/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_if_friend(self):
        #user1 has not sent friend request to user2
        response = self.client.get(
            f"/api/friend/if_friend/{self.user2.username}/",
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        data = json.loads(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['status'], "unfriend")

        #send friend request from user1 to user2
        request_body = {
            "f2Id": "user2",
        }
        response = self.client.post(
            "/api/friend/friend_request/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        data = json.loads(json.dumps(response.data))
        friend_id = data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #user1 is pending user2 to process the friend request
        response = self.client.get(
            f"/api/friend/if_friend/{self.user2.username}/",
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        data = json.loads(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['status'], "pending")

        #user 2 accept the friend request from the user 1
        request_body = {
            "f1Id" : "user1",
            "status" : ACCEPT_STATUS
        }

        response = self.client.patch(
            f"/api/friend/friend_request/{friend_id}/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token2.key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #user1 has been friend with user2
        response = self.client.get(
            f"/api/friend/if_friend/{self.user2.username}/",
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        data = json.loads(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['status'], "friend")

