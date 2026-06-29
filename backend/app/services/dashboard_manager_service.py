import re
from uuid import UUID

from app.core.exceptions import AppException
from app.models import Dashboard, DashboardLayout, User
from app.repositories.dashboard_repository import DashboardRepository
from app.schemas import (
    DashboardEditorCreate,
    DashboardEditorRead,
    DashboardEditorUpdate,
    DashboardLayoutRead,
    DashboardRead,
)
from sqlalchemy.orm import Session
from fastapi import status


class DashboardManagerService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.dashboards = DashboardRepository(db)

    def list_dashboards(self, owner_id: UUID, offset: int = 0, limit: int = 100) -> tuple[list[Dashboard], int]:
        results = self.dashboards.list_by_owner(owner_id, offset, limit)
        total = self.dashboards.count_by_owner(owner_id)
        return results, total

    def create(self, payload: DashboardEditorCreate, owner: User) -> DashboardEditorRead:
        slug = self._ensure_unique_slug(self._slugify(payload.name))
        dashboard = Dashboard(
            owner_id=owner.id,
            industrial_system_id=payload.metadata_id,
            template_id=payload.template_id,
            name=payload.name,
            slug=slug,
            description=payload.description,
            status=payload.status,
            schema_version=payload.schema_version,
            is_public=payload.is_public,
            metadata_json=payload.metadata_json,
        )
        self.db.add(dashboard)
        self.db.flush()

        if payload.layout is not None:
            self._create_or_update_layout(dashboard, payload.layout)

        self.db.commit()
        self.db.refresh(dashboard)
        return self._to_editor_read(dashboard)

    def get(self, id: UUID) -> DashboardEditorRead:
        dashboard = self._get_dashboard(id)
        return self._to_editor_read(dashboard)

    def update(self, id: UUID, payload: DashboardEditorUpdate) -> DashboardEditorRead:
        dashboard = self._get_dashboard(id)
        update_data = payload.model_dump(exclude_unset=True)

        if 'name' in update_data:
            dashboard.name = update_data['name']
        if 'description' in update_data:
            dashboard.description = update_data['description']
        if 'metadata_id' in update_data:
            dashboard.industrial_system_id = update_data['metadata_id']
        if 'template_id' in update_data:
            dashboard.template_id = update_data['template_id']
        if 'status' in update_data:
            dashboard.status = update_data['status']
        if 'schema_version' in update_data:
            dashboard.schema_version = update_data['schema_version']
        if 'is_public' in update_data:
            dashboard.is_public = update_data['is_public']
        if 'metadata_json' in update_data:
            dashboard.metadata_json = update_data['metadata_json']
        if 'layout' in update_data:
            self._create_or_update_layout(dashboard, update_data['layout'])

        self.db.commit()
        self.db.refresh(dashboard)
        return self._to_editor_read(dashboard)

    def delete(self, id: UUID) -> None:
        dashboard = self._get_dashboard(id)
        self.db.delete(dashboard)
        self.db.commit()

    def _get_dashboard(self, id: UUID) -> Dashboard:
        dashboard = self.dashboards.get_with_layouts(id)
        if dashboard is None:
            raise AppException(
                message='Dashboard not found.',
                status_code=status.HTTP_404_NOT_FOUND,
                error_code='dashboard_not_found',
            )
        return dashboard

    def _create_or_update_layout(self, dashboard: Dashboard, layout_payload: dict) -> DashboardLayout:
        layout_data = layout_payload or {}
        breakpoint = layout_data.get('breakpoint', 'lg')
        columns = layout_data.get('columns', 12)
        row_height = layout_data.get('row_height', 30)
        layout_json = layout_data

        layout_record = next(iter(dashboard.layouts), None)
        if layout_record is None:
            layout_record = DashboardLayout(
                dashboard_id=dashboard.id,
                breakpoint=breakpoint,
                columns=columns,
                row_height=row_height,
                layout_json=layout_json,
            )
            self.db.add(layout_record)
        else:
            layout_record.breakpoint = breakpoint
            layout_record.columns = columns
            layout_record.row_height = row_height
            layout_record.layout_json = layout_json

        self.db.flush()
        return layout_record

    def _to_editor_read(self, dashboard: Dashboard) -> DashboardEditorRead:
        layout_record = next(iter(dashboard.layouts), None)
        return DashboardEditorRead(
            dashboard=DashboardRead.model_validate(dashboard),
            layout=(DashboardLayoutRead.model_validate(layout_record) if layout_record else None),
        )

    def _slugify(self, value: str) -> str:
        if not value:
            return 'dashboard'
        slug = re.sub(r'[^a-z0-9]+', '-', value.strip().lower())
        return slug.strip('-') or 'dashboard'

    def _ensure_unique_slug(self, slug: str) -> str:
        candidate = slug
        index = 1
        while self.dashboards.get_by_slug(candidate) is not None:
            index += 1
            candidate = f'{slug}-{index}'
        return candidate
