from PIL import Image
import numpy as np


def color_change(image: Image, color: tuple[int,int,int]):
    """
    image      : RGBA Pillow 이미지 객체
    new_rgb  : (R, G, B) 0–255 정수 3-튜플
    반환값   : 알파는 유지하고 RGB만 new_rgb로 바꾼 새 RGBA 이미지
    """
    # Pillow → NumPy 배열 (복사본을 만들어 원본은 건드리지 않음)
    arr = np.asarray(image.convert("RGBA")).copy()

    # 앞의 3채널(R,G,B)을 새 색으로 통째로 덮어쓰기
    arr[..., :3] = (color[0] + 1, color[1] + 1, color[2] + 1)

    # NumPy 배열 → Pillow 이미지
    return Image.fromarray(arr, mode="RGBA")
