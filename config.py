import os


# Your authorization token

bot_token = os.getenv('nebula_clean')
apollo_token = os.getenv('apollo_api')


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
    'none': (0,0,0),
    'idntt': (37, 52, 124)
}


objekt_contract = {
    'triples': "0xA4B37bE40F7b231Ee9574c4b16b7DDb7EAcDC99B",
    'artms': '0x0fB69F54bA90f17578a59823E09e5a1f8F3FA200',
    'idntt': '0x0000000000000000000000000000000000000000'
}


calender_colors = {                                  # 꼬모수: [배경색, 글자색]
    0: [(34,  38,  43),  (231, 221, 255)],  # '#22262B', '#E7DDFF'
    1: [(72,  70,  77),  (199, 191, 219)],  # '#48464D', '#C7BFDB'
    2: [(112, 108, 122), (219, 210, 241)],  # '#706C7A', '#DBD2F1'
    3: [(152, 146, 166), (23,  28,  32)],   # '#9892A6', '#171C20'
    4: [(192, 184, 211), (41,  44,  51)],   # '#C0B8D3', '#292C33'
    5: [(231, 221, 255), (64,  66,  77)],   # '#E7DDFF', '#40424D'
}
month_start = [4,7,7,3,5,1,3,6,2,4,7,2] #2025
month_end = [31,28,31,30,31,30,31,31,30,31,30,31]
