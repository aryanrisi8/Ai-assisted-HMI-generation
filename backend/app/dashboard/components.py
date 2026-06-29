"""Component Definitions and Recommendation Engine."""

from app.dashboard.schemas import (
    ComponentBinding,
    ComponentRecommendation,
    ComponentType,
    DataSourceType,
    IndustrialSystemMetadata,
    RecommendationResult,
)


class ComponentCatalog:
    """Catalog of available components with their characteristics."""

    # Component profiles: what data types they work best with
    COMPONENT_PROFILES = {
        ComponentType.GAUGE: {
            "best_for": ["numeric", "float", "int"],
            "max_signals": 1,
            "description": "Analog gauge display",
            "priority": 7,
        },
        ComponentType.STAT_CARD: {
            "best_for": ["numeric", "float", "int", "boolean"],
            "max_signals": 1,
            "description": "Single statistic card",
            "priority": 8,
        },
        ComponentType.LINE_CHART: {
            "best_for": ["numeric", "float", "int"],
            "max_signals": 5,
            "description": "Time series line chart",
            "priority": 6,
        },
        ComponentType.BAR_CHART: {
            "best_for": ["numeric", "float", "int"],
            "max_signals": 8,
            "description": "Bar chart for comparison",
            "priority": 5,
        },
        ComponentType.TABLE: {
            "best_for": ["mixed"],
            "max_signals": 10,
            "description": "Data table",
            "priority": 3,
        },
        ComponentType.ALARM_PANEL: {
            "best_for": ["alarm", "boolean"],
            "max_signals": 20,
            "description": "Alarm status panel",
            "priority": 9,
        },
        ComponentType.INDICATOR: {
            "best_for": ["boolean", "status"],
            "max_signals": 1,
            "description": "Binary indicator",
            "priority": 8,
        },
        ComponentType.TREND: {
            "best_for": ["numeric", "float", "int"],
            "max_signals": 3,
            "description": "Trend indicator",
            "priority": 7,
        },
        ComponentType.HEATMAP: {
            "best_for": ["numeric", "matrix"],
            "max_signals": 50,
            "description": "2D heatmap visualization",
            "priority": 4,
        },
    }


