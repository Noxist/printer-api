import io
import base64
from datetime import datetime
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from app.config import PRINT_WIDTH_PX, FONT_TITLE, FONT_BODY, SIZE_TITLE, SIZE_BODY, MARGIN_X, MARGIN_Y, EXTRA_BOTTOM, TZ
from app.utils.helpers import log

class PrintService:
    def __init__(self):
        self.font_title = self._safe_load_font(FONT_TITLE, SIZE_TITLE)
        self.font_body = self._safe_load_font(FONT_BODY, SIZE_BODY)
        self.max_text_width = PRINT_WIDTH_PX - 2 * MARGIN_X

    def _safe_load_font(self, path: str, size: int) -> ImageFont.ImageFont:
        try:
            return ImageFont.truetype(path, size)
        except Exception as e:
            log(f"Font load failed for {path}: {e}. Using default.")
            return ImageFont.load_default()

    def _text_width(self, txt: str, font: ImageFont.ImageFont) -> int:
        try:
            return int(font.getlength(txt))
        except Exception:
            bbox = font.getbbox(txt)
            return bbox[2] - bbox[0]

    def _wrap_by_pixels(self, text: str, font: ImageFont.ImageFont, max_px: int) -> List[str]:
        words = text.split()
        if not words:
            return [""]
        lines = []
        line = words[0]
        for word in words[1:]:
            test = f"{line} {word}"
            if self._text_width(test, font) <= max_px:
                line = test
            else:
                lines.append(line)
                line = word
        lines.append(line)
        return lines

    def _now_str(self) -> str:
        return datetime.now(TZ).strftime("%d.%m.%Y %H:%M")

    def render_text_ticket(self, title: str, lines: List[str], add_datetime: bool = True) -> Image.Image:
        wrapped = []

        date_str = self._now_str() if add_datetime else None
        date_block_height = SIZE_BODY + 10 if date_str else 0

        if title and title.strip():
            for line in self._wrap_by_pixels(title.strip(), self.font_title, self.max_text_width):
                wrapped.append(("title", line))

        for ln in lines:
            txt = (ln or "").strip()
            if not txt:
                wrapped.append(("body", ""))
                continue
            for line in self._wrap_by_pixels(txt, self.font_body, self.max_text_width):
                wrapped.append(("body", line))

        line_h = SIZE_BODY + 10
        total_h = MARGIN_Y + date_block_height + (len(wrapped) * line_h) + EXTRA_BOTTOM
        total_h = max(total_h, 120)
        img = Image.new("L", (PRINT_WIDTH_PX, total_h), color=255)
        draw = ImageDraw.Draw(img)

        y = MARGIN_Y
        if date_str:
            w = self._text_width(date_str, self.font_body)
            draw.text((PRINT_WIDTH_PX - MARGIN_X - w, y), date_str, font=self.font_body, fill=0)
            y += date_block_height

        for kind, txt in wrapped:
            font = self.font_title if kind == "title" else self.font_body
            draw.text((MARGIN_X, y), txt, font=font, fill=0)
            y += line_h

        return img

    def image_to_base64_png(self, img: Image.Image) -> str:
        buf = io.BytesIO()
        img = img.convert("1")  # s/w, Dithering
        img.save(buf, format="PNG", optimize=True)
        return base64.b64encode(buf.getvalue()).decode("ascii")

print_service = PrintService()
