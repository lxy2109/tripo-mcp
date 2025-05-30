import os
import httpx
from typing import Dict, Any
from dotenv import load_dotenv
from models import (
    TextToModelRequest, ImageToModelRequest, MultiviewToModelRequest, TextureModelRequest,
    RefineModelRequest, AnimatePrerigcheckRequest, AnimateRigRequest, AnimateRetargetRequest,
    StylizeModelRequest, ConvertModelRequest, TaskIdRequest, UploadImageRequest
)

load_dotenv()
TRIPO_API_KEY = os.getenv("TRIPO_API_KEY")
BASE_URL = "https://api.tripo3d.ai/v2/openapi"
HEADERS = {"Authorization": f"Bearer {TRIPO_API_KEY}"}

async def text_to_model(data: TextToModelRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "text_to_model"
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def image_to_model(data: ImageToModelRequest) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        with open(data.file_path, "rb") as f:
            files = {"file": (os.path.basename(data.file_path), f, f"image/{data.file_type}")}
            upload_resp = await client.post(f"{BASE_URL}/upload", headers=HEADERS, files=files)
        upload_data = upload_resp.json()
        file_token = upload_data.get("data", {}).get("image_token")
        payload = data.model_dump(exclude_none=True)
        payload["type"] = "image_to_model"
        payload["file"] = {"type": data.file_type, "file_token": file_token}
        del payload["file_path"]
        del payload["file_type"]
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def multiview_to_model(data: MultiviewToModelRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "multiview_to_model"
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def texture_model(data: TextureModelRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "texture_model"
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def refine_model(data: RefineModelRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "refine_model"
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def animate_prerigcheck(data: AnimatePrerigcheckRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "animate_prerigcheck"
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def animate_rig(data: AnimateRigRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "animate_rig"
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def animate_retarget(data: AnimateRetargetRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "animate_retarget"
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def stylize_model(data: StylizeModelRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "stylize_model"
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def convert_model(data: ConvertModelRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "convert_model"
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def get_task_status(data: TaskIdRequest) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/task/{data.task_id}", headers=HEADERS)
        return resp.json()

async def upload_image(data: UploadImageRequest) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        with open(data.file_path, "rb") as f:
            files = {"file": (os.path.basename(data.file_path), f, "image/jpeg")}
            resp = await client.post(f"{BASE_URL}/upload", headers=HEADERS, files=files)
        return resp.json()

async def get_balance() -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/user/balance", headers=HEADERS)
        return resp.json()

# 你可以继续扩展：上传、动画、后处理等API 