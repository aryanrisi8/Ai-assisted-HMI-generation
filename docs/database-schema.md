# PostgreSQL Database Schema

## ER Diagram Description

```text
roles 1 ──── * users

users 1 ──── * dashboards
users 1 ──── * alarm_history
users 1 ──── * assistant_logs

industrial_systems 1 ──── * industrial_systems
industrial_systems 1 ──── * signals
industrial_systems 1 ──── * dashboards

signals 1 ──── * alarms
signals 1 ──── * components

alarms 1 ──── * alarm_history

template_categories 1 ──── * template_categories
template_categories 1 ──── * templates

templates 1 ──── * dashboards

dashboards 1 ──── * dashboard_layouts
dashboards 1 ──── * components
dashboards 1 ──── * assistant_logs

components 1 ──── * components
```

## Table Responsibilities

### `roles`

Stores authorization profiles for operators, engineers, admins, and system users.

- `permissions` is JSON to support fine-grained feature flags and capability maps.
- `name` is globally unique.
- System roles are protected by `is_system_role`.

### `users`

Stores platform identities.

- Belongs to one `role`.
- Owns dashboards and assistant logs.
- Can be recorded as the actor for alarm history events.
- `hashed_password` is persisted only in the SQLAlchemy model and is intentionally excluded from Pydantic read schemas.

### `industrial_systems`

Stores the plant hierarchy, such as site, area, line, cell, machine, or subsystem.

- Self-referencing `parent_id` supports nested equipment trees.
- `code` is globally unique for deterministic references.
- Connected to signals and dashboards.

### `signals`

Stores process variables, status points, calculated points, and command points.

- Belongs to an industrial system.
- Can drive alarms and HMI components.
- `tag` is globally unique.
- Engineering range is constrained with `min_value <= max_value`.

### `alarms`

Stores configured alarm definitions and current alarm state.

- Belongs to one signal.
- Maintains current lifecycle fields such as `active_at`, `acknowledged_at`, and `cleared_at`.
- Lifecycle events are stored separately in `alarm_history`.

### `alarm_history`

Stores immutable alarm lifecycle events.

- Includes event type, previous state, new state, value snapshot, actor, and timestamp.
- Optimized for alarm timeline and historical analytics queries.

### `template_categories`

Stores reusable template taxonomy.

- Self-referencing hierarchy supports categories such as process, utility, alarm, dashboard, and equipment-specific templates.

### `templates`

Stores reusable HMI and dashboard schema templates.

- `schema_json` stores the template structure.
- `version` supports template evolution.
- Used as a source for dashboards.

### `dashboards`

Stores user-facing HMI dashboard metadata.

- Belongs to an owner.
- Can be attached to an industrial system and initialized from a template.
- Contains layouts and components.
- `status` separates drafts, published dashboards, and archived dashboards.

### `dashboard_layouts`

Stores React Grid Layout configuration per dashboard and breakpoint.

- Unique by `dashboard_id` and `breakpoint`.
- `layout_json` stores grid coordinates, width, height, and responsive layout metadata.

### `components`

Stores dashboard component instances.

- Belongs to a dashboard.
- May bind to a signal.
- May be nested under another component.
- Stores schema-driven rendering fields: props, style, bindings, interactions, visibility rules, and registry version.

### `assistant_logs`

Stores AI assistant activity for auditability and improvement.

- Can link to a user and dashboard.
- Covers HMI generation, alarm intelligence, schema validation, and user query activity.
- Stores request and response JSON for traceability.

## Key Relationships

- `roles.id` to `users.role_id`: restrict deletion while users still reference the role.
- `industrial_systems.id` to `industrial_systems.parent_id`: self-referencing hierarchy.
- `industrial_systems.id` to `signals.industrial_system_id`: cascading delete removes child signals.
- `signals.id` to `alarms.signal_id`: cascading delete removes alarm definitions tied to removed signals.
- `alarms.id` to `alarm_history.alarm_id`: cascading delete removes history for deleted alarm definitions.
- `template_categories.id` to `templates.category_id`: restrict deletion while templates exist.
- `dashboards.id` to `dashboard_layouts.dashboard_id`: cascading delete removes dashboard layouts.
- `dashboards.id` to `components.dashboard_id`: cascading delete removes dashboard components.
- `components.id` to `components.parent_component_id`: cascading delete removes nested component children.

