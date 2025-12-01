

def serialize_tier(tier):

    return {
        'id': tier.id,
        'subscription_id': tier.subscription_id,
        'min_calls': tier.min_calls,
        'max_calls': tier.max_calls,
        'start_date': tier.start_date,
        'end_date': tier.end_date,
        'base_price': tier.base_price,
        'price_per_tier': tier.price_per_tier,
        'is_archived': tier.is_archived,
        'created_at': tier.created_at,
        'updated_at': tier.updated_at,
        'created_by': tier.created_by,
        'updated_by': tier.updated_by
    }



def serialize_product(product):
    return {
        'id': product.id,
        'api_name': product.api_name,
        'description': product.description,
        'is_archived': product.is_archived,
        'created_at': product.created_at,
        'updated_at': product.updated_at
    }



def serialize_subscription(sub):
    return {
        'id': sub.id,
        'product_id': sub.product_id,
        'pricing_type': sub.pricing_type,
        'strategy': sub.strategy,
        'is_archived': sub.is_archived,
        'created_at': sub.created_at,
        'updated_at': sub.updated_at,
        'created_by': sub.created_by,
        'updated_by': sub.updated_by,
        'product': serialize_product(sub.product),
        'tiers': [serialize_tier(tier) for tier in sub.tiers]
    }


def serialize_contract(contract):
    return {
        'id': contract.id,
        'client_id': contract.client_id,
        'contract_name': contract.contract_name, 
        'is_archived': contract.is_archived,                
        'created_at': contract.created_at,
        'updated_at': contract.updated_at,
        'created_by': contract.created_by,
        'updated_by': contract.updated_by,
        'subscriptions': [serialize_subscription(sub) for sub in contract.subscriptions],
        'invoices': [serialize_invoice(invoice) for invoice in contract.invoices]
    }


def serialize_invoice(invoice):
    return {
        'id': invoice.id,
        'contract_id': invoice.contract_id,
        'total_amount': invoice.total_amount,
        'start_date': invoice.start_date,
        'end_date': invoice.end_date,
        'is_archived': invoice.is_archived,
        'created_at': invoice.created_at,
        'updated_at': invoice.updated_at,
        'created_by': invoice.created_by,
        'updated_by': invoice.updated_by
    }