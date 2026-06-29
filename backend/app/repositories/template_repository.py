from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.models import Template, TemplateCategory
from app.repositories.base import BaseRepository


class TemplateCategoryRepository(BaseRepository[TemplateCategory]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, TemplateCategory)

    def get_by_slug(self, slug: str) -> TemplateCategory | None:
        statement = select(TemplateCategory).where(TemplateCategory.slug == slug)
        return self.db.scalar(statement)

    def list_categories(self) -> list[TemplateCategory]:
        statement = select(TemplateCategory).order_by(
            TemplateCategory.sort_order,
            TemplateCategory.name,
        )
        return list(self.db.scalars(statement).all())


class TemplateRepository(BaseRepository[Template]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Template)

    def get(self, id: UUID) -> Template | None:
        statement = (
            select(Template)
            .options(selectinload(Template.category))
            .where(Template.id == id)
        )
        return self.db.scalar(statement)

    def get_by_slug(self, slug: str) -> Template | None:
        statement = (
            select(Template)
            .options(selectinload(Template.category))
            .where(Template.slug == slug)
        )
        return self.db.scalar(statement)

    def search(
        self,
        q: str | None = None,
        industry: str | None = None,
        category_id: UUID | None = None,
        is_active: bool | None = True,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Template]:
        statement = select(Template).options(selectinload(Template.category))

        if q:
            pattern = f"%{q}%"
            statement = statement.where(
                or_(
                    Template.name.ilike(pattern),
                    Template.slug.ilike(pattern),
                    Template.description.ilike(pattern),
                    Template.industry.ilike(pattern),
                )
            )
        if industry:
            statement = statement.where(Template.industry == industry)
        if category_id:
            statement = statement.where(Template.category_id == category_id)
        if is_active is not None:
            statement = statement.where(Template.is_active == is_active)

        statement = (
            statement.order_by(Template.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

