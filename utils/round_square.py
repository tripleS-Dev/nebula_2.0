from PIL import Image
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent



def round_square(size,
                 radii=(0, 0, 0, 0),          # (tl, tr, br, bl)
                 color=(0, 0, 0, 0),
                 iOS=False):
    """
    4개의 모서리 각각에 다른 곡률을 줄 수 있는 사각형 PNG 생성.

    Parameters
    ----------
    size   : (w, h)
        최종 이미지 크기(픽셀)
    radii  : int | tuple(int, int, int, int)
        각 모서리 반지름. 단일 int를 주면 4곳 모두 동일 반지름.
        순서는 (좌상, 우상, 우하, 좌하) = (tl, tr, br, bl)
    color  : (R, G, B, A)
        사각형 내부 색상
    """
    if iOS:
        ad = '_ios'
    else:
        ad = ''
    # 입력 정규화 -------------------------------------------------------------
    if isinstance(radii, int):
        radii = (radii, radii, radii, radii)
    if len(radii) != 4:
        raise ValueError("radii는 int 하나 또는 길이 4 튜플이어야 합니다.")

    w, h   = size
    blank  = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    square = Image.new("RGBA", (w, h), color)

    # 모든 모서리가 0이면 바로 반환 ------------------------------------------
    if all(r == 0 for r in radii):
        return square

    # ① 전체 알파 마스크 초기화 (0 = 투명) -----------------------------------
    alpha_mask = np.zeros((h, w), dtype=np.uint8)

    # ② 각 모서리별 마스크 합성 ---------------------------------------------
    positions = ("tl", "tr", "br", "bl")
    for r, pos in zip(radii, positions):
        if r == 0:
            continue

        # 코너 알파 PNG는 좌상단용(quadrant)이라고 가정
        corner = Image.open(f"{BASE_DIR}/rounds/{r}{ad}.png")
        corner_alpha = np.array(corner)[..., 3]

        # 방향 맞추기
        if pos == "tr":
            corner_alpha = np.fliplr(corner_alpha)
        elif pos == "br":
            corner_alpha = np.flipud(np.fliplr(corner_alpha))
        elif pos == "bl":
            corner_alpha = np.flipud(corner_alpha)

        ch, cw = corner_alpha.shape      # 코너 PNG 크기

        # 대상 위치 계산
        y0 = 0 if pos in ("tl", "tr") else h - ch
        x0 = 0 if pos in ("tl", "bl") else w - cw

        # 알파 마스크 최대치로 누적(겹치는 부분 대비)
        alpha_mask[y0:y0+ch, x0:x0+cw] = np.maximum(
            alpha_mask[y0:y0+ch, x0:x0+cw],
            corner_alpha
        )

    # ③ 사각형 배열로 변환 후 알파 “깎기” -------------------------------------
    arr        = np.array(square)
    alpha_orig = arr[..., 3].astype(np.int16)
    alpha_new  = np.clip(alpha_orig - alpha_mask.astype(np.int16), 0, 255)
    arr[..., 3] = alpha_new.astype(np.uint8)

    # ④ 결과 반환 -------------------------------------------------------------
    out = Image.fromarray(arr)
    #out.show()   # 필요 없으면 삭제 가능
    return out


if __name__ == '__main__':
    # 네 모서리 반지름 서로 다르게 지정
    img = round_square(
        size=(600, 200),
        radii=(0, 16, 16, 0),      # (tl, tr, br, bl)
        color=(255, 255, 255, 255),
        iOS=True
    )
    img.show()