import json
from pprint import pprint
from django.test import TestCase, RequestFactory
from django.shortcuts import render
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from user.models import User
from friend.models import Friend
from post.models import Post
from .models import Comment
from .views import CommentViewSet


class CommentTestCase(APITestCase):
    def setUp(self):
        """
        setup: user1, user2
        setup: post1 by user1,  post2 by user2
        setup: friend(user1, user2)
        setup: comment1 for post1 by user2, comment 2 for post2 by user1, 
            comment 3 for post1 by user1.
        """
        self.user1 = User.objects.create_user(
            email="user1@email.com", username="user1", password="passqweruser1",
        )
        self.token1 = Token.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(
            email="user2@email.com", username="user2", password="passqweruser2",
        )
        self.token2 = Token.objects.create(user=self.user2)

        self.post1 = Post.objects.create(
            title="post1",
            content="this post1 from user1",
            author=self.user1,
            visibility="PUBLIC",
        )
        self.post2 = Post.objects.create(
            title="post2",
            content="this post2 from user2",
            author=self.user2,
            visibility="FRIENDS",
        )

        Friend.objects.create(f1Id=self.user1, f2Id=self.user2, status="A")

        self.comment1 = Comment.objects.create(
            content="this is comment1 for post1 by user2",
            post=self.post1,
            created_by=self.user2,
        )

        self.comment2 = Comment.objects.create(
            content="this is comment2 for post2 by user1",
            post=self.post2,
            created_by=self.user1,
        )

        self.comment3 = Comment.objects.create(
            content="this is comment3 for post1 by user1",
            post=self.post1,
            created_by=self.user1,
        )

    def test_create_comment(self):
        request_body = {
            "content": "test comment for post1 by user2",
        }

        response = self.client.post(
            f"/api/post/{str(self.post1.id)}/post_comment/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token2.key,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            f"/api/post/{str(self.post1.id)}/post_comment/", request_body,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comment(self):
        response = self.client.get(f"/api/post/{str(self.post1.id)}/get_comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/api/post/{str(self.post1.id)}/get_comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            f"/api/post/{str(self.post1.id)}/get_comments/",
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment(self):
        request_body = {
            "content": f"{self.comment1.content} updated",
        }

        response = self.client.patch(
            f"/api/comment/{str(self.comment1.id)}/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request_body = {
            "content": f"{self.comment1.content} updated",
        }

        response = self.client.patch(
            f"/api/comment/{str(self.comment1.id)}/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token2.key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment(self):
        response = self.client.delete(
            f"/api/comment/{str(self.comment3.id)}/",
            HTTP_AUTHORIZATION="Token " + self.token2.key,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(
            f"/api/comment/{str(self.comment3.id)}/",
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
