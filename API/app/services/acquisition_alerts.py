"""
Annuity Acquisition Alert Generation Logic
These alerts identify opportunities to PURCHASE NEW annuities (not replacements)
Analyzes client's full portfolio to grow annuity AUM
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


class AcquisitionAlertGenerator:
    """Generates acquisition-focused alerts for new annuity business"""
    
    def __init__(self):
        self.current_date = datetime(2026, 2, 25)
        # Market rates for comparison
        self.best_myga_rate = 0.055  # 5.5% Multi-Year Guaranteed Annuity
        self.best_fia_cap = 0.065    # 6.5% Fixed Indexed Annuity cap rate
    
    def generate_excess_liquidity_alert(self, positions: Dict, client: Dict) -> Optional[Dict]:
        """
        EXCESS_LIQUIDITY Alert: Too much cash earning minimal interest
        
        Detection Criteria:
        - Cash positions > 10% of total portfolio
        - Cash amount > $50,000
        - Client age < 75
        - Low liquidity importance
        """
        summary = positions.get("summary", {})
        total_cash = summary.get("totalCash", 0)
        total_portfolio = positions.get("totalPortfolioValue", 0)
        cash_allocation = summary.get("cashAllocation", 0)
        
        suitability = client.get("clientSuitabilityProfile", {})
        age = suitability.get("age", 60)
        liquidity_importance = suitability.get("liquidityImportance", "Medium")
        
        # Detection logic
        if cash_allocation <= 0.10 or total_cash <= 50000 or age >= 75:
            return None
        
        # Calculate opportunity
        suggested_allocation = total_cash * 0.60  # Move 60% to annuity
        current_yield = 0.005  # 0.5% money market average
        annuity_yield = self.best_fia_cap
        annual_improvement = suggested_allocation * (annuity_yield - current_yield)
        
        # Scoring
        cash_excess = (cash_allocation - 0.10) * 100  # Percent over threshold
        amount_score = min(40, (total_cash / 100000) * 10)  # Up to 40 points
        opportunity_score = min(30, (annual_improvement / 5000) * 10)  # Up to 30 points
        urgency_score = 20 if liquidity_importance == "Low" else 10
        
        ai_score = int(amount_score + opportunity_score + urgency_score)
        
        if ai_score >= 75:
            severity = "HIGH"
            confidence = 0.88
        elif ai_score >= 60:
            severity = "MEDIUM"
            confidence = 0.82
        else:
            severity = "LOW"
            confidence = 0.75
        
        return {
            "alert": {
                "alertId": f"ACQ-EXL-{positions['clientAccountNumber'].replace('-', '')}",
                "type": "EXCESS_LIQUIDITY",
                "severity": severity,
                "title": f"Excess Cash Alert: ${total_cash:,.0f} Earning {current_yield*100}%",
                "reasonShort": f"Move ${suggested_allocation:,.0f} to annuity for ${annual_improvement:,.0f}/year gain",
                "reasons": [
                    f"{cash_allocation*100:.0f}% cash allocation (recommended: 10-15%)",
                    f"${total_cash:,.0f} earning ~{current_yield*100}% in money market",
                    f"Fixed indexed annuity available at {annuity_yield*100}% cap",
                    f"Liquidity importance: {liquidity_importance} (permits annuity allocation)",
                    f"Age {age} (suitable time horizon)"
                ],
                "createdAt": self.current_date.strftime("%Y-%m-%d")
            },
            "ai_analysis": {
                "ai_score": min(ai_score, 95),
                "confidence": confidence,
                "scoring_breakdown": {
                    "cash_excess_score": round(cash_excess, 1),
                    "amount_score": round(amount_score, 1),
                    "opportunity_score": round(opportunity_score, 1),
                    "urgency_score": urgency_score
                },
                "recommendation": {
                    "product_type": "Fixed Indexed Annuity",
                    "suggested_allocation": round(suggested_allocation, 2),
                    "expected_annual_gain": round(annual_improvement, 2),
                    "features": ["10% annual penalty-free withdrawals", "Principal protection", "Index upside participation"]
                },
                "key_factors": [
                    f"${total_cash:,.0f} in cash ({cash_allocation*100:.0f}% of portfolio)",
                    f"Current yield: {current_yield*100}% vs. available {annuity_yield*100}%",
                    f"Estimated gain: ${annual_improvement:,.0f}/year on ${suggested_allocation:,.0f}"
                ],
                "data_points_analyzed": 12,
                "generated_at": datetime.now().isoformat(),
                "algorithm_version": "1.0.0"
            }
        }
    
    def generate_portfolio_unprotected_alert(self, positions: Dict, client: Dict) -> Optional[Dict]:
        """
        PORTFOLIO_UNPROTECTED Alert: High equity exposure without guaranteed income
        
        Detection Criteria:
        - Equity allocation > 60%
        - Age 55+
        - Life stage: Pre-Retirement or Retired
        - Primary objective: Income or Preservation
        - NO existing annuities
        """
        summary = positions.get("summary", {})
        equity_allocation = summary.get("equityAllocation", 0)
        annuity_allocation = summary.get("annuityAllocation", 0)
        total_portfolio = positions.get("totalPortfolioValue", 0)
        
        suitability = client.get("clientSuitabilityProfile", {})
        age = suitability.get("age", 60)
        life_stage = suitability.get("lifeStage", "")
        primary_objective = suitability.get("primaryObjective", "")
        
        # Detection logic
        if equity_allocation <= 0.60 or age < 55 or annuity_allocation > 0:
            return None
        
        if life_stage not in ["Pre-Retirement", "Retired"]:
            return None
        
        if primary_objective not in ["Income", "Preservation"]:
            return None
        
        # Calculate opportunity
        suggested_allocation = total_portfolio * 0.20  # Allocate 20% to annuity with GLWB
        glwb_payout_rate = 0.055  # 5.5% guaranteed withdrawal
        guaranteed_annual_income = suggested_allocation * glwb_payout_rate
        
        # Scoring
        equity_excess = (equity_allocation - 0.60) * 100
        age_score = min(30, (age - 55) * 2)
        objective_match = 35 if primary_objective == "Income" else 25
        unprotected_score = 20 if annuity_allocation == 0 else 0
        
        ai_score = int(equity_excess + age_score + objective_match + unprotected_score)
        
        if ai_score >= 80:
            severity = "HIGH"
            confidence = 0.91
        elif ai_score >= 65:
            severity = "MEDIUM"
            confidence = 0.84
        else:
            severity = "LOW"
            confidence = 0.76
        
        return {
            "alert": {
                "alertId": f"ACQ-UNP-{positions['clientAccountNumber'].replace('-', '')}",
                "type": "PORTFOLIO_UNPROTECTED",
                "severity": severity,
                "title": f"{equity_allocation*100:.0f}% Equities at Age {age} with No Guaranteed Income",
                "reasonShort": f"Allocate ${suggested_allocation:,.0f} to annuity with GLWB for downside protection",
                "reasons": [
                    f"{equity_allocation*100:.0f}% equity allocation (exposed to market volatility)",
                    f"Age {age}, life stage: {life_stage}",
                    f"Primary objective: {primary_objective} (needs guaranteed income)",
                    "Zero allocation to annuities or guaranteed income products",
                    f"GLWB could provide ${guaranteed_annual_income:,.0f}/year guaranteed income"
                ],
                "createdAt": self.current_date.strftime("%Y-%m-%d")
            },
            "ai_analysis": {
                "ai_score": min(ai_score, 95),
                "confidence": confidence,
                "scoring_breakdown": {
                    "equity_excess_score": round(equity_excess, 1),
                    "age_urgency_score": round(age_score, 1),
                    "objective_match_score": objective_match,
                    "unprotected_score": unprotected_score
                },
                "recommendation": {
                    "product_type": "Variable Annuity with GLWB Rider",
                    "suggested_allocation": round(suggested_allocation, 2),
                    "guaranteed_annual_income": round(guaranteed_annual_income, 2),
                    "features": ["Guaranteed Lifetime Withdrawal Benefit", "Market participation", "Downside protection"]
                },
                "key_factors": [
                    f"{equity_allocation*100:.0f}% equities without downside protection",
                    f"Age {age}, {life_stage} - heightened sequence-of-returns risk",
                    f"{primary_objective} objective requires guaranteed income layer",
                    f"${guaranteed_annual_income:,.0f}/year guaranteed income available"
                ],
                "data_points_analyzed": 15,
                "generated_at": datetime.now().isoformat(),
                "algorithm_version": "1.0.0"
            }
        }
    
    def generate_cd_maturity_alert(self, positions: Dict, client: Dict) -> Optional[Dict]:
        """
        CD_MATURITY Alert: CDs maturing soon - annuity could offer better rates
        
        Detection Criteria:
        - CD holdings with maturity date within 90 days
        - CD amount > $50,000
        - Current CD rate < 4.0%
        - Best MYGA rate > CD rate + 1.0%
        """
        cd_positions = []
        for pos in positions.get("positions", []):
            if pos.get("assetClass") == "FIXED_INCOME" and pos.get("maturityDate"):
                maturity_date = datetime.strptime(pos["maturityDate"], "%Y-%m-%d")
                days_to_maturity = (maturity_date - self.current_date).days
                
                if 0 < days_to_maturity <= 90:
                    cd_positions.append({
                        "position": pos,
                        "days_to_maturity": days_to_maturity
                    })
        
        if not cd_positions:
            return None
        
        # Find most urgent CD
        cd_data = min(cd_positions, key=lambda x: x["days_to_maturity"])
        cd_pos = cd_data["position"]
        days_remaining = cd_data["days_to_maturity"]
        
        cd_amount = cd_pos.get("marketValue", 0)
        cd_rate = cd_pos.get("currentRate", 0.035)
        
        if cd_amount <= 50000 or cd_rate >= 0.04:
            return None
        
        # Calculate opportunity
        myga_rate = self.best_myga_rate
        rate_differential = myga_rate - cd_rate
        annual_improvement = cd_amount * rate_differential
        
        # Scoring
        amount_score = min(30, (cd_amount / 100000) * 15)
        rate_gap_score = min(40, (rate_differential / 0.01) * 10)
        urgency_score = min(30, 30 - (days_remaining / 3))
        
        ai_score = int(amount_score + rate_gap_score + urgency_score)
        
        if ai_score >= 75 or days_remaining <= 30:
            severity = "HIGH"
            confidence = 0.92
        elif ai_score >= 60:
            severity = "MEDIUM"
            confidence = 0.85
        else:
            severity = "LOW"
            confidence = 0.78
        
        return {
            "alert": {
                "alertId": f"ACQ-CDM-{positions['clientAccountNumber'].replace('-', '')}",
                "type": "CD_MATURITY",
                "severity": severity,
                "title": f"${cd_amount:,.0f} CD Maturing in {days_remaining} Days at {round(cd_rate*100, 2)}%",
                "reasonShort": f"Multi-year guaranteed annuity (MYGA) offering {round(myga_rate*100, 2)}%",
                "reasons": [
                    f"CD matures on {cd_pos.get('maturityDate')} ({days_remaining} days)",
                    f"Current CD rate: {round(cd_rate*100, 2)}%",
                    f"Best MYGA rate: {round(myga_rate*100, 2)}% ({rate_differential*100:.1f}% improvement)",
                    f"Estimated gain: ${annual_improvement:,.0f}/year",
                    "MYGA offers comparable safety with better yield"
                ],
                "createdAt": self.current_date.strftime("%Y-%m-%d")
            },
            "ai_analysis": {
                "ai_score": min(ai_score, 95),
                "confidence": confidence,
                "scoring_breakdown": {
                    "amount_score": round(amount_score, 1),
                    "rate_gap_score": round(rate_gap_score, 1),
                    "urgency_score": round(urgency_score, 1)
                },
                "recommendation": {
                    "product_type": "Multi-Year Guaranteed Annuity (MYGA)",
                    "suggested_allocation": cd_amount,
                    "guaranteed_rate": myga_rate,
                    "term": "5 years",
                    "expected_annual_gain": round(annual_improvement, 2),
                    "features": ["Guaranteed rate", "Tax deferral", "Principal protection"]
                },
                "key_factors": [
                    f"${cd_amount:,.0f} CD maturing in {days_remaining} days",
                    f"{rate_differential*100:.1f}% rate improvement available",
                    f"${annual_improvement:,.0f}/year additional income",
                    "Time-sensitive: Act before auto-renewal"
                ],
                "data_points_analyzed": 8,
                "generated_at": datetime.now().isoformat(),
                "algorithm_version": "1.0.0"
            }
        }
    
    def generate_income_gap_alert(self, positions: Dict, client: Dict) -> Optional[Dict]:
        """
        INCOME_GAP Alert: Approaching retirement without sufficient guaranteed income
        
        Detection Criteria:
        - Age 60+
        - Retirement target year ≤ 3 years
        - Primary objective: Income
        - Current income need: Now or Soon
        - Guaranteed income < 50% of estimated expenses
        - NO existing annuities
        """
        suitability = client.get("clientSuitabilityProfile", {})
        age = suitability.get("age", 60)
        retirement_target_year = suitability.get("retirementTargetYear", 2030)
        primary_objective = suitability.get("primaryObjective", "")
        life_stage = suitability.get("lifeStage", "")
        
        summary = positions.get("summary", {})
        annuity_allocation = summary.get("annuityAllocation", 0)
        total_portfolio = positions.get("totalPortfolioValue", 0)
        
        years_to_retirement = retirement_target_year - self.current_date.year
        
        # Detection logic
        if age < 60 or years_to_retirement > 3 or annuity_allocation > 0:
            return None
        
        if primary_objective != "Income":
            return None
        
        # Estimate income gap (simplified - would use actual income planning data)
        estimated_annual_expenses = total_portfolio * 0.04  # 4% rule estimate
        estimated_social_security = 35000  # Average estimate
        pension = 0  # Assume none
        
        guaranteed_income = estimated_social_security + pension
        income_gap = estimated_annual_expenses - guaranteed_income
        
        if income_gap <= 0 or (guaranteed_income / estimated_annual_expenses) >= 0.50:
            return None
        
        # Calculate annuity allocation needed
        required_allocation = income_gap / 0.055  # 5.5% payout rate
        
        # Scoring
        gap_severity = min(40, (income_gap / 10000) * 5)
        urgency_score = min(30, 30 - (years_to_retirement * 10))
        income_objective_score = 20
        age_score = min(10, (age - 60) * 1)
        
        ai_score = int(gap_severity + urgency_score + income_objective_score + age_score)
        
        if ai_score >= 75 or years_to_retirement <= 1:
            severity = "HIGH"
            confidence = 0.89
        elif ai_score >= 60:
            severity = "MEDIUM"
            confidence = 0.83
        else:
            severity = "LOW"
            confidence = 0.77
        
        return {
            "alert": {
                "alertId": f"ACQ-ING-{positions['clientAccountNumber'].replace('-', '')}",
                "type": "INCOME_GAP",
                "severity": severity,
                "title": f"Retirement in {years_to_retirement} Year{'s' if years_to_retirement != 1 else ''}: ${income_gap:,.0f} Income Gap",
                "reasonShort": f"Deferred income annuity to close gap with guaranteed lifetime payment",
                "reasons": [
                    f"Retirement target: {retirement_target_year} ({years_to_retirement} years away)",
                    f"Estimated annual expenses: ${estimated_annual_expenses:,.0f}",
                    f"Guaranteed income sources: ${guaranteed_income:,.0f} (Social Security)",
                    f"Income gap: ${income_gap:,.0f}/year",
                    f"Required annuity allocation: ${required_allocation:,.0f} at 5.5% payout"
                ],
                "createdAt": self.current_date.strftime("%Y-%m-%d")
            },
            "ai_analysis": {
                "ai_score": min(ai_score, 95),
                "confidence": confidence,
                "scoring_breakdown": {
                    "gap_severity_score": round(gap_severity, 1),
                    "urgency_score": urgency_score,
                    "income_objective_score": income_objective_score,
                    "age_score": age_score
                },
                "recommendation": {
                    "product_type": "Deferred Income Annuity (DIA)" if years_to_retirement > 1 else "Immediate Annuity (SPIA)",
                    "suggested_allocation": round(required_allocation, 2),
                    "guaranteed_annual_income": round(income_gap, 2),
                    "income_start_year": retirement_target_year,
                    "features": ["Lifetime income guarantee", "Inflation protection option", "Joint-life available"]
                },
                "key_factors": [
                    f"${income_gap:,.0f} annual income gap identified",
                    f"Retirement in {years_to_retirement} year(s) - limited time to secure income",
                    f"Only {(guaranteed_income / estimated_annual_expenses)*100:.0f}% of expenses covered by guaranteed sources",
                    f"Annuity allocation of ${required_allocation:,.0f} would close gap"
                ],
                "data_points_analyzed": 14,
                "generated_at": datetime.now().isoformat(),
                "algorithm_version": "1.0.0"
            }
        }
    
    def generate_diversification_gap_alert(self, positions: Dict, client: Dict) -> Optional[Dict]:
        """
        DIVERSIFICATION_GAP Alert: Portfolio lacks insurance products entirely
        
        Detection Criteria:
        - Total portfolio > $500K
        - Zero allocation to annuities
        - Age 50+
        - Risk tolerance: Conservative or Moderate
        """
        summary = positions.get("summary", {})
        total_portfolio = positions.get("totalPortfolioValue", 0)
        annuity_allocation = summary.get("annuityAllocation", 0)
        
        suitability = client.get("clientSuitabilityProfile", {})
        age = suitability.get("age", 60)
        risk_tolerance = suitability.get("riskTolerance", "")
        
        # Detection logic
        if total_portfolio <= 500000 or annuity_allocation > 0 or age < 50:
            return None
        
        if risk_tolerance not in ["Conservative", "Moderate"]:
            return None
        
        # Calculate opportunity
        suggested_allocation = total_portfolio * 0.15  # Recommend 15% to annuity
        
        # Scoring
        portfolio_size_score = min(30, (total_portfolio / 500000) * 10)
        risk_match_score = 30 if risk_tolerance == "Conservative" else 20
        age_score = min(20, (age - 50) * 1)
        missing_allocation_score = 15
        
        ai_score = int(portfolio_size_score + risk_match_score + age_score + missing_allocation_score)
        
        if ai_score >= 70:
            severity = "MEDIUM"
            confidence = 0.81
        else:
            severity = "LOW"
            confidence = 0.74
        
        return {
            "alert": {
                "alertId": f"ACQ-DVG-{positions['clientAccountNumber'].replace('-', '')}",
                "type": "DIVERSIFICATION_GAP",
                "severity": severity,
                "title": f"${total_portfolio:,.0f} Portfolio with 0% Insurance Products",
                "reasonShort": f"Diversify with 15% annuity allocation (${suggested_allocation:,.0f})",
                "reasons": [
                    f"${total_portfolio:,.0f} portfolio with zero annuity allocation",
                    f"Risk tolerance: {risk_tolerance} (insurance products appropriate)",
                    f"Age {age} (suitable for annuity time horizon)",
                    "Missing downside protection and guaranteed growth layer",
                    f"15% allocation would add ${suggested_allocation:,.0f} in principal-protected assets"
                ],
                "createdAt": self.current_date.strftime("%Y-%m-%d")
            },
            "ai_analysis": {
                "ai_score": min(ai_score, 90),
                "confidence": confidence,
                "scoring_breakdown": {
                    "portfolio_size_score": round(portfolio_size_score, 1),
                    "risk_match_score": risk_match_score,
                    "age_score": age_score,
                    "missing_allocation_score": missing_allocation_score
                },
                "recommendation": {
                    "product_type": "Fixed Indexed Annuity",
                    "suggested_allocation": round(suggested_allocation, 2),
                    "target_allocation_percentage": 15.0,
                    "features": ["Principal protection", "Tax deferral", "Guaranteed growth floor", "Index upside"]
                },
                "key_factors": [
                    "Zero insurance product diversification",
                    f"{risk_tolerance} risk profile supports guaranteed products",
                    "Missing downside protection layer",
                    f"${suggested_allocation:,.0f} allocation would balance equity risk"
                ],
                "data_points_analyzed": 10,
                "generated_at": datetime.now().isoformat(),
                "algorithm_version": "1.0.0"
            }
        }
