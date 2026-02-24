from fastapi import APIRouter, HTTPException, Depends, Body

from app.services.cr_extraction.service import run_service
from app.core.logger import set_log
from app.core.db import get_db
from sqlalchemy.orm import Session


router = APIRouter()

router_prefix = "/cr_extraction"


@router.post(f"{router_prefix}/extract", tags=["document"])
async def extract_document(
    payload: dict | str = Body(...),
    db: Session = Depends(get_db),
):
    set_log("cr_extraction")

    try:
        result = await run_service(payload, db)
        set_log("CR extraction done", level="info")
        return result
    except ValueError as exc:
        set_log(f"ValueError in extract_document: {exc}", level="error")
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        set_log(f"Exception in extract_document: {exc}", level="error")
        raise HTTPException(
            status_code=502, detail=f"VLLM request failed: {exc}"
        ) from exc
