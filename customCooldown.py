
import discord
from discord.ext import commands

class CustomCooldown:
    def __init__(self, rate: int, per: float, alter_rate: int, alter_per: float, bucket: commands.BucketType, *, elements):
        self.elements = elements
        self.default_mapping = commands.CooldownMapping.from_cooldown(rate, per, bucket)
        self.altered_mapping = commands.CooldownMapping.from_cooldown(alter_rate, alter_per, bucket)

    def __call__(self, ctx: commands.Context):
        key = self.altered_mapping._bucket_key(ctx.message)
        if key in self.elements:
            bucket = self.altered_mapping.get_bucket(ctx.message)
        else:
            bucket = self.default_mapping.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(bucket, retry_after)
        return True