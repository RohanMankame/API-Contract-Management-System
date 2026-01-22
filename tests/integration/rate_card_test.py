from tests.factories import (
    rate_card_payload,
    create_rate_card_using_api,
    create_subscription_using_api,
    create_subscription_dependencies,
)
from models.rate_card import RateCard
from models.subscription_tier import SubscriptionTier
from app import db
import uuid




def test_create_rate_card_success(client, auth_headers):
    """Test creating a rate card with valid data"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    
    payload = rate_card_payload(subscription["id"])
    res = client.post("/rate-cards", headers=auth_headers, json=payload)
    
    assert res.status_code == 201
    assert res.get_json()["message"] == "Rate card created successfully"
    rate_card = res.get_json()["data"]["rate_card"]
    assert rate_card["subscription_id"] == subscription["id"]


def test_create_rate_card_missing_subscription_id(client, auth_headers):
    """Test creating rate card without subscription_id"""
    payload = {
        "start_date": "2025-01-01T00:00:00.000Z",
        "end_date": "2026-12-31T23:59:59.999Z",
    }
    res = client.post("/rate-cards", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "Validation Error" in res.get_json()["message"]


def test_create_rate_card_missing_start_date(client, auth_headers):
    """Test creating rate card without start_date"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    
    payload = {
        "subscription_id": subscription["id"],
        "end_date": "2026-12-31T23:59:59.999Z",
    }
    res = client.post("/rate-cards", headers=auth_headers, json=payload)
    
    assert res.status_code == 400


