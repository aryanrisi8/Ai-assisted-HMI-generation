# AI-Assisted Adaptive HMI Generation and Alarm Intelligence Platform

## 1. Target Folder Tree

```text
hmi-platform/
  README.md
  ARCHITECTURE.md
  .env.example
  docker-compose.yml

  frontend/
    package.json
    vite.config.js
    tailwind.config.js
    postcss.config.js
    index.html
    public/
      assets/
      icons/
      templates/
    src/
      main.jsx
      App.jsx
      routes/
        AppRoutes.jsx
        ProtectedRoute.jsx
        routeConfig.js
      layouts/
        AuthLayout.jsx
        DashboardLayout.jsx
        EngineeringLayout.jsx
        RuntimeLayout.jsx
      pages/
        auth/
          LoginPage.jsx
          RegisterPage.jsx
        dashboard/
          OverviewPage.jsx
          PlantSummaryPage.jsx
        hmi-builder/
          HmiProjectsPage.jsx
          HmiEditorPage.jsx
          HmiPreviewPage.jsx
          HmiRuntimePage.jsx
        alarms/
          AlarmConsolePage.jsx
          AlarmAnalyticsPage.jsx
          AlarmRulesPage.jsx
          AlarmInvestigationPage.jsx
        assets/
          AssetHierarchyPage.jsx
          TagBrowserPage.jsx
        admin/
          UsersPage.jsx
          RolesPage.jsx
          AuditLogPage.jsx
      modules/
        auth/
          authService.js
          authStore.js
          authTypes.js
        hmi/
          hmiService.js
          hmiStore.js
          schema/
            hmiSchemaTypes.js
            validators.js
            schemaVersioning.js
          renderer/
            SchemaRenderer.jsx
            RenderContext.jsx
            bindingResolver.js
            visibilityResolver.js
            interactionResolver.js
          registry/
            componentRegistry.js
            componentManifest.js
            componentLoader.js
        alarms/
          alarmService.js
          alarmStore.js
          alarmSeverity.js
          alarmTimeline.js
          alarmCorrelation.js
        assets/
          assetService.js
          tagService.js
          tagBinding.js
        analytics/
          chartService.js
          trendTransforms.js
          rechartsAdapters.js
        ai/
          aiGenerationService.js
          promptTemplates.js
          generationSessionStore.js
      components/
        common/
          Button.jsx
          Input.jsx
          Modal.jsx
          Table.jsx
          Tabs.jsx
          Toast.jsx
          EmptyState.jsx
          LoadingState.jsx
        navigation/
          Sidebar.jsx
          Topbar.jsx
          Breadcrumbs.jsx
        hmi/
          canvas/
            HmiCanvas.jsx
            GridCanvas.jsx
            SelectionOverlay.jsx
            ResizeHandles.jsx
          properties/
            PropertyPanel.jsx
            BindingPanel.jsx
            StylePanel.jsx
            InteractionPanel.jsx
          palette/
            ComponentPalette.jsx
            SymbolLibrary.jsx
          widgets/
            NumericDisplay.jsx
            StatusIndicator.jsx
            ValveSymbol.jsx
            PumpSymbol.jsx
            TankSymbol.jsx
            TrendChart.jsx
            AlarmBanner.jsx
        alarms/
          AlarmTable.jsx
          AlarmCard.jsx
          AlarmTimeline.jsx
          AlarmPriorityMatrix.jsx
          RootCausePanel.jsx
          RecommendationPanel.jsx
      services/
        apiClient.js
        tokenStorage.js
        websocketClient.js
        errorHandler.js
      hooks/
        useAuth.js
        useApi.js
        useWebSocket.js
        useHmiSchema.js
        useAlarmStream.js
        useTagValues.js
      styles/
        index.css
        tailwind.css
      utils/
        dateTime.js
        formatters.js
        permissions.js
        schemaDiff.js
      config/
        environment.js
        featureFlags.js
      tests/
        unit/
        integration/
        e2e/

  backend/
    pyproject.toml
    alembic.ini
    app/
      main.py
      core/
        config.py
        security.py
        jwt.py
        permissions.py
        logging.py
        exceptions.py
      api/
        v1/
          router.py
          endpoints/
            auth.py
            users.py
            roles.py
            assets.py
            tags.py
            hmi_projects.py
            hmi_schemas.py
            hmi_generation.py
            hmi_runtime.py
            alarms.py
            alarm_rules.py
            alarm_intelligence.py
            analytics.py
            audit.py
      db/
        session.py
        base.py
        migrations/
      models/
        user.py
        role.py
        asset.py
        tag.py
        hmi_project.py
        hmi_schema.py
        hmi_component.py
        alarm.py
        alarm_rule.py
        alarm_event.py
        alarm_insight.py
        generation_session.py
        audit_log.py
      schemas/
        auth.py
        user.py
        asset.py
        tag.py
        hmi_project.py
        hmi_schema.py
        hmi_generation.py
        alarm.py
        alarm_rule.py
        alarm_intelligence.py
        analytics.py
      services/
        auth_service.py
        user_service.py
        asset_service.py
        tag_service.py
        hmi_project_service.py
        hmi_schema_service.py
        hmi_generation_service.py
        component_registry_service.py
        runtime_binding_service.py
        alarm_service.py
        alarm_rule_service.py
        alarm_correlation_service.py
        alarm_intelligence_service.py
        analytics_service.py
        audit_service.py
      repositories/
        user_repository.py
        asset_repository.py
        tag_repository.py
        hmi_repository.py
        alarm_repository.py
        analytics_repository.py
        audit_repository.py
      intelligence/
        alarm/
          correlation_engine.py
          root_cause_engine.py
          suppression_engine.py
          priority_engine.py
          recommendation_engine.py
          pattern_detector.py
        hmi_generation/
          layout_planner.py
          schema_generator.py
          component_selector.py
          binding_mapper.py
          validation_engine.py
      registry/
        component_manifest.py
        component_catalog.py
        schema_contracts.py
      realtime/
        websocket_manager.py
        alarm_stream.py
        tag_value_stream.py
      workers/
        alarm_analysis_worker.py
        hmi_generation_worker.py
        notification_worker.py
      tests/
        unit/
        integration/
        api/

  docs/
    architecture/
      system-context.md
      frontend-architecture.md
      backend-architecture.md
      database-design.md
      component-registry.md
      schema-driven-rendering.md
      alarm-intelligence.md
      api-boundaries.md
      security-model.md
      roadmap.md
    diagrams/
      context-diagram.md
      data-flow.md
      alarm-flow.md
      hmi-generation-flow.md
```

