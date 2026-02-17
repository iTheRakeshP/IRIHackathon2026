# AI-Powered In-Force Review Intelligence - Demo Script

**Hackathon Demo | February 2026**

---

## 🎯 Opening Pitch (30 seconds)

*"Advisors are drowning in policy reviews. With thousands of in-force annuities, how do you know WHICH policies need attention and WHY?*

*We built an AI-powered overnight batch system that analyzes client profiles, policy performance, and market alternatives to intelligently flag opportunities."*

---

## 📊 Act 1: The Algorithm (1 minute)

### Show Documentation
*Reference: [Functional_and_Technical_Doc_Angular19_FastAPI.md](Functional_and_Technical_Doc_Angular19_FastAPI.md) Section 2.5*

**Say:**
> *"Our AI uses three sophisticated scoring algorithms, each with weighted factors:"*

### 1. REPLACEMENT Alert Algorithm
```
AI analyzes 4 weighted factors:
├─ Performance Gap (40%)      → Cap rates, fees, crediting history
├─ Suitability Match (30%)    → Client objectives, risk tolerance
├─ Cost-Benefit (20%)         → Surrender penalties vs. gains
└─ Feature Upgrades (10%)     → Income riders, protection features

Formula: AI_Score = Σ(weighted_components)
Trigger: Score > 75 AND surrender penalty < expected gain
```

### 2. INCOME ACTIVATION Alert Algorithm
```
AI analyzes timing optimization:
├─ Rollup gains vs. income foregone
├─ Deferral bonus calculations
├─ Age-based payout thresholds
└─ Break-even analysis

Trigger: Within 90 days of optimal window OR urgency score > 60
```

### 3. SUITABILITY DRIFT Alert Algorithm
```
AI analyzes profile drift with weighted scoring:
├─ Risk Tolerance Change (35%)    → Conservative → Moderate
├─ Primary Objective Shift (30%)  → Growth → Income mismatch
├─ Financial Situation (20%)      → Net worth/income changes
└─ Time Horizon Change (15%)      → Shortened horizons

Trigger: Drift_Score > 50 OR critical mismatch detected
```

**Key Statement:**
> *"This isn't a simple threshold—it's multi-dimensional analysis of 23+ data points per policy."*

---

## 💻 Act 2: Live Demonstration (1-2 minutes)

### Step 1 - Run the Batch Process

**Action:**
```bash
cd API
.\.venv\Scripts\python batch_alert_generator.py
```

**Narrate while it runs:**
> *"Watch as our AI analyzes 23 policies in real-time... Each policy is evaluated against client suitability profiles, market benchmarks, and product catalog. The system is checking cap rate gaps, surrender schedules, income activation timing, and profile drift..."*

### Step 2 - Point to Console Output

**Show:**
```
📋 POL-90002 (Lincoln FIA (2016))
   Client: Milovich Pichirallo
   ✓ REPLACEMENT alert generated (Score: 77, Confidence: 0.87)
   ✓ SUITABILITY_DRIFT alert generated (Score: 35, Confidence: 0.72)
```

**Say:**
> *"See those scores? **77 with 87% confidence**—that's the AI quantifying WHY this policy needs review."*

### Step 3 - Show AI Analysis Output

**Action:** Open `API/data/alerts_generated.json`

**Navigate to ai_analysis section:**
```json
"ai_analysis": {
  "ai_score": 77,
  "confidence": 0.87,
  "scoring_breakdown": {
    "performance_gap": 30.6,           // ← POINT HERE
    "suitability_improvement": 24.5,
    "cost_savings": 16.8,
    "feature_upgrade": 5.5
  },
  "key_factors": [
    "Cap rate gap: current 3.4% vs. available 6.0% (76% improvement)",
    "Income rider opportunity: 7% rollup available",
    "Surrender period ending in 8 months"
  ],
  "data_points_analyzed": 23
}
```

**Narrate:**
> *"Here's the breakdown: **30.6 points from performance gap alone**—the policy's 3.4% cap rate vs. 6.0% market alternatives. The AI analyzed 23 data points to arrive at this score."*

