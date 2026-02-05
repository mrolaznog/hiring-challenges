# Time Spent (6 hours)

## Summary

Refactored and productionalised the backend by cleaning the API layer, consolidating services, improving data access, and adding tests and configuration/logging improvements. Focus was on correctness, consistency, and maintainability.

## Breakdown

### 0) Initial Assessment (~1h)

- Read the existing codebase, flow and data files.
- Identified layers (API, services, data access, schemas, utilities, app setup).
- Scoped refactor tasks and prioritized fixes.

### 1) API Layer (~1h 20m)

- Consolidated routers to one per resource and removed duplicates.
- Standardized versioning under `/api/v1` and added JSON health endpoint.
- Normalized responses to Pydantic models and centralized error handling.
- Improved request validation for IDs and date ranges.

### 2) Service Layer (~1h)

- Removed duplicate service entrypoints and clarified public interfaces.
- Moved business logic to services (validation, stats, formatting).
- Added logging in service actions.
- Ensured services return Pydantic models consistently.

### 3) Data Access Layer (~1h)

- Removed duplicate DB helpers and normalized field names.
- Replaced fake measurements with CSV-backed reads.
- Added file-path configuration, I/O error handling, and caching.
- Ensured consistent snake_case shapes across signal/measurement data.

### 4) Schemas & Models (~40m)

- Removed unused/duplicate schemas and deprecated models.
- Aligned schemas with normalized data shapes.
- Added validators and OpenAPI examples.

### 5) Utilities/Helpers (~30m)

- Removed unused helpers and legacy utility exports.
- Kept only used utilities and eliminated I/O in helpers.

### 6) App Setup + Tests (~30m)

- Added logging config and app lifecycle hooks.
- Added CORS middleware.
- Made reload behavior conditional on `debug_mode`.
- Added unit tests for services, utilities, and data access.
- Updated dependencies for testing and settings.

## Notes

- Some legacy/demo assets (templates/static) and unused helpers were identified for removal.
- Assumed pytest was acceptable for unit tests.
- Used formatter across codebase

## Out of Scope (Nice-to-Have)

- Auth (API keys/JWT) and rate limiting.
- Structured logging with request IDs and correlation IDs.
- Async file I/O or background caching for large CSVs.
- CI pipeline for linting/tests and coverage reports.