## 2. System Overview

The platform generates, renders, operates, and improves industrial HMI screens from structured schemas. It combines a React engineering console, a schema-driven runtime renderer, FastAPI service boundaries, PostgreSQL persistence, and alarm intelligence services for correlation, prioritization, root-cause analysis, and operator recommendations.

Primary product areas:

- HMI engineering workspace
- Schema-driven HMI runtime
- Component registry and symbol library
- Asset hierarchy and tag binding
- Alarm console and alarm analytics
- AI-assisted HMI generation
- Alarm intelligence and recommendations
- Admin, RBAC, and auditability

## 3. Frontend Module Responsibilities

### Auth Module

- Owns login, logout, token refresh, current-user state, and protected route guards.
- Uses Axios interceptors for JWT attachment and authentication failure handling.
- Exposes role and permission helpers to hide or disable restricted UI.

### Routing And Layouts

- React Router defines isolated route groups for authentication, dashboard, engineering, runtime, alarms, assets, and admin.
- Layouts provide navigation shell, permission-aware sidebars, page headers, and runtime-only display modes.

### HMI Builder Module

- Owns project list, editor workspace, grid canvas, component palette, property panels, schema preview, and version actions.
- Uses React Grid Layout for placement, resizing, snapping, and layout persistence.
- Produces schema documents rather than hard-coded React screens.

### Schema Renderer Module

- Converts HMI schema JSON into React components at runtime.
- Resolves component type, props, style, data bindings, visibility rules, interactions, alarms, and permissions.
- Keeps rendering deterministic and versioned so saved HMI schemas remain reproducible.

### Component Registry Module

- Maps schema component types to React components.
- Stores component metadata, supported properties, binding capabilities, validation rules, icons, categories, and runtime constraints.
- Separates engineering-time metadata from runtime rendering behavior.

