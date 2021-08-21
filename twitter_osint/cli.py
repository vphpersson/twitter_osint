from enum import Enum
from typing import Optional, Final
from asyncio import gather as asyncio_gather
from datetime import datetime
from urllib.parse import urljoin

from httpx import AsyncClient as HTTPXAsyncClient
from tabulate import tabulate
from twitter_api.cli import TwitterApiArgumentParser, twitter_api, TwitterApiAction
from twitter_api.calls import get_friend_ids, get_follower_ids, lookup_users, show_user, TWITTER_API_URL
from twitter_api.structures import User, IdsResult

from twitter_osint import cursor_id_to_datetime

NUM_FIRST_FOLLOWERS: Final[int] = 5


class TwitterOISNTAction(Enum):
    INTERSECTION = 'intersection'
    FIRST_FOLLOWERS = 'first_followers'
    CREATION = 'creation'


class TwitterOSINTArgumentParser(TwitterApiArgumentParser):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **(
                dict(
                    description='Perform OSINT actions using the Twitter API.'
                )
                | kwargs
            )
        )

        action_action = next(action for action in self._actions if action.dest == 'action')
        action_action.choices = list(action_action.choices) + [member.value for member in TwitterOISNTAction]


async def twitter_osint(
    http_client: HTTPXAsyncClient,
    action: str,
    user_id: Optional[str],
    screen_name: Optional[str]
) -> Optional[str]:
    """
    Perform an OSINT action using the Twitter API.

    The action is not an OSINT action but rather an action specified in the `twitter_api` library, it is used instead.

    :param http_client: An HTTP client with which to perform the API requests.
    :param action: The action to be performed.
    :param user_id: The user ID of the user to be examined.
    :param screen_name: The screen name of the user to be examined.
    :return: Optional output from the chosen API calls.
    """

    if action in {member.value for member in TwitterApiAction}:
        return await twitter_api(
            http_client=http_client,
            action=action,
            user_id=user_id,
            screen_name=screen_name
        )
    elif action == 'intersection':
        friend_ids, follower_ids = await asyncio_gather(
            get_friend_ids(http_client=http_client, user_id=user_id, screen_name=screen_name, follow_cursor=True),
            get_follower_ids(http_client=http_client, user_id=user_id, screen_name=screen_name, follow_cursor=True)
        )

        friend_ids: set[int] = set(friend_ids)
        follower_ids: set[int] = set(follower_ids)

        return '\n'.join(
            user.screen_name
            for user in await lookup_users(http_client=http_client, user_ids=friend_ids.intersection(follower_ids))
        )
    elif action == 'first_followers':
        user_ids: list[int] = []
        user_cursors: list[int] = []

        cursor = -2
        while len(user_ids) < NUM_FIRST_FOLLOWERS and cursor != 0:
            response = await http_client.get(
                url=urljoin(TWITTER_API_URL, 'followers/ids.json'),
                params={
                    key: value
                    for key, value in [
                        ('user_id', user_id),
                        ('screen_name', screen_name),
                        ('cursor', cursor),
                        ('count', 1)
                    ]
                    if value is not None
                }
            )
            response.raise_for_status()

            ids_result = IdsResult.from_json(json_object=response.json())

            user_ids.extend(ids_result.ids)
            user_cursors.append(ids_result.next_cursor)

            cursor = ids_result.previous_cursor

        users: tuple[User, ...] = await lookup_users(http_client=http_client, user_ids=user_ids)

        return tabulate(
            tabular_data=[
                (
                    user.screen_name,
                    user.name,
                    str(datetime.strptime(user.created_at, '%a %b %d %H:%M:%S %z %Y')),
                    str(cursor_id_to_datetime(cursor_id=user_cursor)),
                )
                for user, user_cursor in zip(users, user_cursors)
            ],
            headers=('Screen name', 'Name', 'Created', '~Follow date')
        )
    elif action == 'creation':
        return (await show_user(http_client=http_client, user_id=user_id, screen_name=screen_name)).created_at
    else:
        raise ValueError(f'Unsupported action: {action}')
