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
    # 互斥校验：file_path、file_token、url、object 只能有一个
    input_count = sum([bool(data.file_path), bool(data.file_token), bool(data.url), bool(data.object)])
    if input_count != 1:
        return {"code": 2003, "msg": "Exactly one of file_path, file_token, url, object must be provided."}
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "image_to_model"
    # 本地文件优先，且必须真实存在
    if data.file_path and os.path.isfile(data.file_path):
        async with httpx.AsyncClient() as client:
            with open(data.file_path, "rb") as f:
                files = {"file": (os.path.basename(data.file_path), f, f"image/{data.file_type or 'jpeg'}")}
                upload_resp = await client.post(f"{BASE_URL}/upload", headers=HEADERS, files=files)
            upload_data = upload_resp.json()
            file_token = upload_data.get("data", {}).get("image_token")
            payload["file"] = {"type": data.file_type or "jpeg", "file_token": file_token}
            payload.pop("file_path", None)
            payload.pop("file_type", None)
            payload.pop("url", None)
            payload.pop("object", None)
    elif data.file_token:
        payload["file"] = {"type": data.file_type or "jpeg", "file_token": data.file_token}
        payload.pop("file_path", None)
        payload.pop("file_type", None)
        payload.pop("url", None)
        payload.pop("object", None)
    elif data.url:
        payload["file"] = {"type": data.file_type or "jpeg", "url": data.url}
        payload.pop("file_path", None)
        payload.pop("file_type", None)
        payload.pop("file_token", None)
        payload.pop("object", None)
    elif data.object:
        payload["file"] = {"type": data.file_type or "jpeg", "object": data.object}
        payload.pop("file_path", None)
        payload.pop("file_type", None)
        payload.pop("file_token", None)
        payload.pop("url", None)
    async with httpx.AsyncClient() as client:
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
    if "out_format" in payload and payload["out_format"] not in ["glb", "fbx"]:
        return {"code": 2002, "msg": "The out_format is unsupported."}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def animate_retarget(data: AnimateRetargetRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "animate_retarget"
    if "out_format" in payload and payload["out_format"] not in ["glb", "fbx"]:
        return {"code": 2002, "msg": "The out_format is unsupported."}
    valid_animations = [
        "preset:idle", "preset:walk", "preset:climb", "preset:jump", "preset:run",
        "preset:slash", "preset:shoot", "preset:hurt", "preset:fall", "preset:turn"
    ]
    if payload.get("animation") not in valid_animations:
        return {"code": 2002, "msg": "The animation is unsupported."}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def stylize_model(data: StylizeModelRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "stylize_model"
    if payload.get("style") not in ["lego", "voxel", "voronoi", "minecraft"]:
        return {"code": 2002, "msg": "The style is unsupported."}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/task", headers=HEADERS, json=payload)
        return resp.json()

async def convert_model(data: ConvertModelRequest) -> Dict[str, Any]:
    payload = data.model_dump(exclude_none=True)
    payload["type"] = "convert_model"
    if payload.get("format") not in ["GLTF", "USDZ", "FBX", "OBJ", "STL", "3MF"]:
        return {"code": 2002, "msg": "The format is unsupported."}
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
        try:
            resp = await client.get(f"{BASE_URL}/user/balance", headers=HEADERS)
            result = resp.json()
            if resp.status_code == 200 and isinstance(result, dict):
                if "code" in result and "data" in result:
                    return result
                elif "balance" in result and "frozen" in result:
                    return {"code": 0, "data": {"balance": result["balance"], "frozen": result["frozen"]}}
                else:
                    return {"code": 0, "data": result}
            else:
                return {"code": 1001, "msg": "Fatal error on server side", "http_status": resp.status_code}
        except Exception as e:
            return {"code": 1001, "msg": f"Fatal error: {str(e)}"}
