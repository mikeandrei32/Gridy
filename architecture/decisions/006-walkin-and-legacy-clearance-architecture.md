# ADR 006: Hybrid Walk-in and Legacy Clearance Architecture

## Status
Accepted

## Context
In Philippine Barangay Governance, a substantial demographic of constituents (e.g., senior citizens, underprivileged residents, or individuals without internet connectivity) request certificates and clearances via physical walk-in visits. 

Standard SaaS applications strictly require an authenticated user account for every entity creation (`DocumentRequest.user = ForeignKey(User)`). Requiring digital accounts for walk-ins in an LGU setting forced desk clerks to either create fabricated "phantom" user accounts or continue issuing manual paper certificates outside the system, defeating the purpose of an enterprise record management platform.

## Decision
We adopted a **Hybrid Nullable Tenant Model** on `DocumentRequest`:
1. **Nullable User Mapping**: The `user` foreign key is configured as `null=True, blank=True, on_delete=models.CASCADE`.
2. **Direct Tenant Anchor**: We introduced a direct `barangay` foreign key (`ForeignKey(Barangay, on_delete=models.CASCADE, null=True, blank=True)`). For digital requests, tenant ownership is inferred through `user.barangay`; for walk-in requests, it is explicitly bound to the creating official's `user.barangay`.
3. **Walk-in Metadata Fields**: Added indexed `is_walkin` boolean, `walkin_name` (`CharField(255)`), and `walkin_purok` (`CharField(100)`).
4. **Role-Based Creation Interception**: Only users with `ADMIN` or `FIELD_OFFICIAL` roles can set `is_walkin=True` and define `walkin_name`. Unauthenticated or resident users attempting to generate walk-in records are rejected with `403 Forbidden`.
5. **Unified Query Boundaries**: All queryset lookups and aggregation statistics unify both categories via:
   `Q(user__barangay=user.barangay) | Q(barangay=user.barangay)`

## Consequences
* **Positive**: Eliminates phantom user creation, preventing database bloat and maintaining clean authentication tables.
* **Positive**: Fully accommodates non-digital citizens, ensuring 100% of barangay document issuances are accounted for digitally.
* **Positive**: Maintains strict multi-tenant data isolation per ADR 004.
* **Negative**: Requires dual-path ORM filtering (`Q` objects) across all viewsets, serializers, and aggregation queries instead of single-column joins.