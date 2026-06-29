import re
from copy import deepcopy
from uuid import UUID

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models import Template, TemplateCategory
from app.repositories.template_repository import (
    TemplateCategoryRepository,
    TemplateRepository,
)
from app.schemas import (
    TemplateCategoryCreate,
    TemplateCategoryRead,
    TemplateCategoryUpdate,
    TemplateCloneRequest,
    TemplateCreate,
    TemplateRead,
    TemplateUpdate,
)


class TemplateService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.templates = TemplateRepository(db)
        self.categories = TemplateCategoryRepository(db)

    def create(self, payload: TemplateCreate) -> TemplateRead:
        self._ensure_category_exists(payload.category_id)
        self._ensure_slug_available(payload.slug)

        template = Template(
            category_id=payload.category_id,
            name=payload.name,
            slug=payload.slug,
            industry=payload.industry,
            description=payload.description,
            layout_json=payload.layout,
            components_json=payload.components,
            schema_json=self._build_schema(payload),
            preview_image_url=payload.preview_image_url,
            version=payload.version,
            is_active=payload.is_active,
            metadata_json=payload.metadata_json,
        )
        self.templates.add(template)
        self.db.commit()
        self.db.refresh(template)
        return self._to_read(self.templates.get(template.id) or template)

    def update(self, id: UUID, payload: TemplateUpdate) -> TemplateRead:
        template = self._get_template(id)

        if payload.category_id:
            self._ensure_category_exists(payload.category_id)
        if payload.slug and payload.slug != template.slug:
            self._ensure_slug_available(payload.slug)

        update_data = payload.model_dump(exclude_unset=True)
        schema_fields = {"name", "industry", "layout", "components"}
        schema_should_refresh = bool(schema_fields.intersection(update_data.keys()))
        if "layout" in update_data:
            template.layout_json = update_data.pop("layout")
        if "components" in update_data:
            template.components_json = update_data.pop("components")

        for field, value in update_data.items():
            setattr(template, field, value)

        if schema_should_refresh and payload.template_schema is None:
            template.schema_json = self._schema_from_template(template)

        self.db.commit()
        self.db.refresh(template)
        return self._to_read(self.templates.get(template.id) or template)

    def delete(self, id: UUID) -> None:
        template = self._get_template(id)
        self.templates.delete(template)
        self.db.commit()

    def clone(self, id: UUID, payload: TemplateCloneRequest) -> TemplateRead:
        source = self._get_template(id)
        clone_name = payload.name or f"{source.name} Copy"
        clone_slug = payload.slug or self._next_clone_slug(source.slug)
        self._ensure_slug_available(clone_slug)
        category_id = payload.category_id or source.category_id
        self._ensure_category_exists(category_id)

        cloned = Template(
            category_id=category_id,
            name=clone_name,
            slug=clone_slug,
            industry=source.industry,
            description=source.description,
            layout_json=deepcopy(source.layout_json),
            components_json=deepcopy(source.components_json),
            schema_json=deepcopy(source.schema_json),
            preview_image_url=source.preview_image_url,
            version=1,
            is_active=source.is_active,
            metadata_json=deepcopy(source.metadata_json),
        )
        self.templates.add(cloned)
        self.db.commit()
        self.db.refresh(cloned)
        return self._to_read(self.templates.get(cloned.id) or cloned)

    def get(self, id: UUID) -> TemplateRead:
        return self._to_read(self._get_template(id))

    def search(
        self,
        q: str | None = None,
        industry: str | None = None,
        category_id: UUID | None = None,
        is_active: bool | None = True,
        offset: int = 0,
        limit: int = 100,
    ) -> list[TemplateRead]:
        records = self.templates.search(
            q=q,
            industry=industry,
            category_id=category_id,
            is_active=is_active,
            offset=offset,
            limit=limit,
        )
        return [self._to_read(record) for record in records]

    def create_category(self, payload: TemplateCategoryCreate) -> TemplateCategoryRead:
        if self.categories.get_by_slug(payload.slug):
            raise AppException(
                message="Template category slug already exists.",
                status_code=status.HTTP_409_CONFLICT,
                error_code="template_category_slug_exists",
            )
        category = TemplateCategory(**payload.model_dump())
        self.categories.add(category)
        self.db.commit()
        self.db.refresh(category)
        return TemplateCategoryRead.model_validate(category)

    def update_category(
        self,
        id: UUID,
        payload: TemplateCategoryUpdate,
    ) -> TemplateCategoryRead:
        category = self._get_category(id)
        if payload.slug and payload.slug != category.slug:
            existing = self.categories.get_by_slug(payload.slug)
            if existing and existing.id != id:
                raise AppException(
                    message="Template category slug already exists.",
                    status_code=status.HTTP_409_CONFLICT,
                    error_code="template_category_slug_exists",
                )
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(category, field, value)
        self.db.commit()
        self.db.refresh(category)
        return TemplateCategoryRead.model_validate(category)

    def list_categories(self) -> list[TemplateCategoryRead]:
        return [
            TemplateCategoryRead.model_validate(category)
            for category in self.categories.list_categories()
        ]

    def delete_category(self, id: UUID) -> None:
        category = self._get_category(id)
        self.categories.delete(category)
        self.db.commit()

    def _get_template(self, id: UUID) -> Template:
        template = self.templates.get(id)
        if template is None:
            raise AppException(
                message="Template not found.",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code="template_not_found",
            )
        return template

    def _get_category(self, id: UUID) -> TemplateCategory:
        category = self.categories.get(id)
        if category is None:
            raise AppException(
                message="Template category not found.",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code="template_category_not_found",
            )
        return category

    def _ensure_category_exists(self, id: UUID) -> None:
        self._get_category(id)

    def _ensure_slug_available(self, slug: str) -> None:
        if self.templates.get_by_slug(slug):
            raise AppException(
                message="Template slug already exists.",
                status_code=status.HTTP_409_CONFLICT,
                error_code="template_slug_exists",
            )

    def _next_clone_slug(self, slug: str) -> str:
        base = re.sub(r"-copy(-\d+)?$", "", slug)
        candidate = f"{base}-copy"
        index = 2
        while self.templates.get_by_slug(candidate):
            candidate = f"{base}-copy-{index}"
            index += 1
        return candidate

    def _build_schema(self, payload: TemplateCreate) -> dict:
        if payload.template_schema:
            return payload.template_schema
        return {
            "name": payload.name,
            "industry": payload.industry,
            "layout": payload.layout,
            "components": payload.components,
        }

    def _schema_from_template(self, template: Template) -> dict:
        return {
            "name": template.name,
            "industry": template.industry,
            "layout": template.layout_json,
            "components": template.components_json,
        }

    def _to_read(self, template: Template) -> TemplateRead:
        return TemplateRead(
            id=template.id,
            category_id=template.category_id,
            name=template.name,
            slug=template.slug,
            industry=template.industry,
            description=template.description,
            layout=template.layout_json,
            components=template.components_json,
            template_schema=template.schema_json,
            preview_image_url=template.preview_image_url,
            version=template.version,
            is_active=template.is_active,
            metadata_json=template.metadata_json,
            created_at=template.created_at,
            updated_at=template.updated_at,
            category=(
                TemplateCategoryRead.model_validate(template.category)
                if template.category
                else None
            ),
        )
