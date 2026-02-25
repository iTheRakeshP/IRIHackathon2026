"""
Data store service - loads and manages JSON data files
"""
import json
from typing import List, Optional, Dict
from pathlib import Path
from app.config import settings
from app.models.client import ClientWithSuitability, Client
from app.models.policy import Policy
from app.models.product import Product
from app.models.alert import AlertSeverity


class DataStore:
    """Data store for managing policy and client data from JSON files"""
    
    def __init__(self):
        self._clients: List[ClientWithSuitability] = []
        self._products: List[Product] = []
        self._policies: List[Policy] = []
        self._acquisition_alerts: List[Dict] = []  # Client-level acquisition opportunities
        self._load_data()
    
    def _load_data(self):
        """Load data from JSON files"""
        # Load clients
        if settings.CLIENTS_DATA_FILE.exists():
            with open(settings.CLIENTS_DATA_FILE, 'r', encoding='utf-8') as f:
                clients_data = json.load(f)
                self._clients = [ClientWithSuitability(**client) for client in clients_data]
        
        # Load policies
        if settings.POLICIES_DATA_FILE.exists():
            with open(settings.POLICIES_DATA_FILE, 'r', encoding='utf-8') as f:
                policies_data = json.load(f)
        
        # Load products
        if settings.PRODUCTS_DATA_FILE.exists():
            with open(settings.PRODUCTS_DATA_FILE, 'r', encoding='utf-8') as f:
                products_data = json.load(f)
                self._products = [Product(**product) for product in products_data]
                self._policies = [Policy(**policy) for policy in policies_data]
        
        # Load acquisition alerts (client-level portfolio opportunities)
        acquisition_alerts_file = settings.DATA_DIR / "acquisition_alerts_generated.json"
        if acquisition_alerts_file.exists():
            with open(acquisition_alerts_file, 'r', encoding='utf-8') as f:
                self._acquisition_alerts = json.load(f)
        else:
            print("⚠️  acquisition_alerts_generated.json not found - run batch_alert_generator.py to generate")
    
    def get_all_policies(self) -> List[Policy]:
        """Get all policies"""
        return self._policies
    
    def get_policy_by_id(self, policy_id: str) -> Optional[Policy]:
        """Get a specific policy by ID"""
        for policy in self._policies:
            if policy.policyId == policy_id:
                return policy
        return None
    
    def get_policies_by_client(self, client_account_number: str) -> List[Policy]:
        """Get all policies for a specific client"""
        return [
            policy for policy in self._policies 
            if policy.clientAccountNumber == client_account_number
        ]
    
    def get_client(self, client_account_number: str) -> Optional[ClientWithSuitability]:
        """Get client information by account number"""
        for client in self._clients:
            if client.client.clientAccountNumber == client_account_number:
                return client
        return None
    
    def get_all_clients(self) -> List[ClientWithSuitability]:
        """Get all clients"""
        return self._clients
    
    def get_clients_with_policies(self) -> Dict[str, ClientWithSuitability]:
        """Get clients who have policies, indexed by account number"""
        # Get unique client account numbers from policies
        client_accounts = set(policy.clientAccountNumber for policy in self._policies)
        
        # Build dictionary of clients with policies
        clients_dict = {}
        for client in self._clients:
            if client.client.clientAccountNumber in client_accounts:
                clients_dict[client.client.clientAccountNumber] = client
        
        return clients_dict
    
    def update_client_suitability(
        self, 
        client_account_number: str, 
        updates: dict
    ) -> Optional[ClientWithSuitability]:
        """Update client suitability profile"""
        for client in self._clients:
            if client.client.clientAccountNumber == client_account_number:
                # Update the fields
                for key, value in updates.items():
                    if value is not None and hasattr(client.clientSuitabilityProfile, key):
                        setattr(client.clientSuitabilityProfile, key, value)
                return client
        return None
    
    def get_acquisition_alerts_by_client(self, client_account_number: str) -> List[Dict]:
        """Get acquisition alerts (portfolio opportunities) for a specific client"""
        for client_alerts in self._acquisition_alerts:
            if client_alerts.get("clientAccountNumber") == client_account_number:
                return client_alerts.get("alerts", [])
        return []
    
    def get_all_acquisition_alerts(self) -> List[Dict]:
        """Get all acquisition alerts across all clients"""
        return self._acquisition_alerts
    
    def update_policy(self, updated_policy: Policy) -> Optional[Policy]:
        """Update a policy in the data store"""
        for idx, policy in enumerate(self._policies):
            if policy.policyId == updated_policy.policyId:
                self._policies[idx] = updated_policy
                return updated_policy
        return None
    
    
    def get_all_products(self) -> List[Product]:
        """Get all products in catalog"""
        return self._products
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get a specific product by ID"""
        for product in self._products:
            if product.productId == product_id:
                return product
        return None
    
    def get_products_by_type(self, product_type: str) -> List[Product]:
        """Get products by type (FIA, Fixed, VA)"""
        return [p for p in self._products if p.productType == product_type]
    
    def get_products_by_carrier(self, carrier: str) -> List[Product]:
        """Get products by carrier"""
        return [p for p in self._products if p.carrier.lower() == carrier.lower()]
    def count_alerts_by_severity(self, policies: List[Policy]) -> Dict[str, int]:
        """Count alerts by severity across a list of policies"""
        counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for policy in policies:
            for alert in policy.alerts:
                counts[alert.severity.value] += 1
        return counts


# Singleton instance
data_store = DataStore()
