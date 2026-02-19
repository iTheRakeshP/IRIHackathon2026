# PlantUML - Business-Focused Diagram Pack

This folder provides non-sequence diagrams for explaining the hackathon flow from a business perspective.

## Diagram Set

1. `01-nightly-batch-business-flow.puml`
   - End-to-end overnight processing view
   - Inputs, rule/scoring passes, and output consumption in UI

2. `02-ui-advisor-review-workflow.puml`
   - Advisor journey from dashboard to module actions
   - Includes replacement, income activation, suitability drift, and missing info branches

3. `03-alert-catalog-and-logic-map.puml`
   - Alert taxonomy + trigger gates + weighted scoring logic
   - Good for stakeholder walkthroughs and governance conversations

4. `04-alert-generation-decision-tree.puml`
   - Per-policy decision tree showing when each alert is created and severity assignment

## Visual Theme

All diagrams use a **professional corporate color palette** with consistent styling:

### Color System
- **Primary Blue** (#1E40AF): Main borders, titles, and system processes
- **Secondary Teal** (#0891B2): Data flows and API interactions
- **Light Background** (#F8FAFC): Clean, professional presentation backdrop

### Alert-Type Colors (Consistent Across All Diagrams)
- **Replacement**: Soft red tones (#FEE2E2 to #DC2626) - High-priority recommendations
- **Income Activation**: Professional amber (#FEF3C7 to #F59E0B) - Timing decisions
- **Suitability Drift**: Fresh green (#D1FAE5 to #10B981) - Periodic reviews
- **Missing Info**: Warm orange (#FDEDD3 to #F97316) - Administrative updates

### Design Principles
- **Shadowing & Roundness**: Modern, polished appearance
- **Bold Borders**: Clear visual hierarchy (2px thickness)
- **Segoe UI Font**: Professional, readable typeface
- **Graduated Shades**: Lighter for context, darker for outcomes

This unified palette ensures all diagrams work together in presentations, governance reviews, and stakeholder demos.

## Render in VS Code

- Install extension: `jebbs.plantuml`
- Open any `.puml` file
- Use `Alt + D` for preview

## Export with PlantUML CLI (optional)

From repo root:

```bash
java -jar plantuml.jar diagrams/plantuml/*.puml
```

This generates PNG files beside each source file.
