# Feature Specification: Walk-in Clearances & Treasury Revenue Auditing

## 1. Overview
Philippine local governance requires accommodating physical walk-in constituents who lack internet access or smartphones, while strictly accounting for regulatory fees per Commission on Audit (COA) standards and the Local Government Code of 1991 (RA 7160). This feature provides hybrid clearance handling, serialized Official Receipt (O.R.) auditing, dynamic PDF assessment slips, and real-time revenue KPIs.

---

## 2. Technical Architecture

### 2.1 Hybrid Data Model (`DocumentRequest`)
*   **Nullable User FK:** `user = ForeignKey(User, null=True, blank=True)`. Eliminates the need to fabricate phantom accounts for walk-in residents.
*   **Direct Tenant FK:** `barangay = ForeignKey(Barangay, null=True, blank=True)`. Anchors multi-tenant jurisdiction when `user` is null.
*   **Constituent Metadata:** `is_walkin` (indexed boolean), `walkin_name` (`CharField(255)`), and `walkin_purok` (`CharField(100)`).
*   **Treasury Auditing:** `or_number` (`CharField(50)`) and `fee_amount` (`DecimalField(max_digits=8, decimal_places=2)`).

### 2.2 Dual-Path ORM Query Isolation
All aggregation queries, viewsets, and list lookups enforce tenant boundaries without omitting walk-in records via:
```python
DocumentRequest.objects.filter(
    Q(user__barangay=user.barangay) | Q(barangay=user.barangay)
)
