from abc import abstractmethod, ABC

import aiohttp
import discord
from enum import Enum
from tot_message import TotMessage
from utils import send_discord_message, Location, Channel

from typing import Optional, Dict


class ReactionType(Enum):
    DISCORD_HERALD = "discord"


class Reaction(ABC):

    def __init__(self, name, location: Location, keyphrase: str, channel: int, radius: int = 50):
        self.name = name
        self.location = location
        self.radius = radius
        self.keyphrase = keyphrase
        self.channel = Channel(channel)

    def should_handle(self, tot_message: TotMessage):
        message_location = tot_message.location
        return self.keyphrase in tot_message.message and \
            self.channel == tot_message.channel and \
            self.radius < self.location.compute_distance_l2(message_location)

    @abstractmethod
    async def handle_message(self, tot_message: TotMessage):
        pass


class DiscordMessageReaction(Reaction):

    def __init__(self,
                 name: str,
                 keyphrase: str,
                 radius: int,
                 url: str,
                 channel: int,
                 prefix_message: str,
                 postfix_message: str,
                 location: Location):

        super().__init__(name=name, location=location, channel=channel, keyphrase=keyphrase, radius=radius)
        self.session: Optional[aiohttp.ClientSession] = None
        self.webhook: Optional[discord.Webhook] = None
        self.prefix = prefix_message
        self.postfix = postfix_message
        self.url = url

    @staticmethod
    def process_message(tot_message: TotMessage) -> str:
        return tot_message.character

    async def handle_message(self, tot_message: TotMessage):
        if not self.should_handle(tot_message):
            return

        if self.webhook is None:
            await self.create_webhook(self.url)

        message = f"{self.prefix} {self.process_message(tot_message)} {self.postfix}"
        await send_discord_message(self.webhook, message, username=self.name)

    async def create_webhook(self, url):
        self.session = aiohttp.ClientSession()
        self.webhook = discord.Webhook.from_url(url, session=self.session)


def reaction_builder_factory(dictionary: Dict) -> Reaction:
    reaction_type = ReactionType(dictionary.get("type"))
    reaction_dictionary = dictionary.copy()
    reaction_dictionary.pop("type")
    if reaction_type == ReactionType.DISCORD_HERALD:
        return DiscordMessageReaction(**reaction_dictionary)
