from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.core.responses import ApiResponse
from app.db.session import get_db
from app.schemas import MetadataCreate, MetadataRead, MetadataUpdate
from app.services.metadata_service import MetadataService


router = APIRouter(
    prefix="/metadata",
    tags=["metadata"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("", response_model=ApiResponse[MetadataRead])
def create_metadata(
    payload: MetadataCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[MetadataRead]:
    metadata = MetadataService(db).create(payload)
    return ApiResponse(message="Metadata created.", data=metadata)


@router.get("", response_model=ApiResponse[list[MetadataRead]])
def list_metadata(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> ApiResponse[list[MetadataRead]]:
    metadata = MetadataService(db).list(offset=offset, limit=limit)
    return ApiResponse(data=metadata)


@router.get("/{id}", response_model=ApiResponse[MetadataRead])
def get_metadata(
    id: UUID,
    db: Session = Depends(get_db),
) -> ApiResponse[MetadataRead]:
    metadata = MetadataService(db).get(id)
    return ApiResponse(data=metadata)


@router.put("/{id}", response_model=ApiResponse[MetadataRead])
def update_metadata(
    id: UUID,
    payload: MetadataUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[MetadataRead]:
    metadata = MetadataService(db).update(id, payload)
    return ApiResponse(message="Metadata updated.", data=metadata)


@router.delete("/{id}", response_model=ApiResponse[dict])
def delete_metadata(
    id: UUID,
    db: Session = Depends(get_db),
) -> ApiResponse[dict]:
    MetadataService(db).delete(id)
    return ApiResponse(message="Metadata deleted.", data={"id": str(id)})
