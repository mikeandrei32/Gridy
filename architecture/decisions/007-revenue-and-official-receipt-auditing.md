# ADR 007: Treasury Revenue Auditing and Official Receipt (O.R.) Compliance

## Status
Accepted

## Context
Under the Local Government Code of 1991 (RA 7160) and Commission on Audit (COA) regulations, barangays must collect statutory fees for clearances, certifications, and business permits. All collections must be documented using government-issued, serialized Official Receipts (O.R.) issued by the Barangay Treasurer.

A document management platform lacking financial tracking creates an unresolvable audit discrepancy between digital document releases and physical treasury logbooks.

## Decision
We integrated statutory treasury and revenue auditing directly into the document lifecycle:
1. **Financial Metadata Fields**: Added `or_number` (`CharField(max_length=50, blank=True, null=True)`) and `fee_amount` (`DecimalField(max_digits=8, decimal_places=2, default=0.00)`) to `DocumentRequest`.
2. **Treasury Slip on PDF Artifacts**: Updated the server-side PDF generator (`xhtml2pdf`) to render a standardized Official Assessment Slip at the bottom of legal clearances, showing:
   - Control Number / Request ID
   - Official Receipt (O.R.) Number
   - Amount Paid in Philippine Pesos (PHP)
   - Official Release Date & Timestamp
3. **Desk Treasury Input**: Enhanced the Executive Desk UI (`ReviewDocumentModal.tsx`) and Walk-in Creation modal to require O.R. and Fee specification prior to document release.
4. **Server-Side Aggregation**: Added real-time revenue computation in `DashboardSummaryView` using:
   `revenue=Sum('fee_amount', filter=Q(status=DocumentRequest.Status.RELEASED))`

## Consequences
* **Positive**: Full compliance with Philippine COA standards and LGU revenue auditing guidelines.
* **Positive**: Enables instant reconciliation between physical treasury receipt booklets and digital clearance issuance logs.
* **Positive**: Executive leadership gains immediate visibility into clearance fee collections on the admin dashboard without manual spreadsheet tracking.
* **Negative**: Introduces a minor administrative requirement for desk officials to record receipt numbers during document processing.