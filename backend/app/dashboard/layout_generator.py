"""Layout Generator for Dashboard Components."""

from app.dashboard.schemas import (
    ComponentConfig,
    ComponentRecommendation,
    ComponentType,
    DashboardComponent,
    LayoutPosition,
    TemplateDefinition,
)


class LayoutGenerator:
    """
    Generates dashboard layouts based on components and templates.

    Handles component placement, positioning, and grid management.
    """

    # Grid configuration
    GRID_WIDTH = 12
    GRID_HEIGHT = 20

    # Component sizing defaults
    COMPONENT_SIZES = {
        ComponentType.STAT_CARD: {"width": 3, "height": 3},
        ComponentType.GAUGE: {"width": 3, "height": 4},
        ComponentType.INDICATOR: {"width": 2, "height": 3},
        ComponentType.LINE_CHART: {"width": 6, "height": 4},
        ComponentType.BAR_CHART: {"width": 6, "height": 4},
        ComponentType.TREND: {"width": 4, "height": 3},
        ComponentType.ALARM_PANEL: {"width": 12, "height": 5},
        ComponentType.TABLE: {"width": 12, "height": 6},
        ComponentType.HEATMAP: {"width": 8, "height": 6},
    }

    def __init__(self, grid_width: int = GRID_WIDTH, grid_height: int = GRID_HEIGHT) -> None:
        """
        Initialize layout generator.

        Args:
            grid_width: Dashboard grid width.
            grid_height: Dashboard grid height.
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid: list[list[bool]] = [
            [False] * grid_width for _ in range(grid_height)
        ]

    def generate_layout(
        self,
        recommendations: list[ComponentRecommendation],
        template: TemplateDefinition | None = None,
    ) -> list[DashboardComponent]:
        """
        Generate dashboard layout from component recommendations.

        Args:
            recommendations: List of component recommendations.
            template: Optional template to apply styling.

        Returns:
            List of positioned components.
        """
        self._reset_grid()
        positioned_components = []

        # Sort recommendations by confidence for better placement
        sorted_recs = sorted(recommendations, key=lambda r: r.confidence, reverse=True)

        for recommendation in sorted_recs:
            component = self._recommendation_to_component(recommendation)
            position = self._find_position(component.component.type)

            if position:
                positioned = DashboardComponent(component=component, position=position)
                positioned_components.append(positioned)
                self._mark_grid(position)
            else:
                # If no position found, try to expand grid
                self._expand_grid()
                position = self._find_position(component.component.type)
                if position:
                    positioned = DashboardComponent(component=component, position=position)
                    positioned_components.append(positioned)
                    self._mark_grid(position)

        return positioned_components

    def _recommendation_to_component(
        self, recommendation: ComponentRecommendation
    ) -> ComponentConfig:
        """
        Convert a component recommendation to a component config.

        Args:
            recommendation: Component recommendation.

        Returns:
            Component configuration.
        """
        return ComponentConfig(
            type=recommendation.component_type,
            title=self._generate_title(recommendation),
            bindings=recommendation.source_bindings,
            properties=recommendation.suggested_properties,
        )

    def _generate_title(self, recommendation: ComponentRecommendation) -> str:
        """Generate a title for a component."""
        if recommendation.source_bindings:
            return recommendation.source_bindings[0].source_tag or "Component"
        return recommendation.component_type.value.replace("_", " ").title()

    def _find_position(
        self, component_type: ComponentType, max_attempts: int = 10
    ) -> LayoutPosition | None:
        """
        Find the best position for a component.

        Args:
            component_type: Type of component.
            max_attempts: Maximum placement attempts.

        Returns:
            Layout position or None if no position found.
        """
        size = self.COMPONENT_SIZES.get(
            component_type,
            {"width": 4, "height": 4},
        )
        width = min(size["width"], self.grid_width)
        height = min(size["height"], self.grid_height)

        # Try to find position: prefer top-left, then sweep left to right, top to bottom
        for row in range(self.grid_height - height + 1):
            for col in range(self.grid_width - width + 1):
                if self._can_place(row, col, height, width):
                    return LayoutPosition(row=row, col=col, width=width, height=height)

        return None

    def _can_place(self, row: int, col: int, height: int, width: int) -> bool:
        """
        Check if component can be placed at position.

        Args:
            row: Row position.
            col: Column position.
            height: Component height.
            width: Component width.

        Returns:
            True if position is available.
        """
        for r in range(row, min(row + height, self.grid_height)):
            for c in range(col, min(col + width, self.grid_width)):
                if self.grid[r][c]:
                    return False
        return True

    def _mark_grid(self, position: LayoutPosition) -> None:
        """
        Mark grid cells as occupied.

        Args:
            position: Component position.
        """
        for r in range(position.row, min(position.row + position.height, self.grid_height)):
            for c in range(position.col, min(position.col + position.width, self.grid_width)):
                self.grid[r][c] = True

    def _reset_grid(self) -> None:
        """Reset grid to empty."""
        self.grid = [
            [False] * self.grid_width for _ in range(self.grid_height)
        ]

    def _expand_grid(self, rows: int = 4) -> None:
        """
        Expand grid downward.

        Args:
            rows: Number of rows to add.
        """
        self.grid_height += rows
        for _ in range(rows):
            self.grid.append([False] * self.grid_width)

    def optimize_layout(self, components: list[DashboardComponent]) -> list[DashboardComponent]:
        """
        Optimize component layout to reduce wasted space.

        Args:
            components: List of positioned components.

        Returns:
            Optimized components.
        """
        if not components:
            return components

        # Sort by row, then by column
        sorted_components = sorted(
            components,
            key=lambda c: (c.position.row, c.position.col),
        )

        self._reset_grid()
        optimized = []

        for component in sorted_components:
            size = self.COMPONENT_SIZES.get(
                component.component.type,
                {"width": 4, "height": 4},
            )
            position = self._find_position(component.component.type)
            if position:
                optimized.append(
                    DashboardComponent(component=component.component, position=position)
                )
                self._mark_grid(position)

        return optimized

    def calculate_layout_metrics(self, components: list[DashboardComponent]) -> dict:
        """
        Calculate layout metrics.

        Args:
            components: List of components.

        Returns:
            Metrics dictionary.
        """
        if not components:
            return {
                "total_cells": 0,
                "used_cells": 0,
                "utilization": 0.0,
                "max_row": 0,
                "component_count": 0,
            }

        max_row = max(
            (c.position.row + c.position.height) for c in components
        )
        used_cells = sum(
            c.position.width * c.position.height
            for c in components
        )
        total_cells = self.grid_width * max(max_row, self.grid_height)
        utilization = (used_cells / total_cells * 100) if total_cells > 0 else 0

        return {
            "total_cells": total_cells,
            "used_cells": used_cells,
            "utilization": round(utilization, 2),
            "max_row": max_row,
            "component_count": len(components),
            "grid_efficiency": "good" if utilization > 60 else "fair" if utilization > 40 else "poor",
        }
