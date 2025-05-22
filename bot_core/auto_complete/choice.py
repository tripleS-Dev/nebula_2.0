from utils import *
from itertools import chain

def choice_by_artist(interaction: discord.Interaction, current: str, OPTIONS: Dict[str, list]):
    if hasattr(interaction.namespace, "artist"):
        artist_choice = interaction.namespace.artist
    else:
        artist_choice = None

    if artist_choice is None:
        values_only = list(dict.fromkeys(chain.from_iterable(OPTIONS.values())))  # 아직 카테고리를 안 골랐으면 모두 반환
        return [app_commands.Choice(name=v, value=v) for v in values_only]


    candidates = OPTIONS.get(artist_choice, [])
    # 현재 입력과 부분 일치하는 것만 필터링
    return [
               app_commands.Choice(name=name, value=name)
               for name in candidates
               if current.lower() in name.lower()
           ][:25]  # 최대 25개