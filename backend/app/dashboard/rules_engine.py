"""Rules Engine for Dashboard Generation."""

from typing import Any

from app.dashboard.schemas import Rule, RuleContext, RuleResult


class RulesEngine:
    """
    Evaluates rules based on industrial metadata context.

    Supports rule matching, evaluation, and priority-based execution.
    """

    def __init__(self) -> None:
        """Initialize the rules engine."""
        self.rules: dict[str, Rule] = {}
        self._loaded_rules: list[Rule] = []

    def add_rule(self, rule: Rule) -> None:
        """
        Add a rule to the engine.

        Args:
            rule: Rule to add.
        """
        if rule.enabled:
            self.rules[rule.id] = rule

    def add_rules(self, rules: list[Rule]) -> None:
        """
        Add multiple rules.

        Args:
            rules: List of rules to add.
        """
        for rule in rules:
            self.add_rule(rule)
        self._loaded_rules = rules

    def evaluate(self, context: RuleContext) -> list[RuleResult]:
        """
        Evaluate all matching rules against the context.

        Args:
            context: Rule context.

        Returns:
            List of evaluation results.
        """
        results = []

        # Sort by priority (descending)
        sorted_rules = sorted(self.rules.values(), key=lambda r: r.priority, reverse=True)

        for rule in sorted_rules:
            matched = self._evaluate_conditions(rule.conditions, context)
            result = RuleResult(
                rule_id=rule.id,
                matched=matched,
                actions=rule.actions if matched else {},
            )
            results.append(result)

        return results

    def evaluate_single(self, rule_id: str, context: RuleContext) -> RuleResult | None:
        """
        Evaluate a single rule.

        Args:
            rule_id: ID of rule to evaluate.
            context: Rule context.

        Returns:
            Evaluation result or None if rule not found.
        """
        rule = self.rules.get(rule_id)
        if not rule:
            return None

        matched = self._evaluate_conditions(rule.conditions, context)
        return RuleResult(
            rule_id=rule.id,
            matched=matched,
            actions=rule.actions if matched else {},
        )

    def _evaluate_conditions(self, conditions: dict[str, Any], context: RuleContext) -> bool:
        """
        Evaluate conditions against context.

        Supports conditions:
        - signal_count: exact value or range {"min": 5, "max": 50}
        - sensor_count: exact value or range
        - has_alarms: boolean
        - system_type: string or list of strings
        - signal_types: list of signal types (all must be present)
        - custom: dict with custom field checks

        Args:
            conditions: Condition dictionary.
            context: Rule context.

        Returns:
            True if all conditions match, False otherwise.
        """
        for condition_key, condition_value in conditions.items():
            if not self._check_condition(condition_key, condition_value, context):
                return False

        return True

    def _check_condition(
        self, condition_key: str, condition_value: Any, context: RuleContext
    ) -> bool:
        """
        Check a single condition.

        Args:
            condition_key: Condition key.
            condition_value: Condition value.
            context: Rule context.

        Returns:
            True if condition matches.
        """
        if condition_key == "signal_count":
            return self._check_numeric_range(context.signal_count, condition_value)

        elif condition_key == "sensor_count":
            return self._check_numeric_range(context.sensor_count, condition_value)

        elif condition_key == "has_alarms":
            return context.has_alarms == condition_value

        elif condition_key == "system_type":
            if isinstance(condition_value, list):
                return context.system_type in condition_value
            return context.system_type == condition_value

        elif condition_key == "signal_types":
            if isinstance(condition_value, list):
                return all(st in context.signal_types for st in condition_value)
            return condition_value in context.signal_types

        return True

    @staticmethod
    def _check_numeric_range(value: int | float, condition: Any) -> bool:
        """
        Check numeric range condition.

        Supports:
        - int: exact match
        - dict with "min" and/or "max" keys

        Args:
            value: Value to check.
            condition: Condition value or range dict.

        Returns:
            True if in range.
        """
        if isinstance(condition, dict):
            if "min" in condition and value < condition["min"]:
                return False
            if "max" in condition and value > condition["max"]:
                return False
            return True

        return value == condition

    def get_matched_rules(self, context: RuleContext) -> list[Rule]:
        """
        Get all rules that match the context.

        Args:
            context: Rule context.

        Returns:
            List of matched rules sorted by priority.
        """
        results = self.evaluate(context)
        matched_ids = [r.rule_id for r in results if r.matched]
        matched_rules = [self.rules[rid] for rid in matched_ids if rid in self.rules]
        return sorted(matched_rules, key=lambda r: r.priority, reverse=True)

    def clear_rules(self) -> None:
        """Clear all rules."""
        self.rules.clear()
        self._loaded_rules.clear()