def test_create_rate_card_missing_end_date(client, auth_headers):
    """Test creating rate card without end_date"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    
    payload = {
        "subscription_id": subscription["id"],
        "start_date": "2025-01-01T00:00:00.000Z",
    }
    res = client.post("/rate-cards", headers=auth_headers, json=payload)
    
    assert res.status_code == 400


def test_create_rate_card_invalid_subscription_id(client, auth_headers):
    """Test creating rate card with non-existent subscription_id"""
    payload = rate_card_payload(str(uuid.uuid4()))
    res = client.post("/rate-cards", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "subscription_id does not exist" in str(res.get_json()["errors"])


def test_create_rate_card_start_after_end(client, auth_headers):
    """Test creating rate card where start_date >= end_date"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    
    payload = {
        "subscription_id": subscription["id"],
        "start_date": "2026-12-31T23:59:59.999Z",
        "end_date": "2025-01-01T00:00:00.000Z",
    }
    res = client.post("/rate-cards", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "start date must be before the end date" in str(res.get_json()["errors"])


def test_create_rate_card_start_before_contract_start(client, auth_headers):
    """Test creating rate card with start_date before contract start_date"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    
    payload = {
        "subscription_id": subscription["id"],
        "start_date": "2024-12-31T00:00:00.000Z",  # Before contract start
        "end_date": "2026-12-31T23:59:59.999Z",
    }
    res = client.post("/rate-cards", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "cannot be before the contract start_date" in str(res.get_json()["errors"])


def test_create_rate_card_end_after_contract_end(client, auth_headers):
    """Test creating rate card with end_date after contract end_date"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    
    payload = {
        "subscription_id": subscription["id"],
        "start_date": "2025-01-01T00:00:00.000Z",
        "end_date": "2027-12-31T23:59:59.999Z",  # After contract end
    }
    res = client.post("/rate-cards", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "cannot be after the contract end_date" in str(res.get_json()["errors"])


def test_create_rate_card_overlapping_dates(client, auth_headers):
    """Test creating rate card with overlapping date range"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    
    # Create first rate card
    payload1 = rate_card_payload(subscription["id"])
    res1 = client.post("/rate-cards", headers=auth_headers, json=payload1)
    assert res1.status_code == 201
    
    # Try to create second rate card with overlapping dates
    payload2 = {
        "subscription_id": subscription["id"],
        "start_date": "2025-06-01T00:00:00.000Z",
        "end_date": "2026-06-01T00:00:00.000Z",
    }
    res2 = client.post("/rate-cards", headers=auth_headers, json=payload2)
    
    assert res2.status_code == 400
    assert "overlaps with an existing rate card" in str(res2.get_json()["errors"])


def test_create_rate_card_db_error(client, auth_headers, monkeypatch):
    """Test create rate card exception when database commit fails"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    
    def mock_commit():
        raise Exception("Database connection error")
    
    monkeypatch.setattr("app.db.session.commit", mock_commit)
    
    payload = rate_card_payload(subscription["id"])
    res = client.post("/rate-cards", headers=auth_headers, json=payload)
    
    assert res.status_code == 500
    assert "Error creating rate card" in res.get_json()["message"]


def test_create_rate_card_validation_error_exception(client, auth_headers, monkeypatch):
    """Test create rate card when schema raises ValidationError"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    
    def mock_load(*args, **kwargs):
        from marshmallow import ValidationError
        raise ValidationError({"test_field": ["Test error message"]})
    
    monkeypatch.setattr("schemas.rate_card_schema.rate_card_write_schema.load", mock_load)
    
    payload = rate_card_payload(subscription["id"])
    res = client.post("/rate-cards", headers=auth_headers, json=payload)
    
    assert res.status_code == 400
    assert "Validation Error" in res.get_json()["message"]



def test_get_rate_cards_success(client, auth_headers):
    """Test getting all rate cards"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    res = client.get("/rate-cards", headers=auth_headers)
    
    assert res.status_code == 200
    assert res.get_json()["message"] == "Rate cards retrieved successfully"
    rate_cards = res.get_json()["data"]["rate_cards"]
    assert len(rate_cards) >= 1


def test_get_rate_cards_excludes_archived(client, auth_headers):
    """Test that archived rate cards are not included in list"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    # Archive the rate card
    client.delete(f"/rate-cards/{rate_card['id']}", headers=auth_headers)
    
    res = client.get("/rate-cards", headers=auth_headers)
    rate_cards = res.get_json()["data"]["rate_cards"]
    rate_card_ids = [rc["id"] for rc in rate_cards]
    
    assert rate_card["id"] not in rate_card_ids


def test_get_rate_cards_empty_list(client, auth_headers):
    """Test getting rate cards when none exist"""
    res = client.get("/rate-cards", headers=auth_headers)
    
    assert res.status_code == 200
    assert res.get_json()["data"]["rate_cards"] == []


def test_get_rate_cards_db_error(client, auth_headers, monkeypatch):
    """Test get rate cards exception when database query fails"""
    def mock_query(*args, **kwargs):
        raise Exception("Database query error")
    
    monkeypatch.setattr("blueprints.rate_card.db.session.query", mock_query)
    
    res = client.get("/rate-cards", headers=auth_headers)
    
    assert res.status_code == 500
    assert "Error fetching rate cards" in res.get_json()["message"]




def test_get_rate_card_by_id_success(client, auth_headers):
    """Test getting a rate card by ID"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    res = client.get(f"/rate-cards/{rate_card['id']}", headers=auth_headers)
    
    assert res.status_code == 200
    assert res.get_json()["message"] == "Rate card retrieved successfully"
    fetched_rc = res.get_json()["data"]["rate_card"]
    assert fetched_rc["id"] == rate_card["id"]


def test_get_rate_card_by_id_not_found(client, auth_headers):
    """Test getting non-existent rate card"""
    non_existent_id = str(uuid.uuid4())
    res = client.get(f"/rate-cards/{non_existent_id}", headers=auth_headers)
    
    assert res.status_code == 404
    assert "Rate card not found" in res.get_json()["message"]


def test_get_rate_card_by_id_archived(client, auth_headers):
    """Test that archived rate cards cannot be retrieved"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    # Archive the rate card
    client.delete(f"/rate-cards/{rate_card['id']}", headers=auth_headers)
    
    res = client.get(f"/rate-cards/{rate_card['id']}", headers=auth_headers)
    assert res.status_code == 404


def test_get_rate_card_by_id_invalid_uuid_format(client, auth_headers):
    """Test getting rate card with invalid UUID format"""
    res = client.get(f"/rate-cards/invalid-uuid", headers=auth_headers)
    
    assert res.status_code == 400
    assert "Invalid rate card id format" in res.get_json()["message"]


def test_get_rate_card_by_id_db_error(client, auth_headers, monkeypatch):
    """Test get rate card exception when database error occurs"""
    def mock_get(*args, **kwargs):
        raise Exception("Database error")
    
    monkeypatch.setattr("blueprints.rate_card.db.session.get", mock_get)
    
    rate_card_id = str(uuid.uuid4())
    res = client.get(f"/rate-cards/{rate_card_id}", headers=auth_headers)
    
    assert res.status_code == 500
    assert "Error fetching rate card" in res.get_json()["message"]




def test_update_rate_card_patch_success(client, auth_headers):
    """Test partial update of rate card"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    update_payload = {
        "start_date": "2025-03-01T00:00:00.000Z",
    }
    res = client.patch(f"/rate-cards/{rate_card['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 200
    assert res.get_json()["message"] == "Rate card updated successfully"


def test_update_rate_card_put_success(client, auth_headers):
    """Test full update of rate card"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    update_payload = {
        "subscription_id": subscription["id"],
        "start_date": "2025-02-01T00:00:00.000Z",
        "end_date": "2026-11-30T23:59:59.999Z",
    }
    res = client.put(f"/rate-cards/{rate_card['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 200
    updated_rc = res.get_json()["data"]["rate_card"]
    assert updated_rc["id"] == rate_card["id"]


def test_update_rate_card_not_found(client, auth_headers):
    """Test updating non-existent rate card"""
    non_existent_id = str(uuid.uuid4())
    update_payload = {"start_date": "2025-03-01T00:00:00.000Z"}
    
    res = client.patch(f"/rate-cards/{non_existent_id}", headers=auth_headers, json=update_payload)
    assert res.status_code == 404


def test_update_rate_card_archived(client, auth_headers):
    """Test updating archived rate card"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    # Archive the rate card
    client.delete(f"/rate-cards/{rate_card['id']}", headers=auth_headers)
    
    update_payload = {"start_date": "2025-03-01T00:00:00.000Z"}
    res = client.patch(f"/rate-cards/{rate_card['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 404


def test_update_rate_card_invalid_uuid_format(client, auth_headers):
    """Test updating rate card with invalid UUID format"""
    update_payload = {"start_date": "2025-03-01T00:00:00.000Z"}
    res = client.patch(f"/rate-cards/invalid-uuid", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 400
    assert "Invalid rate card id format" in res.get_json()["message"]


def test_update_rate_card_invalid_dates(client, auth_headers):
    """Test updating rate card with invalid date range"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    update_payload = {
        "start_date": "2026-12-31T23:59:59.999Z",
        "end_date": "2025-01-01T00:00:00.000Z",
    }
    res = client.patch(f"/rate-cards/{rate_card['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 400
    assert "start date must be before the end date" in str(res.get_json()["errors"])


def test_update_rate_card_overlapping_dates(client, auth_headers):
    """Test updating rate card to overlapping date range"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    
    # Create two non-overlapping rate cards
    payload1 = {
        "subscription_id": subscription["id"],
        "start_date": "2025-01-01T00:00:00.000Z",
        "end_date": "2025-06-30T23:59:59.999Z",
    }
    res1 = client.post("/rate-cards", headers=auth_headers, json=payload1)
    assert res1.status_code == 201
    rc1 = res1.get_json()["data"]["rate_card"]
    
    payload2 = {
        "subscription_id": subscription["id"],
        "start_date": "2025-07-01T00:00:00.000Z",
        "end_date": "2026-12-31T23:59:59.999Z",
    }
    res2 = client.post("/rate-cards", headers=auth_headers, json=payload2)
    assert res2.status_code == 201
    rc2 = res2.get_json()["data"]["rate_card"]
    
    # Try to update rc1 to overlap with rc2
    update_payload = {
        "subscription_id": subscription["id"],
        "start_date": "2025-06-15T00:00:00.000Z",
        "end_date": "2025-08-01T00:00:00.000Z",
    }
    res = client.patch(f"/rate-cards/{rc1['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 400
    assert "overlaps with an existing rate card" in str(res.get_json()["errors"])


def test_update_rate_card_db_error(client, auth_headers, monkeypatch):
    """Test update rate card exception when database commit fails"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    def mock_commit():
        raise Exception("Database connection error")
    
    monkeypatch.setattr("app.db.session.commit", mock_commit)
    
    update_payload = {"start_date": "2025-03-01T00:00:00.000Z"}
    res = client.patch(f"/rate-cards/{rate_card['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 500
    assert "Error updating rate card" in res.get_json()["message"]


def test_update_rate_card_validation_error_exception(client, auth_headers, monkeypatch):
    """Test update rate card when schema raises ValidationError"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    def mock_load(*args, **kwargs):
        from marshmallow import ValidationError
        raise ValidationError({"update_field": ["Update validation failed"]})
    
    monkeypatch.setattr("schemas.rate_card_schema.rate_card_write_schema.load", mock_load)
    
    update_payload = {"start_date": "2025-03-01T00:00:00.000Z"}
    res = client.patch(f"/rate-cards/{rate_card['id']}", headers=auth_headers, json=update_payload)
    
    assert res.status_code == 400
    assert "Validation Error" in res.get_json()["message"]




def test_delete_rate_card_success(client, auth_headers):
    """Test archiving a rate card"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    res = client.delete(f"/rate-cards/{rate_card['id']}", headers=auth_headers)
    
    assert res.status_code == 200
    assert res.get_json()["message"] == "Rate card archived successfully"


def test_delete_rate_card_not_found(client, auth_headers):
    """Test deleting non-existent rate card"""
    non_existent_id = str(uuid.uuid4())
    res = client.delete(f"/rate-cards/{non_existent_id}", headers=auth_headers)
    
    assert res.status_code == 404
    assert "Rate card not found" in res.get_json()["message"]


def test_delete_rate_card_archived(client, auth_headers):
    """Test deleting already archived rate card"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    # Archive once
    client.delete(f"/rate-cards/{rate_card['id']}", headers=auth_headers)
    
    # Try to delete again
    res = client.delete(f"/rate-cards/{rate_card['id']}", headers=auth_headers)
    assert res.status_code == 404


def test_delete_rate_card_invalid_uuid_format(client, auth_headers):
    """Test deleting rate card with invalid UUID format"""
    res = client.delete(f"/rate-cards/invalid-uuid", headers=auth_headers)
    
    assert res.status_code == 400
    assert "Invalid rate card id format" in res.get_json()["message"]


def test_delete_rate_card_db_error(client, auth_headers, monkeypatch):
    """Test delete rate card exception when database commit fails"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    def mock_commit():
        raise Exception("Database connection error")
    
    monkeypatch.setattr("app.db.session.commit", mock_commit)
    
    res = client.delete(f"/rate-cards/{rate_card['id']}", headers=auth_headers)
    
    assert res.status_code == 500
    assert "Error archiving rate card" in res.get_json()["message"]




def test_get_rate_card_subscription_tiers_success(client, auth_headers):
    """Test getting subscription tiers for a rate card"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    from tests.factories import create_subscription_tier_using_api
    create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    res = client.get(f"/rate-cards/{rate_card['id']}/subscription-tiers", headers=auth_headers)
    
    assert res.status_code == 200
    assert res.get_json()["message"].startswith("Subscription tiers for id:")
    tiers = res.get_json()["data"]["subscription_tiers"]
    assert len(tiers) >= 1


def test_get_rate_card_subscription_tiers_excludes_archived(client, auth_headers):
    """Test that archived tiers are not included"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    from tests.factories import create_subscription_tier_using_api
    tier = create_subscription_tier_using_api(client, auth_headers, rate_card["id"])
    
    # Archive the tier
    client.delete(f"/subscription-tiers/{tier['id']}", headers=auth_headers)
    
    res = client.get(f"/rate-cards/{rate_card['id']}/subscription-tiers", headers=auth_headers)
    tiers = res.get_json()["data"]["subscription_tiers"]
    tier_ids = [t["id"] for t in tiers]
    
    assert tier["id"] not in tier_ids


def test_get_rate_card_subscription_tiers_empty(client, auth_headers):
    """Test getting subscription tiers when rate card has none"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    res = client.get(f"/rate-cards/{rate_card['id']}/subscription-tiers", headers=auth_headers)
    
    assert res.status_code == 200
    assert res.get_json()["data"]["subscription_tiers"] == []


def test_get_rate_card_subscription_tiers_not_found(client, auth_headers):
    """Test getting tiers for non-existent rate card"""
    non_existent_id = str(uuid.uuid4())
    res = client.get(f"/rate-cards/{non_existent_id}/subscription-tiers", headers=auth_headers)
    
    assert res.status_code == 404
    assert "Rate card not found" in res.get_json()["message"]


def test_get_rate_card_subscription_tiers_archived_rate_card(client, auth_headers):
    """Test getting tiers for archived rate card"""
    deps = create_subscription_dependencies(client, auth_headers)
    subscription = create_subscription_using_api(client, auth_headers, deps["contract"]["id"], deps["product"]["id"])
    rate_card = create_rate_card_using_api(client, auth_headers, subscription["id"])
    
    # Archive the rate card
    client.delete(f"/rate-cards/{rate_card['id']}", headers=auth_headers)
    
    res = client.get(f"/rate-cards/{rate_card['id']}/subscription-tiers", headers=auth_headers)
    assert res.status_code == 404


def test_get_rate_card_subscription_tiers_invalid_uuid_format(client, auth_headers):
    """Test getting tiers with invalid UUID format"""
    res = client.get(f"/rate-cards/invalid-uuid/subscription-tiers", headers=auth_headers)
    
    assert res.status_code == 400
    assert "Invalid rate card id format" in res.get_json()["message"]


def test_get_rate_card_subscription_tiers_db_error(client, auth_headers, monkeypatch):
    """Test getting tiers exception when database error occurs"""
    def mock_get(*args, **kwargs):
        raise Exception("Database error")
    
    monkeypatch.setattr("blueprints.rate_card.db.session.get", mock_get)
    
    rate_card_id = str(uuid.uuid4())
    res = client.get(f"/rate-cards/{rate_card_id}/subscription-tiers", headers=auth_headers)
    
    assert res.status_code == 500
    assert "Error fetching subscription tiers for rate card" in res.get_json()["message"]