**Point to specific fields:**
- **ai_score**: "Overall assessment: 77 out of 100"
- **confidence**: "87% confidence based on data completeness"
- **scoring_breakdown**: "Shows exactly where the score comes from"
- **key_factors**: "Human-readable explanations for advisors"
- **data_points_analyzed**: "23 individual data points considered"

---

## 🚀 Act 3: The Innovation (30 seconds)

### Highlight What's Unique

**1. Multi-Factor Weighted Scoring**
> *"Not just 'cap rate is low'—we're analyzing performance, suitability alignment, cost-benefit, AND feature gaps simultaneously."*

**2. Explainable AI**
> *"Every alert shows its work: AI score, confidence level, scoring breakdown, and key factors. Full transparency for compliance."*

**3. Context-Aware Analysis**
> *"Same cap rate gap might score differently based on client's risk tolerance, surrender schedule, and financial situation. The AI considers the FULL context."*

**4. Production-Ready**
> *"Overnight batch process analyzed 23 policies in under a second. In production, this scales to thousands of policies nightly."*

---

## 💼 Act 4: Business Impact (30 seconds)

### Show Results Summary

**Point to terminal output:**
```
✅ BATCH PROCESSING COMPLETE
   Policies Analyzed: 23
   Alerts Generated: 31
   - 7 REPLACEMENT opportunities (HIGH priority)
   - 2 INCOME_ACTIVATION timing discussions (MEDIUM priority)
   - 22 SUITABILITY_DRIFT reviews (LOW-MEDIUM priority)
```

**Narrate:**
> *"In seconds, we identified 7 high-priority replacement opportunities from 23 policies. Each with AI scoring to help advisors prioritize. This is proactive portfolio management at scale."*

### Business Value Points
- **Efficiency**: From manual review to automated triage
- **Prioritization**: AI scores help advisors focus on high-impact cases
- **Compliance**: Full audit trail with explainable AI
- **Scale**: Thousands of policies analyzed overnight

---

## 🎬 Closing Power Statement

> *"This isn't just alerting—it's **intelligent triage**. Our AI tells advisors **which** policies need attention, **why** they need it, and **how confident** we are in that assessment. That's the future of in-force annuity management."*

---

## ⏱️ Demo Timeline (4-5 minutes total)

| Time | Action | Key Message |
|------|--------|-------------|
| **0:00-0:30** | Problem setup | "Advisors drowning in policy reviews..." |
| **0:30-1:30** | Show algorithm documentation | "Three weighted scoring algorithms analyzing 23+ data points..." |
| **1:30-2:30** | **Run batch script LIVE** | "Watch AI analyze 23 policies in real-time..." |
| **2:30-3:30** | Open JSON, show ai_analysis fields | "Score 77, confidence 87%, here's the breakdown..." |
| **3:30-4:00** | Highlight innovation | "Multi-factor, explainable, context-aware, production-ready..." |
| **4:00-4:30** | Business impact | "31 alerts generated, 7 high-priority, ready to scale..." |
| **4:30-5:00** | Closing | "Intelligent triage for the future..." |

---

## 🎯 Key Phrases to Use

### Technical Credibility
✓ "Multi-dimensional weighted scoring algorithm"  
✓ "23+ data points per policy analysis"  
✓ "Context-aware suitability matching"  
✓ "Explainable AI with full transparency"  
✓ "Production-ready batch processing"

### Business Value
✓ "Intelligent triage at scale"  
✓ "Proactive portfolio management"  
✓ "Compliance-ready with full audit trail"  
✓ "From reactive reviews to predictive insights"  
✓ "Quantified confidence levels for prioritization"

### Demo Impact
✓ "Watch in real-time..." (run script live)  
✓ "Here's the math..." (show scoring_breakdown)  
✓ "Full transparency..." (show ai_analysis fields)  
✓ "Production-ready..." (emphasize speed/scale)  
✓ "See the scores..." (point to confidence levels)

---

## 📋 Pre-Demo Checklist

### Technical Setup
- [ ] FastAPI server running (optional for batch demo)
- [ ] Terminal ready in `API` folder
- [ ] `alerts_generated.json` backup (in case you need to regenerate)
- [ ] Documentation file open (Functional_and_Technical_Doc_Angular19_FastAPI.md)
- [ ] JSON viewer ready (or VS Code with JSON formatting)

