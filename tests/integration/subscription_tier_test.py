from tests.factories import (
    subscription_tier_payload, 
    create_rate_card_using_api, 
    create_subscription_using_api,
    create_subscription_tier_using_api,
    create_subscription_dependencies,
    user_payload
)
from models.subscription_tier import SubscriptionTier
from app import db
import uuid


def test_create_subscription_tier_success(client, auth_headers):
    """Test creating a subscription tier with valid data"""
  
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    payload = subscription_tier_payload(rate_card["id"])
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 201
   
    


def test_create_subscription_tier_missing_rate_card_id(client, auth_headers):
    """Test creating subscription tier without rate_card_id"""
    payload = {
        "min_calls": 0,
        "max_calls": 100,
        "unit_price": 10.00
    }
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "Validation Error" in res.get_json()["message"]


def test_create_subscription_tier_missing_min_calls(client, auth_headers):
    """Test creating subscription tier without min_calls"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    payload = {
        "rate_card_id": rate_card["id"],
        "max_calls": 100,
        "unit_price": 10.00
    }
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400


def test_create_subscription_tier_missing_max_calls(client, auth_headers):
    """Test creating subscription tier without max_calls"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    payload = {
        "rate_card_id": rate_card["id"],
        "min_calls": 0,
        "unit_price": 10.00
    }
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400


def test_create_subscription_tier_missing_unit_price(client, auth_headers):
    """Test creating subscription tier without unit_price"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    payload = {
        "rate_card_id": rate_card["id"],
        "min_calls": 0,
        "max_calls": 100
    }
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400


def test_create_subscription_tier_invalid_rate_card_id(client, auth_headers):
    """Test creating subscription tier with non-existent rate_card_id"""
    payload = subscription_tier_payload(str(uuid.uuid4()))
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "RateCard does not exist" in str(res.get_json()["errors"])


def test_create_subscription_tier_invalid_uuid_format(client, auth_headers):
    """Test creating subscription tier with invalid UUID format"""
    payload = subscription_tier_payload("invalid-uuid")
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    errors = res.get_json()["errors"]
    assert "Not a valid UUID" in str(errors)

def test_create_subscription_tier_negative_min_calls(client, auth_headers):
    """Test creating subscription tier with negative min_calls"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    payload = subscription_tier_payload(rate_card["id"], min_calls=-5)
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "Call limits must be non-negative" in str(res.get_json()["errors"])


def test_create_subscription_tier_max_calls_less_than_two(client, auth_headers):
    """Test creating subscription tier with invalid max_calls"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    payload = subscription_tier_payload(rate_card["id"], max_calls=-5)
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "Call limits must be non-negative" in str(res.get_json()["errors"])


def test_create_subscription_tier_min_equals_max(client, auth_headers):
    """Test creating subscription tier with min_calls >= max_calls"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    payload = subscription_tier_payload(rate_card["id"], min_calls=100, max_calls=100)
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "min_calls must be less than max_calls" in str(res.get_json()["errors"])


def test_create_subscription_tier_min_greater_than_max(client, auth_headers):
    """Test creating subscription tier with min_calls > max_calls"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    payload = subscription_tier_payload(rate_card["id"], min_calls=200, max_calls=100)
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "min_calls must be less than max_calls" in str(res.get_json()["errors"])


def test_create_subscription_tier_negative_unit_price(client, auth_headers):
    """Test creating subscription tier with negative unit_price"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    payload = subscription_tier_payload(rate_card["id"], unit_price=-5.00)
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "Unit price must be non-negative" in str(res.get_json()["errors"])


def test_create_subscription_tier_unlimited_max_calls(client, auth_headers):
    """Test creating subscription tier with unlimited max_calls (-1)"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    payload = subscription_tier_payload(rate_card["id"], min_calls=0, max_calls=-1)
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 201
    tier = res.get_json()["data"]["subscription_tier"]
    assert tier["max_calls"] == -1


def test_create_subscription_tier_db_error(client, auth_headers, monkeypatch):
    """Test create subscription tier exception when database commit fails"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    def mock_commit():
        raise Exception("Database connection error")
    
    monkeypatch.setattr("app.db.session.commit", mock_commit)
    
    payload = subscription_tier_payload(rate_card["id"])
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 500
    assert "Error creating subscription tier" in res.get_json()["message"]


