from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.core.responses import ApiResponse
from app.db.session import get_db
from app.schemas import (
    TemplateCategoryCreate,
    TemplateCategoryRead,
    TemplateCategoryUpdate,
    TemplateCloneRequest,
    TemplateCreate,
    TemplateRead,
    TemplateUpdate,
)
from app.services.template_service import TemplateService


router = APIRouter(
    prefix="/templates",
    tags=["templates"],
    dependencies=[Depends(get_current_active_user)],
)

category_router = APIRouter(
    prefix="/template-categories",
    tags=["template-categories"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("", response_model=ApiResponse[TemplateRead])
def create_template(
    payload: TemplateCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[TemplateRead]:
    template = TemplateService(db).create(payload)
    return ApiResponse(message="Template created.", data=template)


@router.get("", response_model=ApiResponse[list[TemplateRead]])
def search_templates(
    q: str | None = Query(default=None),
    industry: str | None = Query(default=None),
    category_id: UUID | None = Query(default=None),
    is_active: bool | None = Query(default=True),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> ApiResponse[list[TemplateRead]]:
    templates = TemplateService(db).search(
        q=q,
        industry=industry,
        category_id=category_id,
        is_active=is_active,
        offset=offset,
        limit=limit,
    )
    return ApiResponse(data=templates)


@router.get("/{id}", response_model=ApiResponse[TemplateRead])
def get_template(
    id: UUID,
    db: Session = Depends(get_db),
) -> ApiResponse[TemplateRead]:
    template = TemplateService(db).get(id)
    return ApiResponse(data=template)


@router.put("/{id}", response_model=ApiResponse[TemplateRead])
def update_template(
    id: UUID,
    payload: TemplateUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[TemplateRead]:
    template = TemplateService(db).update(id, payload)
    return ApiResponse(message="Template updated.", data=template)


@router.delete("/{id}", response_model=ApiResponse[dict])
def delete_template(
    id: UUID,
    db: Session = Depends(get_db),
) -> ApiResponse[dict]:
    TemplateService(db).delete(id)
    return ApiResponse(message="Template deleted.", data={"id": str(id)})


@router.post("/{id}/clone", response_model=ApiResponse[TemplateRead])
def clone_template(
    id: UUID,
    payload: TemplateCloneRequest,
    db: Session = Depends(get_db),
) -> ApiResponse[TemplateRead]:
    template = TemplateService(db).clone(id, payload)
    return ApiResponse(message="Template cloned.", data=template)


@category_router.post("", response_model=ApiResponse[TemplateCategoryRead])
def create_template_category(
    payload: TemplateCategoryCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[TemplateCategoryRead]:
    category = TemplateService(db).create_category(payload)
    return ApiResponse(message="Template category created.", data=category)


@category_router.get("", response_model=ApiResponse[list[TemplateCategoryRead]])
def list_template_categories(
    db: Session = Depends(get_db),
) -> ApiResponse[list[TemplateCategoryRead]]:
    categories = TemplateService(db).list_categories()
    return ApiResponse(data=categories)


@category_router.put("/{id}", response_model=ApiResponse[TemplateCategoryRead])
def update_template_category(
    id: UUID,
    payload: TemplateCategoryUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[TemplateCategoryRead]:
    category = TemplateService(db).update_category(id, payload)
    return ApiResponse(message="Template category updated.", data=category)


@category_router.delete("/{id}", response_model=ApiResponse[dict])
def delete_template_category(
    id: UUID,
    db: Session = Depends(get_db),
) -> ApiResponse[dict]:
    TemplateService(db).delete_category(id)
    return ApiResponse(message="Template category deleted.", data={"id": str(id)})

