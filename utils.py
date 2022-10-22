import discord
from dataclasses import dataclass
import math

@dataclass
class Location:
    x: int
    y: int
    z: int

    @staticmethod
    def from_string(string: str):
        x, y, z = string.split(" ")
        return Location(x=int(x), y=int(y), z=int(z))

    def compute_distance_l2(self, there: "Location"):
        math.sqrt((self.x - there.x)**2 + (self.y - there.y)**2 + (self.z - there.z)**2)


async def send_discord_message(webhook: discord.Webhook, message: str, username: str):
    await webhook.send(message, wait=True, username=username)