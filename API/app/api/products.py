"""
Products API endpoints
"""
from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
from app.models.product import Product, ProductComparison, ProductSummary
from app.services.data_store import data_store
from app.services.product_matcher import product_matcher

router = APIRouter()


@router.get("/products", response_model=List[Product])
async def get_all_products(
    product_type: Optional[str] = Query(None, description="Filter by product type (FIA, Fixed, VA)"),
    carrier: Optional[str] = Query(None, description="Filter by carrier name")
):
    """
    Get all products in the catalog.
    Optionally filter by product type or carrier.
    """
    products = data_store.get_all_products()
    
    # Apply filters
    if product_type:
        products = [p for p in products if p.productType == product_type]
    
    if carrier:
        products = [p for p in products if p.carrier.lower() == carrier.lower()]
    
    return products


@router.get("/products/{product_id}", response_model=Product)
async def get_product_detail(
    product_id: str = Path(..., description="Product ID")
):
    """
    Get detailed product information by ID.
    """
    product = data_store.get_product_by_id(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    
    return product


@router.get("/policies/{policy_id}/alternatives", response_model=ProductComparison)
async def get_policy_alternatives(
    policy_id: str = Path(..., description="Policy ID"),
    max_results: int = Query(3, ge=1, le=5, description="Maximum number of alternatives")
):
    """
    Get alternative product recommendations for a policy.
    Used in the Replacement Opportunity module.
    
    - Matches products based on policy type and client suitability
    - Prioritizes Symetra and Brighthouse products
    - Returns 2-3 top alternatives with comparison notes
    """
    # Get current policy
    policy = data_store.get_policy_by_id(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail=f"Policy {policy_id} not found")
    
    # Get client information
    client = data_store.get_client(policy.clientAccountNumber)
    if not client:
        raise HTTPException(
            status_code=404, 
            detail=f"Client {policy.clientAccountNumber} not found"
        )
    
    # Find alternatives using product matcher
    comparison = product_matcher.create_comparison(
        policy=policy,
        client=client,
        max_alternatives=max_results
    )
    
    return comparison


@router.get("/products/carrier/{carrier_name}", response_model=List[Product])
async def get_products_by_carrier(
    carrier_name: str = Path(..., description="Carrier name (e.g., 'Symetra', 'Brighthouse Financial')")
):
    """
    Get all products from a specific carrier.
    Useful for showcasing Symetra or Brighthouse products.
    """
    products = data_store.get_products_by_carrier(carrier_name)
    
    if not products:
        raise HTTPException(
            status_code=404,
            detail=f"No products found for carrier '{carrier_name}'"
        )
    
    return products