### Alarm Module

- Provides live alarm table, alarm details, acknowledgement workflow, shelving, filtering, timeline views, analytics, and investigation panels.
- Consumes REST APIs for history and WebSocket streams for live events.
- Displays intelligence outputs such as probable causes, correlated alarms, recommended actions, and confidence scores.

### Asset And Tag Module

- Manages plant hierarchy, equipment, tag browser, tag metadata, and tag-to-component bindings.
- Provides reusable selectors for HMI builder and alarm rule configuration.

### Analytics Module

- Owns trend visualizations, alarm frequency charts, severity distributions, operator response metrics, and equipment health summaries.
- Uses Recharts adapters so API response shapes do not leak into chart components.

### AI Generation Module

- Manages generation sessions, prompts, generated schema drafts, validation feedback, and human approval.
- Treats AI output as proposed schema changes, not directly deployed runtime screens.

## 4. Backend Module Responsibilities

### API Layer

- FastAPI routers expose versioned REST endpoints under `/api/v1`.
- Endpoint modules remain thin and delegate business behavior to services.
- Request and response contracts are defined with Pydantic schemas.

### Core Layer

- Owns application config, JWT security, password hashing, RBAC checks, logging, exception handling, and environment settings.
- Provides cross-cutting utilities used by all service modules.

### Model Layer

- SQLAlchemy ORM models represent persisted domain entities.
- Models define relationships, indexes, constraints, and lifecycle timestamps.

### Repository Layer

- Encapsulates database access patterns.
- Keeps service logic independent from query details.
- Provides focused query methods for HMI schemas, alarm history, asset hierarchy, and analytics.

### Service Layer

- Owns business workflows and transaction boundaries.
- Coordinates repositories, validation engines, intelligence engines, audit logging, and realtime publishing.

### Intelligence Layer

- Contains alarm correlation, root-cause analysis, suppression, priority scoring, recommendation, pattern detection, and HMI generation logic.
- Designed so heuristic, rules-based, statistical, and AI-backed engines can evolve independently.

### Realtime Layer

- Manages WebSocket connections and event fan-out.
- Publishes alarm streams, tag value streams, HMI runtime updates, and generation status events.

### Worker Layer

- Runs longer background tasks such as alarm analysis, HMI generation, notification dispatch, and batch analytics.
- Keeps API request-response flows responsive.

## 5. API Service Boundaries

### Auth Service

- Login, refresh token, logout, current user, password management.
- Owns JWT issuance and token validation.

### User And RBAC Service

- Users, roles, permissions, operator groups, engineering groups.
- Enforces access to projects, assets, alarm actions, and admin screens.

### Asset And Tag Service

- Plant hierarchy, equipment models, tags, tag metadata, tag history references.
- Provides search and browse APIs for HMI binding and alarm rules.

### HMI Project Service

- HMI projects, screens, schema versions, publish workflow, rollback, draft management.
- Separates editable schemas from published runtime schemas.

### HMI Generation Service

- Accepts generation requests from prompts, asset selections, existing screens, templates, or alarm context.
- Produces validated schema drafts with explanations and warnings.

### Component Registry Service

- Serves registry manifests to the frontend.
- Validates whether schema components are supported by the current platform version.

### HMI Runtime Service

- Serves published schemas and runtime configuration.
- Resolves allowed data bindings and runtime permissions.

### Alarm Service

- Alarm ingestion, live state, history, acknowledgement, shelving, comments, ownership, and lifecycle transitions.

### Alarm Rule Service

- Alarm definitions, thresholds, severities, suppression rules, escalation policies, and notification routing.

### Alarm Intelligence Service

- Correlation groups, probable root causes, alarm flood detection, nuisance alarm detection, priority recommendations, and operator guidance.

### Analytics Service

- Dashboard summaries, trend data, alarm KPIs, response metrics, equipment alarm rates, and audit analytics.

### Audit Service

- Records security, engineering, runtime, and alarm actions.
- Supports traceability for regulated industrial environments.

## 6. Database Structure

### Identity And Access

- `users`: account profile, email, password hash, status, last login.
- `roles`: named role definitions.
- `permissions`: granular capabilities.
- `user_roles`: user-to-role mapping.
- `role_permissions`: role-to-permission mapping.