class ComponentRecommendationEngine:
    """
    Recommends dashboard components based on industrial metadata.

    Analyzes signals, sensors, and system characteristics to suggest
    appropriate components and their configuration.
    """

    def __init__(self) -> None:
        """Initialize the recommendation engine."""
        self.catalog = ComponentCatalog()

    def recommend(self, metadata: IndustrialSystemMetadata) -> RecommendationResult:
        """
        Generate component recommendations for industrial metadata.

        Args:
            metadata: Industrial system metadata.

        Returns:
            Recommendation result with components and layout reasoning.
        """
        recommendations = []
        reasoning_points = []

        # Analyze signals
        all_signals = self._collect_all_signals(metadata)
        signal_types = self._categorize_signals(all_signals)

        # 1. Recommend stat cards for critical metrics
        stat_cards = self._recommend_stat_cards(all_signals, signal_types)
        recommendations.extend(stat_cards)
        if stat_cards:
            reasoning_points.append(
                f"Added {len(stat_cards)} stat cards for key metrics visibility"
            )

        # 2. Recommend gauges for analog values
        gauges = self._recommend_gauges(all_signals, signal_types)
        recommendations.extend(gauges)
        if gauges:
            reasoning_points.append(f"Added {len(gauges)} gauges for analog monitoring")

        # 3. Recommend charts for trending data
        charts = self._recommend_trends(all_signals, signal_types)
        recommendations.extend(charts)
        if charts:
            reasoning_points.append(f"Added trending visualizations for time-series data")

        # 4. Recommend alarm panel if alarms exist
        if metadata.alarms:
            alarm_rec = self._recommend_alarm_panel(metadata.alarms)
            if alarm_rec:
                recommendations.append(alarm_rec)
                reasoning_points.append(
                    f"Added alarm panel for {len(metadata.alarms)} alarm sources"
                )

        # 5. Recommend table for multiple signals
        if len(all_signals) > 5:
            table_rec = self._recommend_table(all_signals, len(all_signals))
            if table_rec:
                recommendations.append(table_rec)
                reasoning_points.append("Added data table for comprehensive signal monitoring")

        # 6. Recommend indicators for boolean signals
        indicators = self._recommend_indicators(signal_types.get("boolean", []))
        recommendations.extend(indicators)
        if indicators:
            reasoning_points.append(f"Added {len(indicators)} status indicators")

        # Calculate estimated layout size
        grid_width = 12
        grid_height = max(4, (len(recommendations) // 3 + 1) * 4)

        layout_reasoning = "; ".join(reasoning_points) or "Generated minimal dashboard layout"

        return RecommendationResult(
            recommendations=self._sort_by_confidence(recommendations),
            layout_reasoning=layout_reasoning,
            estimated_grid_size={"width": grid_width, "height": grid_height},
        )

    def _collect_all_signals(self, metadata: IndustrialSystemMetadata) -> list[dict]:
        """Collect all signals from all sensors."""
        signals = []
        for sensor in metadata.sensors:
            for signal in sensor.signals:
                signals.append(
                    {
                        "signal": signal,
                        "sensor": sensor,
                    }
                )
        return signals

    def _categorize_signals(self, signals: list[dict]) -> dict[str, list[dict]]:
        """Categorize signals by type."""
        categorized = {
            "numeric": [],
            "boolean": [],
            "status": [],
            "other": [],
        }

        for item in signals:
            signal = item["signal"]
            data_type = signal.data_type.lower()

            if data_type in ["int", "float", "numeric", "double"]:
                categorized["numeric"].append(item)
            elif data_type in ["boolean", "bool", "bit"]:
                categorized["boolean"].append(item)
            elif data_type in ["status", "enum", "string"]:
                categorized["status"].append(item)
            else:
                categorized["other"].append(item)

        return categorized

    def _recommend_stat_cards(
        self, all_signals: list[dict], categorized: dict
    ) -> list[ComponentRecommendation]:
        """Recommend stat cards for key metrics."""
        recommendations = []

        # Prioritize numeric signals with units and ranges
        numeric_signals = categorized.get("numeric", [])[:3]  # Top 3

        for item in numeric_signals:
            signal = item["signal"]
            sensor = item["sensor"]

            recommendation = ComponentRecommendation(
                component_type=ComponentType.STAT_CARD,
                reasoning=f"Key metric: {signal.name} from {sensor.name}",
                confidence=0.9,
                source_bindings=[
                    ComponentBinding(
                        source_type=DataSourceType.SIGNAL,
                        source_id=signal.id,
                        source_tag=signal.tag,
                        property_name="value",
                    )
                ],
                suggested_properties={
                    "unit": signal.unit or "",
                    "precision": 2,
                    "show_trend": True,
                },
            )
            recommendations.append(recommendation)

        return recommendations

    def _recommend_gauges(
        self, all_signals: list[dict], categorized: dict
    ) -> list[ComponentRecommendation]:
        """Recommend gauges for analog values with ranges."""
        recommendations = []

        numeric_signals = categorized.get("numeric", [])

        for item in numeric_signals[3:6]:  # Next 3 signals after stat cards
            signal = item["signal"]
            sensor = item["sensor"]

            if signal.min_value is not None and signal.max_value is not None:
                recommendation = ComponentRecommendation(
                    component_type=ComponentType.GAUGE,
                    reasoning=(
                        f"Analog gauge for {signal.name} with range "
                        f"{signal.min_value}-{signal.max_value}"
                    ),
                    confidence=0.85,
                    source_bindings=[
                        ComponentBinding(
                            source_type=DataSourceType.SIGNAL,
                            source_id=signal.id,
                            source_tag=signal.tag,
                            property_name="value",
                        )
                    ],
                    suggested_properties={
                        "min": signal.min_value,
                        "max": signal.max_value,
                        "unit": signal.unit or "",
                    },
                )
                recommendations.append(recommendation)

        return recommendations

    def _recommend_trends(
        self, all_signals: list[dict], categorized: dict
    ) -> list[ComponentRecommendation]:
        """Recommend trend and chart components."""
        recommendations = []

        numeric_signals = categorized.get("numeric", [])

        if len(numeric_signals) > 1:
            # Line chart for multiple signals
            top_signals = numeric_signals[:5]
            bindings = [
                ComponentBinding(
                    source_type=DataSourceType.SIGNAL,
                    source_id=item["signal"].id,
                    source_tag=item["signal"].tag,
                    property_name="value",
                )
                for item in top_signals
            ]

            recommendation = ComponentRecommendation(
                component_type=ComponentType.LINE_CHART,
                reasoning=f"Time-series trend visualization for {len(top_signals)} metrics",
                confidence=0.85,
                source_bindings=bindings,
                suggested_properties={
                    "time_window": "1h",
                    "aggregate": "average",
                    "show_legend": True,
                },
            )
            recommendations.append(recommendation)

        return recommendations

    def _recommend_alarm_panel(self, alarms: list[dict]) -> ComponentRecommendation | None:
        """Recommend alarm panel."""
        if not alarms:
            return None

        bindings = [
            ComponentBinding(
                source_type=DataSourceType.ALARM,
                source_id=str(i),
                property_name="status",
            )
            for i in range(min(len(alarms), 10))
        ]

        return ComponentRecommendation(
            component_type=ComponentType.ALARM_PANEL,
            reasoning=f"Centralized alarm monitoring for {len(alarms)} alarm sources",
            confidence=0.95,
            source_bindings=bindings,
            suggested_properties={
                "show_severity": True,
                "show_timestamp": True,
                "auto_refresh": True,
            },
        )

    def _recommend_table(
        self, all_signals: list[dict], signal_count: int
    ) -> ComponentRecommendation | None:
        """Recommend data table for many signals."""
        bindings = [
            ComponentBinding(
                source_type=DataSourceType.SIGNAL,
                source_id=item["signal"].id,
                source_tag=item["signal"].tag,
                property_name="value",
            )
            for item in all_signals[:10]
        ]

        return ComponentRecommendation(
            component_type=ComponentType.TABLE,
            reasoning=f"Data table for comprehensive monitoring of {len(all_signals)} signals",
            confidence=0.75,
            source_bindings=bindings,
            suggested_properties={
                "sortable": True,
                "filterable": True,
                "show_units": True,
            },
        )

    def _recommend_indicators(self, boolean_signals: list[dict]) -> list[ComponentRecommendation]:
        """Recommend indicators for boolean signals."""
        recommendations = []

        for item in boolean_signals[:5]:  # Top 5
            signal = item["signal"]
            sensor = item["sensor"]

            recommendation = ComponentRecommendation(
                component_type=ComponentType.INDICATOR,
                reasoning=f"Status indicator for {signal.name}",
                confidence=0.8,
                source_bindings=[
                    ComponentBinding(
                        source_type=DataSourceType.SIGNAL,
                        source_id=signal.id,
                        source_tag=signal.tag,
                        property_name="value",
                    )
                ],
                suggested_properties={
                    "active_label": "Active",
                    "inactive_label": "Inactive",
                    "blink_on_change": True,
                },
            )
            recommendations.append(recommendation)

        return recommendations

    @staticmethod
    def _sort_by_confidence(recommendations: list[ComponentRecommendation]) -> list[ComponentRecommendation]:
        """Sort recommendations by confidence descending."""
        return sorted(recommendations, key=lambda r: r.confidence, reverse=True)
