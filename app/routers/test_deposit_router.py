from ..main import app
from fastapi import HTTPException
from fastapi.testclient import TestClient


client = TestClient(app)


def test_calculate_deposit_single_month():
    deposit_data = {
        "amount": 10000,
        "date": "01.01.2022",
        "rate": 5,
        "periods": 1
    }
    # deposit_data = DepositSchema(amount=1000, date='01.01.2022', rate=5, periods=1)
    expected_result = {'01.01.2022': 10041.67}

    response = client.post('/deposits/calculate', json=deposit_data)
    assert response.status_code == 200
    assert response.json() == expected_result


def test_calculate_deposit_large_periods():
    deposit_data = {
        "amount": 10000.50,
        "date": "01.01.2022",
        "rate": 5,
        "periods": 60
    }

    response = client.post('/deposits/calculate', json=deposit_data)
    assert response.status_code == 200

    last_date = "01.12.2026"
    expected_last_amount = 12834.23
    assert response.json()[last_date] == expected_last_amount


def test_calculate_deposit_invalid_date_format():
    deposit_data = {
        "amount": 100000,
        "date": "01/01/2022",
        "rate": 5,
        "periods": 1
    }

    try:
        client.post('/deposits/calculate', json=deposit_data)
    except HTTPException as e:
        assert e.status_code == 400
        assert str(e.detail) == "value is not a valid datetime (format '%d.%m.%Y' expected)"
