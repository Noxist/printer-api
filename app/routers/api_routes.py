from fastapi import APIRouter, Request, HTTPException, UploadFile, File
from fastapi.responses import PlainTextResponse
from PIL import Image
import io

from app.models.schemas import PrintPayload, RawPayload
from app.services.print_service import print_service
from app.services.mqtt_service import mqtt_service
from app.core.security import check_api_key
from app.utils.helpers import log, health_check
from app.config import PRINT_WIDTH_PX, TOPIC, PUBLISH_QOS

router = APIRouter()

@router.get("/_health", response_class=PlainTextResponse)
def health():
    return health_check()

@router.get("/")
def ok():
    return {"ok": True, "topic": TOPIC, "qos": PUBLISH_QOS}

@router.post("/print")
async def print_job(p: PrintPayload, request: Request):
    check_api_key(request)
    log("API /print", p.model_dump())
    img = print_service.render_text_ticket(p.title, p.lines, add_datetime=p.add_datetime)
    b64 = print_service.image_to_base64_png(img)
    mqtt_service.publish_image(b64, cut_paper=(1 if p.cut else 0))
    return {"ok": True}

@router.post("/webhook/print")
async def webhook(request: Request):
    check_api_key(request)
    data = await request.json() if "application/json" in (request.headers.get("content-type") or "") else {}
    text = data.get("text") or request.query_params.get("text")
    if not text:
        raise HTTPException(400, "text required")
    log("API /webhook/print", {"text": text})
    img = print_service.render_text_ticket("TASK", [text], add_datetime=True)
    b64 = print_service.image_to_base64_png(img)
    mqtt_service.publish_image(b64, cut_paper=1)
    return {"ok": True}

@router.post("/api/print/template")
async def api_print_template(p: PrintPayload, request: Request):
    check_api_key(request)
    log("API /api/print/template", p.model_dump())
    img = print_service.render_text_ticket(p.title, p.lines, add_datetime=p.add_datetime)
    b64 = print_service.image_to_base64_png(img)
    mqtt_service.publish_image(b64, cut_paper=(1 if p.cut else 0))
    return {"ok": True}

@router.post("/api/print/raw")
async def api_print_raw(p: RawPayload, request: Request):
    check_api_key(request)
    log("API /api/print/raw", p.model_dump())
    lines = (p.text + (f"\n{print_service._now_str()}" if p.add_datetime else "")).splitlines()
    img = print_service.render_text_ticket("", lines, add_datetime=False)
    b64 = print_service.image_to_base64_png(img)
    mqtt_service.publish_image(b64, cut_paper=1)
    return {"ok": True}

@router.post("/api/print/image")
async def api_print_image(request: Request, file: UploadFile = File(...)):
    check_api_key(request)
    content = await file.read()
    img = Image.open(io.BytesIO(content)).convert("L")
    w, h = img.size
    if w != PRINT_WIDTH_PX:
        img = img.resize((PRINT_WIDTH_PX, int(h * (PRINT_WIDTH_PX / w))))
    b64 = print_service.image_to_base64_png(img)
    log("API /api/print/image", {"orig_size": (w, h), "sent_width": PRINT_WIDTH_PX, "bytes": len(b64)})
    mqtt_service.publish_image(b64, cut_paper=1)
    return {"ok": True}

