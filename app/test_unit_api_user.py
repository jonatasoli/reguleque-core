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
    data = dict(username="x1")
    response = client.post("/user/create", headers=HEADERS, json=data)
    response_data = response.json().get("detail")[0]
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data.get("msg") == "field required"
    assert response_data.get("type") == "value_error.missing"
    # assert response_data.get("loc") == ["body", "user_id"]


def test_create_user(client, mocker):
    """Must return dict with user and Token"""
    mocker.patch(
        "user.service_layer.Auth.signup",
        return_value=dict(message='user create with id 2')
    )
    data = dict(username="test", password="asdasd", mail="test@mail.com")
    response = client.post("/user/create", headers=HEADERS, json=data)
    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response_data, dict)
    assert response_data == dict(message='user create with id 2')


def test_login_error_fields(client):
    """Must be error on validate fields"""
    data = dict(username="x1")
    response = client.post("/user/login", headers=HEADERS, json=data)
    response_data = response.json().get("detail")[0]
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data.get("msg") == "field required"
    assert response_data.get("type") == "value_error.missing"



def test_login_user(client, mocker):
    """Must be return message and token"""
    mocker.patch(
        "user.service_layer.Auth.login",
        return_value=dict(
            access_token="access_token",
            token_type= "bearer",
            role= "user",
            message='login user'
        )
    )
    data = dict(username="test", password="asdasd")
    response = client.post("/user/login", headers=HEADERS, json=data)
    response_header = response.headers.get('content-type')
    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_header == 'application/json'
    assert response_data == dict(
        access_token="access_token",
        token_type= "bearer",
        role= "user",
        message='login user'

    )


@pytest.mark.skip
def test_jwt_token(client):
    """Must be error on validate fields"""
    _HEADERS = {"Content-Type": "application/json", "Token": "beaver-xxx"}
    _data = {"Token", "beaver-xxx"}
    response = client.post("/user/dashboard", data=_data, headers=_HEADERS)
    assert response.status_code == status.HTTP_200_OK


def test_error_jwt_token_validate(client):
    """Must be error on validate fields"""
    _HEADERS = {"Content-Type": "application/json", "Token": "beaver-xxx"}
    response = client.post("/user/dashboard", headers=_HEADERS)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
