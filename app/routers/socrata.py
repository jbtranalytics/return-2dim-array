import requests
import json
from fastapi import APIRouter
from ..models import DataResponseModel, SocrataRequest


router = APIRouter(
    prefix="/socrata",
    tags=["Socrata"]
)


@router.post("/", response_model = DataResponseModel)
def request_data(payload: SocrataRequest):
    response = getResponse(payload)
    fields = getFields(response["headers"])
    processed_data = processData(response["data"], fields)
    return {"data": processed_data, "fields": fields}


def processData(data, fields):
    processed_data = [[field for field in fields.keys()]]
    for record in data:
        processed_data.append([record.get(field, None) for field in fields.keys()])
    return processed_data


def getFields(raw_fields_data):
    field_names = json.loads(raw_fields_data['X-SODA2-Fields'])
    field_types = json.loads(raw_fields_data['X-SODA2-Types'])
    fields = {}
    for i, field_name in enumerate(field_names):
        fields[field_name] = {
            "order": i + 1,
            "type": field_types[i]
        }
    return fields


def getResponse(payload: SocrataRequest):
    with requests.Session() as session:
        if payload.username and payload.password:
            session.auth(payload.username.get_secret_value(), payload.password.get_secret_value())
        if payload.token:
            session.headers.update({"X-App-Token": payload.token.get_secret_value()})
        response = session.get(payload.url, timeout=600)
    return {"data": response.json(), "headers": response.headers}