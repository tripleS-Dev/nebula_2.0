import os

bot_token = os.getenv('nebula_clean')

SEASONS = {
    'tripleS': ['Atom01', 'Binary01', 'Cream01', 'Divine01', 'Ever01', 'Atom02'],
    'ARTMS': ['Atom01', 'Binary01', 'Cream01'],
    'idntt': ['Spring25']
}
CLASSES = {
    'tripleS': ['First', 'Second', 'Special', 'Welcome', 'Zero'],
    'ARTMS': ['First', 'Second', 'Special', 'Welcome', 'Zero'],
    'idntt': ['Basic', 'Event', 'Special'],
}

ARTISTS = ['tripleS', 'ARTMS', 'idntt']

SORTS = ['Newest', 'Oldest']

member_color = {
    "seoyeon": (34, 174, 255),
    "hyerin": (146, 0, 255),
    "jiwoo": (255, 248, 0),
    "chaeyeon": (152, 242, 29),
    "yooyeon": (219, 12, 116),
    "soomin": (252, 131, 164),
    "nakyoung": (103, 153, 160),
    "yubin": (255, 227, 226),
    "kaede": (255, 201, 53),
    "dahyun": (255, 154, 214),
    "kotone": (255, 222, 0),
    "yeonji": (89, 116, 255),
    "nien": (255, 149, 63),
    "sohyun": (18, 34, 181),
    "xinyu": (213, 19, 19),
    "mayu": (254, 142, 118),
    "lynn": (172, 98, 183),
    "joobin": (183, 245, 76),
    "hayeon": (82, 217, 187),
    "shion": (255, 66, 138),
    "chaewon": (199, 163, 224),
    "sullin": (123, 186, 141),
    "seoah": (207, 243, 255),
    "jiyeon": (255, 171, 98),
    "heejin": (237, 0, 144),
    'haseul': (0, 166, 82),
    'kimlip': (239, 24, 65),
    'jinsoul': (25, 36, 167),
    'choerry': (90, 43, 146),
    'none': (0,0,0)
}
