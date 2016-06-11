import uuid
import datetime
import math
from itertools import islice
from numbers import Number
from collections import deque, defaultdict


class User:
    def __init__(self, full_name):
        self.__full_name = full_name
        self.__uuid = uuid.uuid4()
        self.__posts = deque(maxlen=50)

    @property
    def full_name(self):
        return self.__full_name

    @property
    def uuid(self):
        return self.__uuid

    def add_post(self, post_content):
        self.__posts.append(Post(self.__uuid, post_content))

    def get_post(self):
        return (post for post in self.__posts)

    def __str__(self):
        return "{}, [{}]".format(self.__full_name, self.__uuid)

    def __repr__(self):
        return str(self)


class Post:
    def __init__(self, author, content):
        self.__author = author
        self.__published_at = datetime.datetime.now()
        self.__content = content

    def __str__(self):
        return """Author: {}
                  Published at: {}
                  Content: {}""".format(self.__author,
                                        self.__published_at,
                                        self.__content)

    def __repr__(self):
        return str(self)

    @property
    def author(self):
        return self.__author

    @property
    def published_at(self):
        return self.__published_at

    @property
    def content(self):
        return self.__content


def check_if_users_exist(func):
    def checked_arguments(self, *args):
        for arg in args:
            if not isinstance(arg, Number) and arg not in self.users.keys():
                raise UserDoesNotExistError(arg)
        return func(self, *args)
    return checked_arguments


class SocialGraph:
    def __init__(self):
        self.__users = {}
        self.__graph = defaultdict(set)

    @property
    def users(self):
        return self.__users

    def add_user(self, user):
        if user.uuid in self.__users:
            raise UserAlreadyExistsError(user)
        self.__users[user.uuid] = user
        self.__graph[user.uuid]

    @check_if_users_exist
    def get_user(self, user_uuid):
        return self.__users[user_uuid]

    @check_if_users_exist
    def delete_user(self, user_uuid):
        del self.__users[user_uuid]
        del self.__graph[user_uuid]

    @check_if_users_exist
    def follow(self, follower, followee):
        if follower == followee:
            raise ValueError("User cannot follow himself!")
        self.__graph[follower].add(followee)

    @check_if_users_exist
    def unfollow(self, follower, followee):
        if follower == followee:
            raise ValueError("User cannot unfollow himself!")
        if self.is_following(follower, followee):
            self.__graph[follower].remove(followee)

    @check_if_users_exist
    def is_following(self, follower, followee):
        if follower == followee:
            raise ValueError("User cannot be following himself!")
        return followee in self.__graph[follower]

    @check_if_users_exist
    def followers(self, user_uuid):
        return set(follower for follower in self.__graph.keys()
                   if follower != user_uuid and
                   self.is_following(follower, user_uuid))

    @check_if_users_exist
    def following(self, user_uuid):
        return self.__graph[user_uuid]

    @check_if_users_exist
    def friends(self, user_uuid):
        return set(
            friend for friend in self.__graph[user_uuid]
            if self.is_following(friend, user_uuid))

    @check_if_users_exist
    def max_distance(self, user_uuid):
        max_distance_found = max(self.find_min_distances(user_uuid).values())
        return max_distance_found if max_distance_found != 0 else math.inf

    def find_min_distances(self, user_uuid):
        queue = []
        queue.append(user_uuid)
        # the dictionary maps destinations(other users)
        # with distances from user_uuid
        distances = defaultdict(int)
        visited = set()
        depth_counter = -1
        children_counter = 1

        while queue:
            depth_counter += 1
            new_children_counter = 0

            for _ in range(children_counter):
                current_elem = queue.pop(0)
                for child in self.__graph[current_elem]:
                    if child not in visited:
                        new_children_counter += 1
                        queue.append(child)

                if(distances[current_elem] == 0 or
                        distances[current_elem] > depth_counter):
                    distances[current_elem] = depth_counter
                visited.add(current_elem)
            children_counter = new_children_counter
        return distances

    @check_if_users_exist
    def min_distance(self, from_user_uuid, to_user_uuid):
        if from_user_uuid == to_user_uuid:
            return 0

        distances_found = self.find_min_distances(from_user_uuid)
        if to_user_uuid not in distances_found.keys():
            raise UsersNotConnectedError(from_user_uuid, to_user_uuid)

        return distances_found[to_user_uuid]

    @check_if_users_exist
    def nth_layer_followings(self, user_uuid, n):
        if n == 0:
            return set()
        elif n < 0:
            raise ValueError("Layer number must be at least 0!" +
                             "Yours was {}.".format(n))

        max_distances_found = self.find_min_distances(user_uuid)
        nth_layer = set([destination
                        for destination, distance in
                        max_distances_found.items() if distance == n])
        return nth_layer

    @check_if_users_exist
    def generate_feed(self, user_uuid, offset=0, limit=10):
        if offset < 0:
            raise ValueError("Offset index must be a positive number!" +
                             " Yours was {}".format(offset))
        elif limit < 0:
            raise ValueError("Limit index must be a positive number!" +
                             " Yours was {}".format(limit))

        all_posts = []
        for followee in self.__graph[user_uuid]:
            all_posts.extend(self.__users[followee].get_post())

        sorted_by_date = sorted(all_posts,
                                key=lambda post: post.published_at,
                                reverse=True)
        return islice(sorted_by_date, offset, offset + limit)


class UserDoesNotExistError(Exception):
    def __init__(self, uuid):
        self.message = "User with uuid [{}] does not exist!".format(uuid)

    def __str__(self):
        return self.message


class UserAlreadyExistsError(Exception):
    def __init__(self, user):
        self.message = "User {} alredy exists!".format(user)

    def __str__(self):
        return self.message


class UsersNotConnectedError(Exception):
    def __init__(self, from_user_uuid, to_user_uuid):
        self.message = """There is no possible path
        between user [{}] and user [{}]""".format(from_user_uuid, to_user_uuid)

    def __str__(self):
        return self.message
