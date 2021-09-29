from fastapi import status
from datetime import datetime

import json
import pytest




HEADERS = {"Content-Type": "application/json"}


def test_error_route(client):
    response = client.get("/error_route", headers=HEADERS)
    response_data = response.json().get("detail")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_data == "Not Found"


def test_create_user_error_fields(client):
    """Must be error on validate fields"""
    data = dict(name="x1")
    response = client.post("/user/create", headers=HEADERS, json=data)
    response_data = response.json().get("detail")[0]
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data.get("msg") == "field required"
    assert response_data.get("type") == "value_error.missing"
    # assert response_data.get("loc") == ["body", "user_id"]


def test_login_error_fields(client):
    """Must be error on validate fields"""
    data = dict(username="x1")
    response = client.post("/user/login", headers=HEADERS, json=data)
    response_data = response.json().get("detail")[0]
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data.get("msg") == "field required"
    assert response_data.get("type") == "value_error.missing"



def test_error_jwt_token(client):
    """Must be error on validate fields"""
    _HEADERS = {"Content-Type": "application/json", "Token": "beaver-xxx"}
    response = client.post("/user/dashboard", headers=_HEADERS)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_error_jwt_token_validate(client):
    """Must be error on validate fields"""
    _HEADERS = {"Content-Type": "application/json", "Token": "beaver-xxx"}
    response = client.post("/user/dashboard", headers=_HEADERS)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
