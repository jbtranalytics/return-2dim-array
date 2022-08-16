from typing import Union, Any
from pydantic import BaseModel, SecretStr, AnyHttpUrl


class SocrataRequest(BaseModel):
    url: AnyHttpUrl
    token: Union[SecretStr, None] = None
    username: Union[SecretStr, None] = None
    password: Union[SecretStr, None] = None
    class Config:
        schema_extra = {
            "example": {
                "url": "https://data.lacity.org/resource/dik5-hwp6.json?$limit=10000",
                "token": "",
                "username": "",
                "password": ""
            }
        }


class ArcGISRequest(BaseModel):
    url: AnyHttpUrl
    class Config:
        schema_extra = {
            "example": {
                "url": "https://services5.arcgis.com/7nsPwEMP38bSkCjy/arcgis/rest/services/Neighborhood_Council_Boundaries_(2018)/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&returnCentroid=true&f=json"
            }
        }


class DataResponseModel(BaseModel):
    data: list[list[Any]]
    fields: dict