## Constraints

- Unique role names.
- Unique user email and username.
- Unique industrial system code.
- Unique signal tag.
- Unique signal name within an industrial system.
- Unique alarm code.
- Unique alarm name within a signal.
- Unique category slug.
- Unique category name within a parent category.
- Unique template slug.
- Unique dashboard slug.
- Unique layout breakpoint per dashboard.
- Unique component key per dashboard.
- Positive scan rates, layout columns, row heights, template versions, dashboard schema versions.
- Non-negative alarm delay, deadband, and assistant latency.

## Index Strategy

### Identity

- `roles.name`
- `users.email`
- `users.username`
- `users.role_id`

### Plant Model

- `industrial_systems.parent_id`
- `industrial_systems.code`
- `industrial_systems.system_type, industrial_systems.status`
- `signals.industrial_system_id`
- `signals.tag`
- `signals.data_type`

### Alarm Operations

- `alarms.signal_id`
- `alarms.code`
- `alarms.state, alarms.severity`
- `alarms.active_at`
- `alarm_history.alarm_id, alarm_history.occurred_at`
- `alarm_history.actor_id`
- `alarm_history.event_type`
- `alarm_history.occurred_at`

### Dashboard Runtime

- `dashboards.owner_id`
- `dashboards.industrial_system_id`
- `dashboards.template_id`
- `dashboards.status`
- `dashboards.slug`
- `dashboard_layouts.dashboard_id`
- `components.dashboard_id`
- `components.signal_id`
- `components.parent_component_id`
- `components.type`

### Assistant Traceability

- `assistant_logs.user_id`
- `assistant_logs.dashboard_id`
- `assistant_logs.log_type`
- `assistant_logs.created_at`

## Migration Strategy

### Tooling

Use Alembic for schema migrations and SQLAlchemy metadata as the source of truth.

Recommended files:

```text
backend/
  alembic.ini
  app/
    models.py
  migrations/
    env.py
    versions/
```

### Initial Migration

1. Create PostgreSQL extensions needed by the platform.
2. Create enum types before tables.
3. Create parent tables first: `roles`, `template_categories`, `industrial_systems`.
4. Create dependent tables: `users`, `signals`, `templates`, `dashboards`.
5. Create child tables: `alarms`, `dashboard_layouts`, `components`, `alarm_history`, `assistant_logs`.
6. Create indexes and constraints.
7. Seed minimum roles and template categories in a separate data migration.

### Migration Rules

- Never edit an applied migration.
- Prefer additive migrations for production systems.
- Backfill data before adding non-null constraints to existing populated tables.
- Add indexes concurrently for large production tables.
- Use explicit enum migration steps when adding enum values.
- Keep data migrations separate from structural migrations when possible.
- Include downgrade steps for development and staging, but treat production downgrades as emergency operations requiring a backup and runbook.

### Versioning Policy

- `dashboards.schema_version` tracks schema-driven rendering compatibility.
- `templates.version` tracks reusable template evolution.
- `components.registry_version` tracks the component registry contract used by the component instance.

### Seed Data

Initial seed data should include:

- Roles: `admin`, `engineer`, `operator`, `viewer`.
- Template categories: `process`, `alarm`, `utility`, `overview`, `equipment`.
- Optional starter templates for blank dashboard and alarm console.

### Operational Considerations

- Partition `alarm_history` by month if event volume is high.
- Retain `assistant_logs` according to governance and privacy policy.
- Add GIN indexes for frequently queried JSON fields only after query patterns are known.
- Keep alarm state in `alarms` for fast current-state queries and immutable event history in `alarm_history`.
- Use backups before migrations that rewrite large JSON fields.