def test_create_subscription_tier_validation_error_exception(client, auth_headers, monkeypatch):
    """Test create subscription tier when schema raises ValidationError"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    def mock_load(*args, **kwargs):
        from marshmallow import ValidationError
        raise ValidationError({"test_field": ["Test error message"]})
    
    monkeypatch.setattr("schemas.subscription_tier_schema.subscription_tier_write_schema.load", mock_load)
    
    payload = subscription_tier_payload(rate_card["id"])
    res = client.post("/subscription-tiers", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "Validation Error" in res.get_json()["message"]
    assert "test_field" in res.get_json()["errors"]



# ===== SUBSCRIPTION-TIERS ENDPOINT (GET - List) =====

def test_get_subscription_tiers_success(client, auth_headers):
    """Test getting all subscription tiers"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    res = client.get("/subscription-tiers", headers=auth_headers)
    
    assert res.status_code == 200
    assert res.get_json()["message"] == "Subscription tiers retrieved successfully"
    tiers = res.get_json()["data"]["subscription_tiers"]
    assert len(tiers) >= 1


def test_get_subscription_tiers_excludes_archived(client, auth_headers):
    """Test that archived subscription tiers are not included in list"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    # Archive the tier
    client.delete(f"/subscription-tiers/{tier['id']}", headers=auth_headers)
    
    res = client.get("/subscription-tiers", headers=auth_headers)
    tiers = res.get_json()["data"]["subscription_tiers"]
    tier_ids = [t["id"] for t in tiers]
    
    assert tier["id"] not in tier_ids


def test_get_subscription_tiers_db_error(client, auth_headers, monkeypatch):
    """Test get subscription tiers exception when database query fails"""
    def mock_query(*args, **kwargs):
        raise Exception("Database query error")
    
    monkeypatch.setattr("blueprints.subscription_tier.db.session.query", mock_query)
    
    res = client.get("/subscription-tiers", headers=auth_headers)
    
    assert res.status_code == 500
    assert "Error fetching subscription tiers" in res.get_json()["message"]


# ===== SUBSCRIPTION-TIERS/<ID> ENDPOINT (GET) =====

def test_get_subscription_tier_by_id_success(client, auth_headers):
    """Test getting a subscription tier by ID"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    res = client.get(f"/subscription-tiers/{tier['id']}", headers=auth_headers)
    
    assert res.status_code == 200
    assert res.get_json()["message"] == "Subscription tier retrieved successfully"
    fetched_tier = res.get_json()["data"]["subscription_tier"]
    assert fetched_tier["id"] == tier["id"]


def test_get_subscription_tier_by_id_not_found(client, auth_headers):
    """Test getting non-existent subscription tier"""
    non_existent_id = str(uuid.uuid4())
    res = client.get(f"/subscription-tiers/{non_existent_id}", headers=auth_headers)
    
    assert res.status_code == 404
    assert "Subscription tier not found" in res.get_json()["message"]