### Files to Have Open
1. Terminal at `G:\Projects\Advance\IRIHackathon2026\API`
2. `Functional_and_Technical_Doc_Angular19_FastAPI.md` (Section 2.5)
3. `alerts_generated.json` (ready to show ai_analysis)
4. Browser with Swagger docs open (optional): http://localhost:8000/docs

### Practice Points
- [ ] Run batch script smoothly
- [ ] Navigate quickly to AI analysis in JSON
- [ ] Explain one scoring_breakdown in detail
- [ ] Emphasize the 23 data points
- [ ] Show confidence level interpretation

---

## 🎤 Q&A Preparation

### Expected Questions & Answers

**Q: "How did you train the AI?"**  
A: "We built a weighted scoring algorithm based on domain expertise from advisors and compliance requirements. The weights (40%, 30%, 20%, 10%) were calibrated using sample policy data. We also have infrastructure to integrate OpenAI for natural language explanations if needed."

**Q: "How accurate is the AI?"**  
A: "We report confidence levels with each alert. High confidence (85%+) means complete data and clear thresholds met. The scoring is deterministic and explainable—we can show exactly why each score was calculated."

**Q: "Can this scale to thousands of policies?"**  
A: "Yes—we analyzed 23 policies in under a second. The algorithm is O(n) complexity, so it scales linearly. In production, we'd run this overnight as a batch job against the full portfolio."

**Q: "What about compliance and auditability?"**  
A: "Every alert includes full transparency: AI score, confidence, scoring breakdown, data points analyzed, algorithm version, and timestamp. Complete audit trail for regulatory review."

**Q: "How do advisors use these alerts?"**  
A: "Alerts are prioritized by severity and AI score. Advisors can review the 'key_factors' for quick context, then dive into the AI Copilot for detailed explanations and documentation drafting."

**Q: "What makes this better than simple rule-based alerts?"**  
A: "Multi-dimensional analysis. A 3% cap rate gap might be critical for one client but acceptable for another based on their risk tolerance, surrender schedule, and objectives. Our AI weighs ALL these factors together, not just threshold checks."

---

## 🔧 Technical Details (If Asked)

### Technology Stack
- **Backend**: Python 3.12, FastAPI 0.109.0
- **AI/ML**: Custom weighted scoring algorithms + OpenAI integration (optional)
- **Data**: JSON-based (demo) → PostgreSQL/MongoDB (production)
- **Processing**: Batch overnight job (cron/scheduled task)

### Algorithm Details
- Replacement: 4-factor weighted (40%/30%/20%/10%)
- Income Activation: Timing optimization with break-even analysis
- Suitability Drift: 4-factor weighted (35%/30%/20%/15%)
- Confidence: Based on data completeness and threshold clarity

### Scalability
- Current: 23 policies in < 1 second
- Production estimate: 10,000 policies in ~7 minutes
- Parallelization possible for faster processing

---

## 💡 Demo Tips

### Do's
✓ Run the batch script live (shows it's real)  
✓ Point to specific numbers in the JSON  
✓ Explain ONE algorithm in detail (choose Replacement)  
✓ Emphasize explainability and transparency  
✓ Show enthusiasm about the AI scoring  

### Don'ts
✗ Don't read the JSON file—narrate what matters  
✗ Don't get lost in technical jargon  
✗ Don't skip the business value (Act 4)  
✗ Don't forget to mention compliance/audit trail  
✗ Don't undersell the innovation  

---

## 🏆 Success Metrics

**What Makes This Demo Successful:**

1. **Judges understand the algorithm** (multi-factor weighted scoring)
2. **Judges see it work live** (batch script runs successfully)
3. **Judges appreciate the transparency** (explainable AI fields)
4. **Judges recognize business value** (intelligent triage at scale)
5. **Judges ask technical questions** (shows engagement and credibility)

---

**Good luck with your demo! 🚀**

*Remember: Confidence, clarity, and showing real working code will win over the judges.*
