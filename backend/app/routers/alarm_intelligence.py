from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.core.exceptions import AppException
from app.core.responses import ApiResponse
from app.db.session import get_db
from app.repositories.alarm_intelligence_repository import AlarmIntelligenceRepository
from app.schemas import (
    AlarmIntelligenceAnalysis,
    AlarmIntelligenceRequest,
    AlarmIntelligenceResultRead,
)
from app.services.alarm_intelligence_service import AlarmIntelligenceService


router = APIRouter(
    prefix="/alarm-intelligence",
    tags=["alarm-intelligence"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("/analyze", response_model=ApiResponse[AlarmIntelligenceAnalysis])
def analyze_alarm_stream(
    payload: AlarmIntelligenceRequest,
    db: Session = Depends(get_db),
) -> ApiResponse[AlarmIntelligenceAnalysis]:
    del db
    analysis = AlarmIntelligenceService().analyze(payload.events)
    return ApiResponse(message="Alarm stream analyzed successfully.", data=analysis)


@router.post("/process", response_model=ApiResponse[AlarmIntelligenceAnalysis])
def process_alarm_stream(
    payload: AlarmIntelligenceRequest,
    db: Session = Depends(get_db),
) -> ApiResponse[AlarmIntelligenceResultRead]:
    result = AlarmIntelligenceService(
        AlarmIntelligenceRepository(db)
    ).process(payload.events)
    return ApiResponse(
        message="Alarm stream processed successfully.",
        data=_to_result_read(result),
    )


@router.get("/results", response_model=ApiResponse[list[AlarmIntelligenceResultRead]])
def list_alarm_intelligence_results(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> ApiResponse[list[AlarmIntelligenceResultRead]]:
    results = AlarmIntelligenceService(
        AlarmIntelligenceRepository(db)
    ).list_results(limit=limit)
    return ApiResponse(data=[_to_result_read(result) for result in results])


@router.get("/results/{id}", response_model=ApiResponse[AlarmIntelligenceResultRead])
def get_alarm_intelligence_result(
    id: UUID,
    db: Session = Depends(get_db),
) -> ApiResponse[AlarmIntelligenceResultRead]:
    result = AlarmIntelligenceService(AlarmIntelligenceRepository(db)).get_result(id)
    if result is None:
        raise AppException(
            message="Alarm intelligence result not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="alarm_intelligence_result_not_found",
        )
    return ApiResponse(data=_to_result_read(result))


def _to_result_read(result) -> AlarmIntelligenceResultRead:
    return AlarmIntelligenceResultRead(
        id=result.id,
        root_cause=result.root_cause,
        confidence=result.confidence,
        affected_signals=result.affected_signals,
        severity_ranking=result.severity_ranking,
        suppressed_duplicates=result.suppressed_duplicates,
        grouped_incidents=result.grouped_incidents,
        incident_clusters=result.incident_clusters,
        input_event_count=result.input_event_count,
        created_at=result.created_at,
    )
