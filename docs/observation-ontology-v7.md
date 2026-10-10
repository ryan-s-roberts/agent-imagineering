# General observations — evidence ontology v7

ObservationRecord expresses a source claim about an existing entity. It does not require
a maintenance request, and cannot create a subject or resolve its identity. Its subject
can be any entity kind whose source supports the attributed property.

Fields:

- `subject_id`: existing case-local entity ID.
- `location_text`: source-stated location, or null; does not manufacture a room entity.
- `observation_kind`: measurement, setting, rating, presence, or physical_condition.
- `attribute`: semantic property observed, stated without an inferred diagnosis.
- `value`: tagged number with nullable source-stated unit, text, or boolean.
- `quoted_expression`: exact source expression including hedges and negation.
- `epistemic_status`: asserted, appears, uncertain, or not_verified. Asserted means the
  source asserts it, never that the evaluator independently verified it.
- `observed_at_text`: stated observation time or null, distinct from attachment availability.

Inherited provenance preserves origin, modality, polarity and identifiable author. A PDF
claim remains document_report. An uploader is not necessarily an author. Planned or
conditional observations cannot establish actual current state. Unknown authors stay null.
Every populated semantic field requires source spans; the exact quote field must be backed
by its identical source expression. Absence claims use presence + boolean false and source
negative polarity; consumers must not apply a second boolean inversion.

Numbers retain explicitly stated units; omitted units remain null. Text preserves ratings
and physical descriptions without forcing them into numeric scales. A device setting is
not proof it functions; a condition description is not a repair authorization. Workflow
ConditionRecord retains its existing meaning and is not used for physical findings.

This extension is domain-general. The independent prompt examples concern a sensor,
stain and latch rating. Existing development PDFs motivated the representational gap;
results are therefore development evidence, not untouched evaluation evidence. No new
model run has yet evaluated v7. Frozen evidence-v6 runs remain intact.
