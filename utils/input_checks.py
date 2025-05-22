from utils import app_commands, Dict, List

def input_check(artist: app_commands.Choice[str], a: Dict[str, List[str]], b: str) -> bool:

    if not artist:
        return True

    artist = artist.value

    if not b:
        return True

    elif b in a.get(artist):
        return True
    else:
        return False