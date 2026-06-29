from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.models import AlarmIntelligenceResult
from app.repositories.alarm_intelligence_repository import AlarmIntelligenceRepository
from app.schemas import AlarmIntelligenceAnalysis, AlarmIntelligenceCluster, AlarmIntelligenceGroup, AlarmStreamEvent


SEVERITY_WEIGHTS = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
    "info": 0,
}

ROOT_CAUSE_RULES = [
    ("cooling", "Cooling Pump Failure"),
    ("pump", "Cooling Pump Failure"),
    ("fan", "Cooling Fan Degradation"),
    ("valve", "Valve Stiction"),
    ("sensor", "Sensor Drift"),
    ("power", "Power Supply Issue"),
    ("network", "Network Latency"),
    ("heat", "Heat Exchanger Fouling"),
    ("flow", "Flow Instability"),
    ("vibration", "Mechanical Vibration"),
    ("temperature", "Thermal Overload"),
]


class AlarmIntelligenceService:
    def __init__(self, repository: AlarmIntelligenceRepository | None = None) -> None:
        self.repository = repository

    def analyze(self, events: list[AlarmStreamEvent] | None = None) -> AlarmIntelligenceAnalysis:
        normalized_events = self._normalize_events(events or [])
        ranked_events = self._rank_severity(normalized_events)
        deduped_events, suppressed_count = self._suppress_duplicates(ranked_events)
        grouped_incidents = self._group_incidents(deduped_events)
        incident_clusters = self._cluster_incidents(deduped_events)
        root_cause, confidence = self._suggest_root_cause(deduped_events)
        affected_signals = [
            signal
            for signal in dict.fromkeys(
                event["signal_tag"] for event in deduped_events if event.get("signal_tag")
            )
        ]

        return AlarmIntelligenceAnalysis(
            root_cause=root_cause,
            confidence=confidence,
            affected_signals=affected_signals,
            severity_ranking=[
                {
                    "code": event["code"],
                    "severity": event["severity"],
                    "score": event["severity_weight"],
                    "source": event.get("source"),
                }
                for event in sorted(
                    deduped_events,
                    key=lambda item: (-item["severity_weight"], item["timestamp"]),
                )
            ],
            suppressed_duplicates=suppressed_count,
            grouped_incidents=[
                AlarmIntelligenceGroup(
                    key=group["key"],
                    alarm_count=group["alarm_count"],
                    max_severity=group["max_severity"],
                    affected_signals=group["affected_signals"],
                )
                for group in grouped_incidents
            ],
            incident_clusters=[
                AlarmIntelligenceCluster(
                    cluster_id=cluster["cluster_id"],
                    alarm_count=cluster["alarm_count"],
                    average_severity=cluster["average_severity"],
                    representative_signal=cluster["representative_signal"],
                )
                for cluster in incident_clusters
            ],
        )

    def process(self, events: list[AlarmStreamEvent]) -> AlarmIntelligenceResult:
        analysis = self.analyze(events)
        if self.repository is None:
            raise RuntimeError("Alarm intelligence repository is required to persist results.")

        result = AlarmIntelligenceResult(
            root_cause=analysis.root_cause,
            confidence=analysis.confidence,
            affected_signals=analysis.affected_signals,
            severity_ranking=analysis.severity_ranking,
            suppressed_duplicates=analysis.suppressed_duplicates,
            grouped_incidents=[
                group.model_dump() for group in analysis.grouped_incidents
            ],
            incident_clusters=[
                cluster.model_dump() for cluster in analysis.incident_clusters
            ],
            input_event_count=len(events),
        )
        self.repository.add(result)
        self.repository.db.commit()
        self.repository.db.refresh(result)
        return result

    def list_results(self, limit: int = 50) -> list[AlarmIntelligenceResult]:
        if self.repository is None:
            raise RuntimeError("Alarm intelligence repository is required to list results.")
        return self.repository.list_recent(limit=limit)

    def get_result(self, id) -> AlarmIntelligenceResult | None:
        if self.repository is None:
            raise RuntimeError("Alarm intelligence repository is required to read results.")
        return self.repository.get_result(id)

    def _normalize_events(self, events: list[AlarmStreamEvent | dict[str, Any]]) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []
        for event in events:
            if isinstance(event, AlarmStreamEvent):
                payload = event.model_dump()
            else:
                payload = dict(event)

            timestamp = payload.get("timestamp")
            if timestamp is None:
                timestamp_value = datetime.now(timezone.utc)
            elif isinstance(timestamp, datetime):
                timestamp_value = timestamp
            else:
                timestamp_value = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))

            severity = str(payload.get("severity") or "medium").lower()
            if severity not in SEVERITY_WEIGHTS:
                severity = "medium"

            normalized.append(
                {
                    "code": str(payload.get("code") or "alarm"),
                    "name": str(payload.get("name") or payload.get("code") or "Alarm"),
                    "severity": severity,
                    "source": str(payload.get("source") or payload.get("source_name") or "unknown"),
                    "signal_tag": str(payload.get("signal_tag") or payload.get("signal") or "").strip(),
                    "message": str(payload.get("message") or ""),
                    "timestamp": timestamp_value,
                    "metadata": payload.get("metadata_json") or payload.get("metadata") or {},
                }
            )

        return sorted(normalized, key=lambda item: item["timestamp"])

    def _rank_severity(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for event in events:
            event["severity_weight"] = SEVERITY_WEIGHTS[event["severity"]]
            event["severity_rank"] = self._severity_rank(event["severity_weight"])
        return events

    def _suppress_duplicates(self, events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
        kept: list[dict[str, Any]] = []
        suppressed = 0
        for event in events:
            signature = (event["code"], event["source"], event["signal_tag"])
            duplicate = False
            for existing in kept:
                same_signature = (existing["code"], existing["source"], existing["signal_tag"])
                if same_signature == signature and abs((event["timestamp"] - existing["timestamp"]).total_seconds()) <= 300:
                    duplicate = True
                    break
            if duplicate:
                suppressed += 1
            else:
                event["signature"] = signature
                kept.append(event)
        return kept, suppressed

    def _group_incidents(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        groups: dict[str, list[dict[str, Any]]] = {}
        for event in events:
            group_key = event["signal_tag"] or event["source"] or event["code"]
            groups.setdefault(group_key, []).append(event)

        grouped: list[dict[str, Any]] = []
        for key, members in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
            grouped.append(
                {
                    "key": key,
                    "alarm_count": len(members),
                    "max_severity": max((member["severity"] for member in members), key=lambda value: SEVERITY_WEIGHTS[value]),
                    "affected_signals": [
                        signal
                        for signal in dict.fromkeys(member["signal_tag"] for member in members if member.get("signal_tag"))
                    ],
                }
            )
        return grouped

    def _cluster_incidents(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if len(events) < 2:
            return [
                {
                    "cluster_id": 0,
                    "alarm_count": len(events),
                    "average_severity": max((event["severity"] for event in events), key=lambda value: SEVERITY_WEIGHTS[value], default="medium"),
                    "representative_signal": events[0]["signal_tag"] if events else None,
                }
            ]

        import pandas as pd
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler

        frame = pd.DataFrame(
            [
                {
                    "severity_weight": event["severity_weight"],
                    "text_length": len(event["message"] or ""),
                    "source_indicator": 1 if event.get("source") else 0,
                    "signal_indicator": 1 if event.get("signal_tag") else 0,
                }
                for event in events
            ]
        )
        scaled = StandardScaler().fit_transform(frame)
        labels = KMeans(n_clusters=min(3, len(events)), random_state=42, n_init=10).fit_predict(scaled)
        clusters: list[dict[str, Any]] = []
        for cluster_id in sorted(set(labels.tolist())):
            members = [event for event, label in zip(events, labels) if label == cluster_id]
            clusters.append(
                {
                    "cluster_id": int(cluster_id),
                    "alarm_count": len(members),
                    "average_severity": max((member["severity"] for member in members), key=lambda value: SEVERITY_WEIGHTS[value]),
                    "representative_signal": next((member["signal_tag"] for member in members if member.get("signal_tag")), None),
                }
            )
        return clusters

    def _suggest_root_cause(self, events: list[dict[str, Any]]) -> tuple[str, int]:
        if not events:
            return "No actionable alarm pattern detected", 55

        text = " ".join(
            f"{event['name']} {event['message']}" for event in events
        ).lower()
        scores: dict[str, int] = {}
        for keyword, cause in ROOT_CAUSE_RULES:
            if keyword in text:
                score = sum(SEVERITY_WEIGHTS[event["severity"]] for event in events if keyword in f"{event['name']} {event['message']}".lower())
                scores[cause] = score

        if not scores:
            return "General control loop anomaly", 62

        best_cause, best_score = max(scores.items(), key=lambda item: (item[1], item[0]))
        confidence = min(98, 60 + int(best_score * 7))
        return best_cause, confidence

    def _severity_rank(self, weight: int) -> int:
        if weight >= 4:
            return 1
        if weight == 3:
            return 2
        if weight == 2:
            return 3
        if weight == 1:
            return 4
        return 5
