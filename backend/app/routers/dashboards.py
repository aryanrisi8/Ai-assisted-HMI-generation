from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.core.responses import ApiResponse
from app.db.session import get_db
from app.schemas import (
    DashboardEditorCreate,
    DashboardEditorRead,
    DashboardEditorUpdate,
    DashboardRead,
    TemplateRead,
)
from app.services.dashboard_manager_service import DashboardManagerService
from app.services.dashboard_service import DashboardGenerationService
from app.services.template_service import TemplateService


router = APIRouter(
    prefix='/dashboards',
    tags=['dashboards'],
    dependencies=[Depends(get_current_active_user)],
)


@router.post('', response_model=ApiResponse[DashboardEditorRead])
def create_dashboard(
    payload: DashboardEditorCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> ApiResponse[DashboardEditorRead]:
    dashboard = DashboardManagerService(db).create(payload, current_user)
    return ApiResponse(message='Dashboard created.', data=dashboard)


@router.get('', response_model=ApiResponse[dict])
def list_dashboards(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
) -> ApiResponse[dict]:
    results, total = DashboardManagerService(db).list_dashboards(
        current_user.id, offset=offset, limit=limit
    )
    return ApiResponse(data={
        'results': [DashboardRead.model_validate(dashboard) for dashboard in results],
        'meta': {
            'offset': offset,
            'limit': limit,
            'total': total,
        },
    })


@router.get('/templates', response_model=ApiResponse[list[TemplateRead]])
def get_dashboard_templates(
    db: Session = Depends(get_db),
) -> ApiResponse[list[TemplateRead]]:
    templates = TemplateService(db).search()
    return ApiResponse(data=templates)


@router.post('/generate/{metadata_id}', response_model=ApiResponse[dict])
def generate_dashboard(
    metadata_id: UUID,
    db: Session = Depends(get_db),
) -> ApiResponse[dict]:
    from app.repositories.metadata_repository import MetadataRepository
    from app.dashboard.schemas import IndustrialSystemMetadata

    metadata = MetadataRepository(db).get_metadata(metadata_id)
    if metadata is None:
        return ApiResponse(
            success=False,
            message='Metadata not found.',
            data={},
        )

    system_metadata = IndustrialSystemMetadata(
        id=metadata.id,
        name=metadata.name,
        code=metadata.code,
        description=metadata.description,
        system_type=metadata.system_type,
        location=metadata.location,
        sensors=[
            {
                'id': str(sensor.id),
                'code': sensor.code,
                'name': sensor.name,
                'sensor_type': sensor.sensor_type,
                'description': sensor.description,
                'signals': [
                    {
                        'id': str(signal.id),
                        'tag': signal.tag,
                        'name': signal.name,
                        'data_type': signal.data_type,
                        'direction': signal.direction,
                        'unit': signal.engineering_unit,
                        'min_value': signal.min_value,
                        'max_value': signal.max_value,
                        'description': signal.description,
                    }
                    for signal in sensor.signals
                ],
            }
            for sensor in metadata.sensors
        ],
        alarms=[
            {
                'id': str(alarm.id),
                'code': alarm.code,
                'name': alarm.name,
                'severity': alarm.severity,
                'state': alarm.state,
                'signal_id': str(alarm.signal_id) if alarm.signal_id else None,
            }
            for signal in metadata.signals
            for alarm in signal.alarms
        ],
    )

    generated = DashboardGenerationService().generate(system_metadata)
    return ApiResponse(data=generated)


@router.get('/recommendations/{metadata_id}', response_model=ApiResponse[dict])
def get_dashboard_recommendations(
    metadata_id: UUID,
    db: Session = Depends(get_db),
) -> ApiResponse[dict]:
    from app.repositories.metadata_repository import MetadataRepository
    from app.dashboard.schemas import IndustrialSystemMetadata

    metadata = MetadataRepository(db).get_metadata(metadata_id)
    if metadata is None:
        return ApiResponse(
            success=False,
            message='Metadata not found.',
            data={},
        )

    system_metadata = IndustrialSystemMetadata(
        id=metadata.id,
        name=metadata.name,
        code=metadata.code,
        description=metadata.description,
        system_type=metadata.system_type,
        location=metadata.location,
        sensors=[
            {
                'id': str(sensor.id),
                'code': sensor.code,
                'name': sensor.name,
                'sensor_type': sensor.sensor_type,
                'description': sensor.description,
                'signals': [
                    {
                        'id': str(signal.id),
                        'tag': signal.tag,
                        'name': signal.name,
                        'data_type': signal.data_type,
                        'direction': signal.direction,
                        'unit': signal.engineering_unit,
                        'min_value': signal.min_value,
                        'max_value': signal.max_value,
                        'description': signal.description,
                    }
                    for signal in sensor.signals
                ],
            }
            for sensor in metadata.sensors
        ],
        alarms=[
            {
                'id': str(alarm.id),
                'code': alarm.code,
                'name': alarm.name,
                'severity': alarm.severity,
                'state': alarm.state,
                'signal_id': str(alarm.signal_id) if alarm.signal_id else None,
            }
            for signal in metadata.signals
            for alarm in signal.alarms
        ],
    )

    recommendations = DashboardGenerationService().get_raw_recommendations(system_metadata)
    return ApiResponse(data=recommendations.model_dump())


@router.get('/{id}', response_model=ApiResponse[DashboardEditorRead])
def get_dashboard(
    id: UUID,
    db: Session = Depends(get_db),
) -> ApiResponse[DashboardEditorRead]:
    dashboard = DashboardManagerService(db).get(id)
    return ApiResponse(data=dashboard)


@router.put('/{id}', response_model=ApiResponse[DashboardEditorRead])
def update_dashboard(
    id: UUID,
    payload: DashboardEditorUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[DashboardEditorRead]:
    dashboard = DashboardManagerService(db).update(id, payload)
    return ApiResponse(message='Dashboard updated.', data=dashboard)


@router.delete('/{id}', response_model=ApiResponse[dict])
def delete_dashboard(
    id: UUID,
    db: Session = Depends(get_db),
) -> ApiResponse[dict]:
    DashboardManagerService(db).delete(id)
    return ApiResponse(message='Dashboard deleted.', data={'id': str(id)})