### Asset And Tag Model

- `assets`: hierarchical plant/equipment structure with parent-child relationships.
- `asset_types`: reusable equipment classifications.
- `tags`: process variables, status tags, command tags, and calculated tags.
- `tag_metadata`: units, ranges, historian references, quality rules.
- `tag_bindings`: reusable references between tags and HMI/alarm entities.

### HMI Engineering

- `hmi_projects`: project metadata, owner, lifecycle state.
- `hmi_screens`: screen metadata within a project.
- `hmi_schema_versions`: versioned schema JSON, validation status, author, publish status.
- `hmi_components`: optional indexed component records extracted from schemas for search and impact analysis.
- `hmi_templates`: reusable screen and component templates.
- `generation_sessions`: AI-assisted generation requests, outputs, validation results, and approval status.

### Component Registry

- `component_categories`: display groups such as process, control, alarm, chart, layout.
- `component_definitions`: canonical component types, versions, manifest metadata.
- `component_property_definitions`: editable property contracts.
- `component_binding_definitions`: supported data binding contracts.

### Alarm Management

- `alarm_rules`: alarm definitions, thresholds, severity, asset/tag association.
- `alarm_events`: immutable alarm lifecycle events.
- `alarm_states`: current active, acknowledged, shelved, cleared state.
- `alarm_comments`: operator and engineer annotations.
- `alarm_shelves`: shelving intervals and reasons.
- `alarm_correlations`: grouped related alarms.
- `alarm_insights`: root cause, recommendations, confidence, and generated intelligence output.

### Analytics And Audit

- `audit_logs`: actor, action, entity type, entity ID, before/after metadata, timestamp.
- `metric_snapshots`: precomputed operational metrics.
- `notification_events`: escalation and notification history.

## 7. Component Registry Architecture

The component registry is the contract between generated schemas, engineering tools, and runtime rendering.

Each component definition contains:

- Stable `type` identifier, such as `process.pump` or `chart.trend`.
- Semantic version.
- Display name, category, icon, and palette placement.
- React runtime component mapping.
- Engineering editor metadata.
- Property schema.
- Binding schema.
- Event and interaction schema.
- Validation rules.
- Default dimensions for React Grid Layout.
- Runtime permissions and safety constraints.

Registry layers:

- Backend catalog: authoritative component manifest and compatibility rules.
- Frontend registry: maps component types to React components and editor panels.
- Schema validator: checks generated and manually edited schemas against registry contracts.
- Migration adapter: upgrades old schema versions when component contracts evolve.

Design principles:

- Schemas reference component types, not file paths.
- Component versions must remain backward-compatible or provide migrations.
- Engineering metadata can change without breaking published runtime rendering.
- Runtime rendering must fail gracefully for unsupported or deprecated components.

## 8. Schema-Driven Rendering Architecture

### Schema Document Shape

An HMI screen schema should describe:

- Screen identity and schema version.
- Grid layout and responsive breakpoints.
- Component instances.
- Component props.
- Data bindings.
- Conditional visibility and style rules.
- Interaction definitions.
- Alarm overlays and alarm state mappings.
- Permissions.
- Runtime refresh requirements.

### Rendering Flow

1. Runtime loads the published HMI schema.
2. Schema validator checks version, registry compatibility, and required bindings.
3. Renderer creates a render context with user, permissions, tag values, alarm states, and theme.
4. Component resolver maps schema component types to registered React components.
5. Binding resolver injects live tag values and quality states.
6. Visibility and interaction resolvers evaluate rules.
7. Components render using deterministic props derived from schema and runtime context.
8. WebSocket updates refresh bound values, alarm overlays, and runtime state.

### Engineering Flow

1. User creates or edits a screen in the HMI builder.
2. Canvas stores layout using React Grid Layout.
3. Property panels update schema component props and bindings.
4. Validator continuously checks registry compatibility.
5. Preview uses the same renderer as runtime.
6. Publishing freezes a schema version and makes it available to runtime routes.

### AI Generation Flow

1. User requests a screen from natural language, selected assets, templates, or alarm context.
2. Backend generation service creates a proposed schema.
3. Validation engine checks schema structure, component compatibility, layout quality, and binding availability.
4. Frontend presents generated draft for review.
5. Engineer edits, validates, and explicitly publishes.

