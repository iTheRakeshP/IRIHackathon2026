"""
Product matching service - finds suitable alternative products
"""
from typing import List, Optional
from app.models.policy import Policy
from app.models.client import ClientWithSuitability
from app.models.product import Product, ProductComparison
from app.services.data_store import data_store


class ProductMatcher:
    """Service to match products to policies and client profiles"""
    
    # Priority carriers for hackathon demo
    PRIORITY_CARRIERS = ["Symetra", "Brighthouse Financial"]
    
    def find_alternatives(
        self,
        current_policy: Policy,
        client: ClientWithSuitability,
        max_results: int = 3
    ) -> List[Product]:
        """
        Find alternative products that match the current policy and client profile.
        Prioritizes Symetra and Brighthouse products.
        """
        all_products = data_store.get_all_products()
        
        # Filter by product type
        candidates = [
            p for p in all_products 
            if p.productType == current_policy.productType
        ]
        
        # Score products based on suitability
        scored_products = []
        for product in candidates:
            score = self._score_product(product, current_policy, client)
            scored_products.append((score, product))
        
        # Sort by score (descending)
        scored_products.sort(key=lambda x: x[0], reverse=True)
        
        # Return top results
        return [product for score, product in scored_products[:max_results]]
    
    def _score_product(
        self,
        product: Product,
        current_policy: Policy,
        client: ClientWithSuitability
    ) -> float:
        """
        Score a product for suitability.
        Higher score = better match.
        """
        score = 0.0
        
        # Boost for priority carriers (Symetra, Brighthouse)
        if product.carrier in self.PRIORITY_CARRIERS:
            score += 50.0
        
        # Boost for new products
        if product.isNewProduct:
            score += 10.0
        
        # Match client objectives
        client_objective = client.clientSuitabilityProfile.primaryObjective
        if client_objective in product.suitableFor:
            score += 30.0
        
        # Match risk profile
        if product.riskProfile == client.clientSuitabilityProfile.riskTolerance:
            score += 20.0
        
        # Compare performance metrics
        if current_policy.productType == "FIA" and product.indexOptions:
            # Get highest cap rate
            current_cap = current_policy.renewalCapRate or current_policy.currentCapRate or 0
            product_caps = [opt.currentValue for opt in product.indexOptions if opt.strategy.endswith("Cap")]
            if product_caps:
                max_cap = max(product_caps)
                if max_cap > current_cap:
                    score += (max_cap - current_cap) * 5  # Reward higher caps
        
        elif current_policy.productType == "Fixed":
            current_rate = current_policy.renewalCapRate or current_policy.currentCapRate or 0
            if product.currentFixedRate and product.currentFixedRate > current_rate:
                score += (product.currentFixedRate - current_rate) * 10
        
        # Prefer shorter surrender schedules
        if product.surrenderSchedule.years < current_policy.surrenderScheduleYears:
            score += 15.0
        
        # Reward premium bonus
        if product.bonusRate:
            score += product.bonusRate * 2
        
        # Check state availability
        if current_policy.applicationState in product.availableStates:
            score += 10.0
        
        # Account value consideration - ensure within min/max
        if (client.clientSuitabilityProfile.liquidNetWorthRange and 
            current_policy.accountValue >= product.minimumPremium):
            if product.maximumPremium is None or current_policy.accountValue <= product.maximumPremium:
                score += 5.0
        
        # Age suitability
        client_age = client.clientSuitabilityProfile.age
        if product.ageMin <= client_age <= product.ageMax:
            score += 5.0
        
        return score
    
    def create_comparison(
        self,
        policy: Policy,
        client: ClientWithSuitability,
        max_alternatives: int = 3
    ) -> ProductComparison:
        """
        Create a product comparison for the replacement module.
        Returns current policy info and top alternative products.
        """
        alternatives = self.find_alternatives(policy, client, max_alternatives)
        
        # Build current policy summary
        current_policy_summary = {
            "policyId": policy.policyId,
            "policyLabel": policy.policyLabel,
            "carrier": policy.carrier,
            "productType": policy.productType,
            "accountValue": policy.accountValue,
            "currentCapRate": policy.currentCapRate,
            "renewalCapRate": policy.renewalCapRate,
            "surrenderEndDate": policy.surrenderEndDate,
            "fees": {
                "m_e_fee": policy.fees.m_e_fee,
                "riderFee": policy.fees.riderFee
            }
        }
        
        # Build comparison notes
        comparison_notes = self._generate_comparison_notes(
            policy, alternatives, client
        )
        
        return ProductComparison(
            currentPolicy=current_policy_summary,
            alternatives=alternatives,
            comparisonNotes=comparison_notes
        )
    
    def _generate_comparison_notes(
        self,
        current_policy: Policy,
        alternatives: List[Product],
        client: ClientWithSuitability
    ) -> List[str]:
        """Generate key comparison points"""
        notes = []
        
        if not alternatives:
            return ["No suitable alternatives found at this time."]
        
        # Note prioritization of partner carriers
        partner_count = sum(1 for p in alternatives if p.carrier in self.PRIORITY_CARRIERS)
        if partner_count > 0:
            notes.append(
                f"Showing {partner_count} products from preferred carriers "
                f"(Symetra, Brighthouse Financial)"
            )
        
        # Performance comparison
        if current_policy.productType == "FIA":
            current_cap = current_policy.renewalCapRate or current_policy.currentCapRate or 0
            for alt in alternatives:
                caps = [opt.currentValue for opt in alt.indexOptions if opt.strategy.endswith("Cap")]
                if caps:
                    max_cap = max(caps)
                    if max_cap > current_cap:
                        notes.append(
                            f"{alt.carrier} {alt.productName} offers up to {max_cap}% cap "
                            f"vs. current {current_cap}%"
                        )
        
        # Surrender schedule
        for alt in alternatives:
            if alt.surrenderSchedule.years < current_policy.surrenderScheduleYears:
                notes.append(
                    f"{alt.productName} has shorter {alt.surrenderSchedule.years}-year "
                    f"surrender period"
                )
        
        # Special features
        for alt in alternatives:
            if alt.bonusRate:
                notes.append(
                    f"{alt.productName} includes {alt.bonusRate}% premium bonus"
                )
            
            if len(alt.competitiveAdvantages) > 0:
                notes.append(
                    f"{alt.productName}: {alt.competitiveAdvantages[0]}"
                )
        
        return notes[:5]  # Limit to 5 key points


# Singleton instance
product_matcher = ProductMatcher()