def test_get_subscription_tier_by_id_archived(client, auth_headers):
    """Test that archived subscription tiers cannot be retrieved"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    # Archive the tier
    client.delete(f"/subscription-tiers/{tier['id']}", headers=auth_headers)
    
    res = client.get(f"/subscription-tiers/{tier['id']}", headers=auth_headers)
    assert res.status_code == 404


def test_get_subscription_tier_by_id_invalid_uuid(client, auth_headers):
    """Test getting subscription tier with invalid UUID format"""
    res = client.get(f"/subscription-tiers/invalid-uuid", headers=auth_headers)
    
    assert res.status_code == 500
    assert "Error getting subscription tier" in res.get_json()["message"]


def test_get_subscription_tier_by_id_db_error(client, auth_headers, monkeypatch):
    """Test get subscription tier exception when database query fails"""
    def mock_query(*args, **kwargs):
        raise Exception("Database query error")
    
    monkeypatch.setattr("blueprints.subscription_tier.db.session.query", mock_query)
    
    tier_id = str(uuid.uuid4())
    res = client.get(f"/subscription-tiers/{tier_id}", headers=auth_headers)
    
    assert res.status_code == 500
    assert "Error getting subscription tier" in res.get_json()["message"]




def test_get_subscription_tier_by_id_validation_error_exception(client, auth_headers, monkeypatch):
    """Test get subscription tier when ValidationError is raised"""
    from marshmallow import ValidationError
    
    def mock_query(*args, **kwargs):
        raise ValidationError({"tier_field": ["Validation failed"]})
    
    monkeypatch.setattr("blueprints.subscription_tier.db.session.query", mock_query)
    
    tier_id = str(uuid.uuid4())
    res = client.get(f"/subscription-tiers/{tier_id}", headers=auth_headers)
    
    assert res.status_code == 400
    assert "Validation Error" in res.get_json()["message"]





def test_update_subscription_tier_patch_success(client, auth_headers):
    """Test partial update of subscription tier"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    update_payload = {"unit_price": 25.00}
    res = client.patch(f"/subscription-tiers/{tier['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 200
    assert float(res.get_json()["data"]["subscription_tier"]["unit_price"]) == 25.00


def test_update_subscription_tier_put_success(client, auth_headers):
    """Test full update of subscription tier"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    update_payload = {
        "min_calls": 100,
        "max_calls": 500,
        "unit_price": 50.00
    }
    res = client.put(f"/subscription-tiers/{tier['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 200
    updated_tier = res.get_json()["data"]["subscription_tier"]
    assert updated_tier["min_calls"] == 100
    assert updated_tier["max_calls"] == 500


def test_update_subscription_tier_not_found(client, auth_headers):
    """Test updating non-existent subscription tier"""
    non_existent_id = str(uuid.uuid4())
    update_payload = {"unit_price": 25.00}
    
    res = client.patch(f"/subscription-tiers/{non_existent_id}", headers=auth_headers, json=update_payload)
    assert res.status_code == 404


def test_update_subscription_tier_validation_error(client, auth_headers):
    """Test updating subscription tier with invalid data"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    update_payload = {"unit_price": -10.00}
    res = client.patch(f"/subscription-tiers/{tier['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 400
    assert "Validation Error" in res.get_json()["message"]


def test_update_subscription_tier_invalid_min_max(client, auth_headers):
    """Test updating subscription tier with invalid min/max calls"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    update_payload = {"min_calls": 500, "max_calls": 100}
    res = client.patch(f"/subscription-tiers/{tier['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 400
    assert "min_calls must be less than max_calls" in str(res.get_json()["errors"])


def test_update_subscription_tier_db_error(client, auth_headers, monkeypatch):
    """Test update subscription tier exception when database commit fails"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    def mock_commit():
        raise Exception("Database connection error")
    
    monkeypatch.setattr("app.db.session.commit", mock_commit)
    
    update_payload = {"unit_price": 25.00}
    res = client.patch(f"/subscription-tiers/{tier['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 500
    assert "Error updating subscription tier" in res.get_json()["message"]




def test_update_subscription_tier_validation_error_exception(client, auth_headers, monkeypatch):
    """Test update subscription tier when schema raises ValidationError"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    def mock_load(*args, **kwargs):
        from marshmallow import ValidationError
        raise ValidationError({"update_field": ["Update validation failed"]})
    
    monkeypatch.setattr("schemas.subscription_tier_schema.subscription_tier_write_schema.load", mock_load)
    
    update_payload = {"unit_price": 25.00}
    res = client.patch(f"/subscription-tiers/{tier['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 400
    assert "Validation Error" in res.get_json()["message"]




def test_delete_subscription_tier_success(client, auth_headers):
    """Test archiving a subscription tier"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    res = client.delete(f"/subscription-tiers/{tier['id']}", headers=auth_headers)
    
    assert res.status_code == 200
    assert res.get_json()["message"] == "Subscription tier archived successfully"
    assert res.get_json()["data"]["subscription_tier"]["is_archived"] is True


def test_delete_subscription_tier_not_found(client, auth_headers):
    """Test deleting non-existent subscription tier"""
    non_existent_id = str(uuid.uuid4())
    res = client.delete(f"/subscription-tiers/{non_existent_id}", headers=auth_headers)
    
    assert res.status_code == 404
    assert "Subscription tier not found" in res.get_json()["message"]


def test_delete_subscription_tier_db_error(client, auth_headers, monkeypatch):
    """Test delete subscription tier exception when database commit fails"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    def mock_commit():
        raise Exception("Database connection error")
    
    monkeypatch.setattr("app.db.session.commit", mock_commit)
    
    res = client.delete(f"/subscription-tiers/{tier['id']}", headers=auth_headers)
    
    assert res.status_code == 500
    assert "Error archiving subscription tier" in res.get_json()["message"]






def test_delete_subscription_tier_validation_error_exception(client, auth_headers, monkeypatch):
    """Test delete subscription tier when ValidationError is raised"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    from marshmallow import ValidationError
    
    def mock_get(*args, **kwargs):
        raise ValidationError({"delete_field": ["Delete validation failed"]})
    
    monkeypatch.setattr("blueprints.subscription_tier.db.session.get", mock_get)
    
    res = client.delete(f"/subscription-tiers/{tier['id']}", headers=auth_headers)
    
    assert res.status_code == 400
    assert "Validation Error" in res.get_json()["message"]