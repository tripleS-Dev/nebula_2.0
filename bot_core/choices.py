from utils import *


def strings_to_choices(strings: List[str]) -> List[app_commands.Choice[str]]:
    """
    문자열 리스트 → app_commands.Choice 리스트 변환

    Parameters
    ----------
    strings : List[str]
        예) ["newest", "oldest", "popular"]

    Returns
    -------
    List[app_commands.Choice[str]]
        예) [Choice(name='newest', value='newest'), ...]
    """
    return [app_commands.Choice(name=s, value=s) for s in strings]


# --- 사용 예시 -------------------------------------------------------------
if __name__ == "__main__":
    raw_options = ["newest", "oldest", "popular"]
    choice_objects = strings_to_choices(raw_options)
    for choice in choice_objects:
        print(f"name={choice.name}, value={choice.value}")
