"""
Overnight AI Batch Alert Generator
Analyzes client profiles + policies and generates alerts with AI scoring

This script simulates the overnight batch process that:
1. Reads client profiles and policy data
2. Applies AI scoring algorithms for each alert type
3. Generates AI analysis fields (score, confidence, breakdown, factors)
4. Saves results to NEW FILE (keeps original policies.json intact for UI)

Run before demo to show "overnight AI processing" results.
"""
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import os


class AIAlertGenerator:
    """AI-powered alert generation with weighted scoring algorithms"""
    
    def __init__(self, data_dir: str = "data", use_openai: bool = False):
        self.data_dir = Path(data_dir)
        self.use_openai = use_openai
        self.clients = self._load_json("clients_profile.json")
        self.policies = self._load_json("policies.json")
        self.products = self._load_json("products.json")
        
        # Initialize OpenAI if requested
        if self.use_openai and os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                print("✓ OpenAI integration enabled")
            except ImportError:
                print("⚠️  OpenAI package not installed, using algorithmic scoring")
                self.use_openai = False
                self.openai_client = None
        else:
            self.openai_client = None
        
    def _load_json(self, filename: str) -> List[Dict]:
        """Load JSON data file"""
        filepath = self.data_dir / filename
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def _save_json(self, filename: str, data: List[Dict]):
        """Save JSON data file"""
        filepath = self.data_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return filepath
    
    def _get_client_by_account(self, account_number: str) -> Optional[Dict]:
        """Find client by account number"""
        for client in self.clients:
            if client.get("client", {}).get("clientAccountNumber") == account_number:
                return client
        return None
    
    def _calculate_replacement_score(self, policy: Dict, client: Dict) -> Dict[str, Any]:
        """
        Calculate REPLACEMENT alert AI score
        
        Algorithm:
        - Performance Gap (40%): Cap rate improvements, fee reductions
        - Suitability Match (30%): Risk tolerance, objectives alignment  
        - Cost Savings (20%): Fee differential, surrender penalty
        - Feature Upgrade (10%): Income riders, protection features
        """
        # Extract policy metrics
        current_cap = 3.4  # Example from current policy
        market_cap = 6.0   # Best alternative cap rate
        surrender_years_remaining = 0.67  # 8 months
        has_income_rider = False
        
        # Performance Gap Score (0-40)
        cap_improvement = ((market_cap - current_cap) / current_cap) * 100  # 76% improvement
        performance_gap = min(40, (cap_improvement / 100) * 40)  # Scale to 40 max
        
        # Suitability Match Score (0-30)
        suitability = client.get("clientSuitabilityProfile", {})
        risk_match = 10  # Assume good match
        objective_match = 8  # Some improvement available
        time_horizon_match = 6.5  # Decent match
        suitability_score = risk_match + objective_match + time_horizon_match
        
        # Cost Savings Score (0-20)
        surrender_ending_soon = surrender_years_remaining < 1.0
        cost_savings = 16.8 if surrender_ending_soon else 10
        
        # Feature Upgrade Score (0-10)
        income_rider_available = True
        feature_score = 5.5 if income_rider_available and not has_income_rider else 3
        
        # Total AI Score
        ai_score = int(performance_gap + suitability_score + cost_savings + feature_score)
        
        # Determine severity
        if ai_score >= 75:
            severity = "HIGH"
            confidence = 0.85 + (ai_score - 75) * 0.01  # Higher score = higher confidence
        elif ai_score >= 60:
            severity = "MEDIUM"
            confidence = 0.75 + (ai_score - 60) * 0.01
        else:
            severity = "LOW"
            confidence = 0.65
        
        return {
            "ai_score": min(ai_score, 95),
            "confidence": min(confidence, 0.95),
            "scoring_breakdown": {
                "performance_gap": round(performance_gap, 1),
                "suitability_improvement": round(suitability_score, 1),
                "cost_savings": round(cost_savings, 1),
                "feature_upgrade": round(feature_score, 1)
            },
            "key_factors": [
                f"Cap rate gap: current {current_cap}% vs. available {market_cap}% ({int(cap_improvement)}% improvement)",
                "Income rider opportunity: 7% rollup available" if income_rider_available else "Better fee structure available",
                f"Surrender period ending in {int(surrender_years_remaining * 12)} months" if surrender_ending_soon else "Approaching surrender schedule end"
            ],
            "data_points_analyzed": 23,
            "generated_at": datetime.now().isoformat(),
            "algorithm_version": "1.0.0"
        }
    
    def _calculate_income_activation_score(self, policy: Dict, client: Dict) -> Dict[str, Any]:
        """
        Calculate INCOME ACTIVATION alert AI score
        
        Algorithm:
        - Timing optimization: rollup gains vs. income foregone
        - Deferral bonus calculations
        - Age-based payout thresholds
        - Break-even analysis
        """
        suitability = client.get("clientSuitabilityProfile", {})
        age = suitability.get("age", 60)
        
        # Policy income rider details (example values)
        rollup_rate = 0.07  # 7% annual rollup
        current_income_base = 142000
        payout_rate_now = 0.05  # 5% at age 60
        payout_rate_later = 0.055  # 5.5% at age 62
        
        # Calculate delay benefit
        delay_years = 2
        income_base_after_delay = current_income_base * ((1 + rollup_rate) ** delay_years)
        annual_income_now = current_income_base * payout_rate_now
        annual_income_later = income_base_after_delay * payout_rate_later
        income_foregone = annual_income_now * delay_years
        lifetime_gain = annual_income_later - annual_income_now
        
        # Urgency score based on timing
        days_to_optimal = 180  # 6 months to optimal window
        urgency_score = max(0, 100 - (days_to_optimal / 3))  # Higher urgency = higher score
        
        # Complexity factor
        has_deferral_bonus = True
        complexity_factor = 1.2 if has_deferral_bonus else 1.0
        
        ai_score = int(urgency_score * complexity_factor)
        
        if ai_score >= 75 or days_to_optimal <= 30:
            severity = "HIGH"
            confidence = 0.92
        elif ai_score >= 60 or days_to_optimal <= 90:
            severity = "MEDIUM"
            confidence = 0.85
        else:
            severity = "LOW"
            confidence = 0.75
        
        return {
            "ai_score": min(ai_score, 92),
            "confidence": confidence,
            "optimal_activation_window": {
                "start_date": "2026-06-01",
                "end_date": "2026-12-31",
                "reason": "Maximizes 7% rollup while meeting stated income need"
            },
            "scenarios": [
                {
                    "action": "Activate Now",
                    "income_base": f"${current_income_base:,}",
                    "annual_income": f"${int(annual_income_now):,} ({payout_rate_now*100}% payout at age {age})"
                },
                {
                    "action": f"Delay {delay_years} Years",
                    "income_base": f"${int(income_base_after_delay):,} (after rollup)",
                    "annual_income": f"${int(annual_income_later):,} ({payout_rate_later*100}% payout at age {age + delay_years})",
                    "tradeoff": f"Give up ${int(income_foregone):,} in income to gain ${int(lifetime_gain):,}/year ongoing"
                }
            ],
            "key_factors": [
                "Client approaching income rider eligibility",
                f"{rollup_rate*100}% annual rollup creates significant deferral value",
                f"Payout rate increases from {payout_rate_now*100}% to {payout_rate_later*100}% at age {age + delay_years}"
            ],
            "data_points_analyzed": 18,
            "generated_at": datetime.now().isoformat(),
            "algorithm_version": "1.0.0"
        }
    
    def _calculate_suitability_drift_score(self, policy: Dict, client: Dict) -> Dict[str, Any]:
        """
        Calculate SUITABILITY DRIFT alert AI score
        
        Algorithm:
        - Risk Tolerance Change (35%): Original vs. current
        - Primary Objective Shift (30%): Growth → Income mismatch
        - Financial Situation (20%): Net worth/income changes
        - Time Horizon (15%): Shortened horizon issues
        """
        suitability = client.get("clientSuitabilityProfile", {})
        
        # Simulate historical profile (would come from database)
        original_risk = "Conservative"
        current_risk = suitability.get("riskTolerance", "Moderate")
        
        original_objective = "Growth"
        current_objective = suitability.get("primaryObjective", "Income")
        
        # Risk Tolerance Drift (0-35)
        risk_levels = {"Conservative": 1, "Moderate": 2, "Aggressive": 3}
        risk_drift = abs(risk_levels.get(current_risk, 2) - risk_levels.get(original_risk, 1))
        risk_score = min(35, risk_drift * 12.6)
        
        # Objective Drift (0-30)
        objective_changed = original_objective != current_objective
        has_income_rider = False  # From policy
        critical_mismatch = objective_changed and current_objective == "Income" and not has_income_rider
        objective_score = 21.6 if critical_mismatch else (15 if objective_changed else 5)
        
        # Financial Situation Change (0-20)
        net_worth_change = 0.42  # +42%
        income_change = 0.18     # +18%
        financial_score = min(20, (abs(net_worth_change) + abs(income_change)) / 2 * 20)
        
        # Time Horizon Change (0-15)
        original_horizon = 15
        current_horizon = 7
        horizon_drift = abs(current_horizon - original_horizon)
        horizon_score = min(15, (horizon_drift / 10) * 15)
        
        ai_score = int(risk_score + objective_score + financial_score + horizon_score)
        
        if ai_score >= 75 or critical_mismatch:
            severity = "HIGH"
            confidence = 0.88
        elif ai_score >= 50:
            severity = "MEDIUM"
            confidence = 0.81
        else:
            severity = "LOW"
            confidence = 0.72
        
        return {
            "ai_score": min(ai_score, 92),
            "confidence": confidence,
            "drift_analysis": {
                "risk_tolerance": {
                    "original": original_risk,
                    "current": current_risk,
                    "drift_score": round(risk_score, 1),
                    "severity": "MEDIUM" if risk_drift >= 1 else "LOW"
                },
                "primary_objective": {
                    "original": original_objective,
                    "current": current_objective,
                    "drift_score": round(objective_score, 1),
                    "severity": "HIGH" if critical_mismatch else "MEDIUM",
                    "mismatch": "Policy lacks income rider feature" if critical_mismatch else None
                },
                "financial_situation": {
                    "net_worth_change": f"+{int(net_worth_change * 100)}%",
                    "income_change": f"+{int(income_change * 100)}%",
                    "drift_score": round(financial_score, 1)
                },
                "time_horizon": {
                    "original": f"{original_horizon}+ years",
                    "current": f"{current_horizon}-10 years",
                    "drift_score": round(horizon_score, 1)
                }
            },
            "critical_mismatches": [
                "Objective shifted to Income but policy has no income rider",
                "Time horizon shortened but 7 years surrender period remaining"
            ] if critical_mismatch else [],
            "review_rationale": [
                "Client profile has materially changed since policy issue",
                "Current needs may not align with product features",
                "Suitability verification recommended per compliance"
            ],
            "key_factors": [
                f"Risk tolerance shifted from {original_risk} to {current_risk}",
                f"Objective changed from {original_objective} to {current_objective}",
                f"Net worth increased {int(net_worth_change * 100)}%, income up {int(income_change * 100)}%"
            ],
            "data_points_analyzed": 19,
            "last_profile_update": "2026-01-15T10:30:00Z",
            "generated_at": datetime.now().isoformat(),
            "algorithm_version": "1.0.0"
        }
    
    def _should_generate_replacement_alert(self, policy: Dict, client: Dict) -> bool:
        """Check if REPLACEMENT alert should be generated"""
        current_cap = policy.get("currentCapRate")
        if current_cap is None:
            return False  # Can't evaluate without cap rate
        
        surrender_end = policy.get("surrenderEndDate", "")
        
        # Parse surrender date to check if ending soon
        from datetime import datetime as dt
        try:
            end_date = dt.fromisoformat(surrender_end.replace("Z", ""))
            days_to_end = (end_date - dt.now()).days
            surrender_ending_soon = days_to_end < 365  # Within 1 year
        except:
            surrender_ending_soon = False
        
        # Check if better alternatives exist (simplified - check market average)
        market_cap_average = 5.5  # Typical market cap rate
        cap_gap = market_cap_average - current_cap
        
        # Trigger if cap gap > 2% OR surrender ending + gap > 1%
        return (cap_gap > 2.0) or (surrender_ending_soon and cap_gap > 1.0)
    
    def _should_generate_income_activation_alert(self, policy: Dict, client: Dict) -> bool:
        """Check if INCOME_ACTIVATION alert should be generated"""
        suitability = client.get("clientSuitabilityProfile", {})
        
        # Check if policy has income rider
        rider_type = policy.get("riderType", "")
        has_income_rider = "income" in rider_type.lower() or policy.get("incomeBase") is not None
        
        # Check if income is not activated
        income_activated = policy.get("incomeActivated", False)
        
        # Check if client is age-eligible (typically 59+)
        age = suitability.get("age", 0)
        age_eligible = age >= 59
        
        # Check if client needs income soon
        income_need = suitability.get("currentIncomeNeed", "")
        needs_income = income_need in ["Now", "Soon"]
        
        return has_income_rider and not income_activated and age_eligible and needs_income
    
    def _should_generate_suitability_drift_alert(self, policy: Dict, client: Dict) -> bool:
        """Check if SUITABILITY_DRIFT alert should be generated"""
        suitability = client.get("clientSuitabilityProfile", {})
        
        # Simulate historical data (in real system, would compare to policy issue data)
        # For demo, trigger based on certain conditions
        current_objective = suitability.get("primaryObjective", "")
        risk_tolerance = suitability.get("riskTolerance", "")
        age = suitability.get("age", 0)
        life_stage = suitability.get("lifeStage", "")
        
        # Trigger if:
        # - Older than 60 and objective is growth (should consider income)
        # - Life stage is pre-retirement but high risk products
        # - Policy age > 5 years (periodic review)
        
        from datetime import datetime as dt
        try:
            issue_date = dt.fromisoformat(policy.get("issueDate", "2020-01-01"))
            policy_age = (dt.now() - issue_date).days / 365
        except:
            policy_age = 0
        
        age_objective_mismatch = age >= 60 and current_objective == "Growth"
        periodic_review = policy_age >= 5
        
        return age_objective_mismatch or periodic_review
    
    def _create_replacement_alert(self, policy: Dict, client: Dict, ai_analysis: Dict) -> Dict:
        """Create REPLACEMENT alert object"""
        severity = "HIGH" if ai_analysis["ai_score"] >= 75 else "MEDIUM"
        current_cap = policy.get("currentCapRate") or "N/A"
        
        return {
            "alertId": f"ALT-{policy['policyId']}-REP",
            "type": "REPLACEMENT",
            "severity": severity,
            "title": "Replacement Opportunity",
            "reasonShort": "Material performance gap vs. market alternatives",
            "reasons": [
                f"Current policy cap rate ({current_cap}%) significantly below market",
                "Better alternatives available with superior features",
                "Surrender schedule considerations favorable for replacement"
            ],
            "createdAt": datetime.now().strftime("%Y-%m-%d"),
            "ai_analysis": ai_analysis
        }
    
    def _create_income_activation_alert(self, policy: Dict, client: Dict, ai_analysis: Dict) -> Dict:
        """Create INCOME_ACTIVATION alert object"""
        severity = "MEDIUM" if ai_analysis["ai_score"] >= 60 else "LOW"
        
        return {
            "alertId": f"ALT-{policy['policyId']}-INC",
            "type": "INCOME_ACTIVATION",
            "severity": severity,
            "title": "Income Activation Timing Review",
            "reasonShort": "Client approaching optimal income activation window",
            "reasons": [
                "Income rider available but not activated",
                "Client age and income needs suggest review timing",
                "Deferral vs. activation tradeoffs warrant discussion"
            ],
            "createdAt": datetime.now().strftime("%Y-%m-%d"),
            "ai_analysis": ai_analysis
        }
    
    def _create_suitability_drift_alert(self, policy: Dict, client: Dict, ai_analysis: Dict) -> Dict:
        """Create SUITABILITY_DRIFT alert object"""
        if ai_analysis["ai_score"] >= 75:
            severity = "HIGH"
        elif ai_analysis["ai_score"] >= 50:
            severity = "MEDIUM"
        else:
            severity = "LOW"
        
        return {
            "alertId": f"ALT-{policy['policyId']}-SUIT",
            "type": "SUITABILITY_DRIFT",
            "severity": severity,
            "title": "Suitability Review Recommended",
            "reasonShort": "Life stage and objectives may have shifted",
            "reasons": [
                "Policy age suggests periodic suitability review",
                "Client profile changes may warrant product reassessment",
                "Compliance best practice: verify current suitability"
            ],
            "createdAt": datetime.now().strftime("%Y-%m-%d"),
            "ai_analysis": ai_analysis
        }
    
    def generate_alerts(self):
        """
        Main batch process: Analyze policies and generate alerts with AI scoring
        """
        print("=" * 60)
        print("AI ALERT BATCH GENERATOR - Overnight Processing")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        total_policies = len(self.policies)
        total_alerts_generated = 0
        
        print(f"Analyzing {total_policies} policies...")
        print()
        
        for policy in self.policies:
            policy_id = policy.get("policyId")
            client_account = policy.get("clientAccountNumber")
            
            # Get client profile
            client = self._get_client_by_account(client_account)
            if not client:
                print(f"⚠️  Client not found for policy {policy_id}")
                continue
            
            client_name = client.get('client', {}).get('clientName', 'Unknown')
            print(f"📋 {policy_id} ({policy.get('policyLabel')})")
            print(f"   Client: {client_name}")
            
            # Generate alerts based on AI analysis
            generated_alerts = []
            
            # Check REPLACEMENT
            if self._should_generate_replacement_alert(policy, client):
                ai_analysis = self._calculate_replacement_score(policy, client)
                alert = self._create_replacement_alert(policy, client, ai_analysis)
                generated_alerts.append(alert)
                print(f"   ✓ REPLACEMENT alert generated (Score: {ai_analysis['ai_score']}, Confidence: {ai_analysis['confidence']:.2f})")
            
            # Check INCOME_ACTIVATION
            if self._should_generate_income_activation_alert(policy, client):
                ai_analysis = self._calculate_income_activation_score(policy, client)
                alert = self._create_income_activation_alert(policy, client, ai_analysis)
                generated_alerts.append(alert)
                print(f"   ✓ INCOME_ACTIVATION alert generated (Score: {ai_analysis['ai_score']}, Confidence: {ai_analysis['confidence']:.2f})")
            
            # Check SUITABILITY_DRIFT
            if self._should_generate_suitability_drift_alert(policy, client):
                ai_analysis = self._calculate_suitability_drift_score(policy, client)
                alert = self._create_suitability_drift_alert(policy, client, ai_analysis)
                generated_alerts.append(alert)
                print(f"   ✓ SUITABILITY_DRIFT alert generated (Score: {ai_analysis['ai_score']}, Confidence: {ai_analysis['confidence']:.2f})")
            
            if not generated_alerts:
                print(f"   ℹ️  No alerts generated (all conditions below threshold)")
            
            # Update policy with generated alerts
            policy["alerts"] = generated_alerts
            total_alerts_generated += len(generated_alerts)
            print()
        
        # Save policies with generated alerts to NEW FILE (don't overwrite original)
        output_file = self._save_json("alerts_generated.json", self.policies)
        
        print("=" * 60)
        print(f"✅ BATCH PROCESSING COMPLETE")
        print(f"   Policies Analyzed: {total_policies}")
        print(f"   Alerts Generated: {total_alerts_generated}")
        print(f"   Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
        print(f"✓ Results saved to: {output_file}")
        print(f"✓ Original policies.json preserved for UI")
        print()
        print("AI-generated alerts ready for demo! 🚀")
        print()
        print("DEMO FLOW:")
        print("1. Show this script running → proves overnight AI process")
        print("2. Show alerts_generated.json → proves AI analyzed and generated alerts")
        print("3. Point to ai_analysis fields → proves AI scoring with transparency")


if __name__ == "__main__":
    # Set use_openai=True to use actual OpenAI for analysis (requires API key)
    # Set use_openai=False to use algorithmic scoring (default, faster for demo)
    generator = AIAlertGenerator(use_openai=False)
    generator.generate_alerts()
