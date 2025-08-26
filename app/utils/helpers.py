import sys
import os

def log(*args):
    print("[printer]", *args, file=sys.stdout, flush=True)

def health_check() -> str:
    from app.config import FONT_TITLE, FONT_BODY, SIZE_TITLE, SIZE_BODY, TOPIC, PUBLISH_QOS, PRINT_WIDTH_PX, MARGIN_X, MARGIN_Y

    exists_title = os.path.exists(FONT_TITLE)
    exists_body = os.path.exists(FONT_BODY)

    return (
        f"OK\n"
        f"topic={TOPIC} qos={PUBLISH_QOS}\n"
        f"fonts: title=({FONT_TITLE}) exists={exists_title} size={SIZE_TITLE}; "
        f"body=({FONT_BODY}) exists={exists_body} size={SIZE_BODY}\n"
        f"width={PRINT_WIDTH_PX} margins=({MARGIN_X},{MARGIN_Y})... "
    )