## 9. Alarm Intelligence Architecture

### Alarm Data Flow

1. Alarm events enter through ingestion APIs or integration adapters.
2. Alarm service normalizes events and updates current alarm state.
3. Realtime layer broadcasts active alarm changes to clients.
4. Alarm intelligence workers analyze event windows, equipment relationships, severity patterns, and historical recurrence.
5. Intelligence outputs are stored as alarm insights and correlation records.
6. Alarm console displays prioritized, explainable recommendations.

### Intelligence Capabilities

- Alarm flood detection.
- Correlated alarm grouping.
- Probable root-cause ranking.
- Nuisance alarm detection.
- Dynamic priority recommendations.
- Suppression suggestions.
- Operator response recommendations.
- Recurring pattern detection.
- Asset-level alarm health scoring.

### Engine Responsibilities

- Correlation engine groups alarms by time window, asset hierarchy, tag relationships, and configured process dependencies.
- Root-cause engine ranks likely initiating alarms using chronology, topology, severity, and historical patterns.
- Suppression engine identifies alarms that may be hidden, delayed, or grouped under defined operating states.
- Priority engine recommends severity changes based on frequency, consequence, operator response, and alarm philosophy rules.
- Recommendation engine produces operator guidance with confidence, supporting evidence, and required verification steps.
- Pattern detector finds repeating alarm sequences and nuisance candidates.

### Explainability Requirements

Every alarm intelligence result should include:

- Confidence score.
- Evidence list.
- Related alarm IDs.
- Related assets and tags.
- Time window used for analysis.
- Recommendation status.
- Human feedback status.

## 10. Security And Governance

- JWT authentication for API access.
- Role-based and permission-based authorization.
- Separate permissions for viewing, editing, publishing, acknowledging alarms, shelving alarms, managing rules, and administering users.
- Audit logs for schema edits, publishes, rollbacks, alarm actions, auth events, and admin changes.
- Published HMI schemas are immutable.
- AI-generated outputs require validation and human approval before publishing.

## 11. Development Roadmap

### Phase 1: Foundation

- Create React, Tailwind, React Router, Axios project shell.
- Create FastAPI, SQLAlchemy, PostgreSQL backend shell.
- Add JWT auth, RBAC model, base routing, and database migrations.
- Establish API client, route guards, layout shell, and audit logging.

### Phase 2: Asset And Tag Foundation

- Build asset hierarchy and tag metadata model.
- Add asset browser and tag browser.
- Define tag binding contracts for HMI components and alarm rules.
- Add realtime tag stream abstraction.

### Phase 3: Component Registry

- Define backend component manifest model.
- Define frontend registry mapping.
- Add registry validation and compatibility checks.
- Build initial industrial component set.

### Phase 4: Schema-Driven HMI Builder

- Build HMI project and screen management.
- Add React Grid Layout canvas.
- Add component palette and property panels.
- Add schema validation, preview, versioning, publish, and rollback.

### Phase 5: Runtime Renderer

- Implement published schema runtime loading.
- Add binding resolver, visibility resolver, and interaction resolver.
- Add WebSocket-driven tag and alarm state updates.
- Add runtime permission handling and graceful component fallback.

### Phase 6: Alarm Management

- Add alarm rules, alarm event ingestion, current state tracking, and alarm history.
- Build live alarm console with acknowledgement, shelving, comments, filters, and timeline.
- Add alarm analytics dashboards.

### Phase 7: Alarm Intelligence

- Add correlation, flood detection, nuisance detection, and root-cause ranking.
- Add recommendation panel and investigation workflow.
- Store feedback on intelligence results for future tuning.

### Phase 8: AI-Assisted HMI Generation

- Add generation sessions and draft schema workflow.
- Generate screens from prompts, asset selections, templates, and alarm contexts.
- Validate generated schemas against registry and binding contracts.
- Add review, edit, approve, and publish workflow.

### Phase 9: Hardening And Operations

- Add integration tests, API contract tests, frontend component tests, and runtime renderer tests.
- Add performance budgets for schema rendering and alarm streaming.
- Add observability, structured logs, backups, deployment scripts, and environment-specific configuration.

