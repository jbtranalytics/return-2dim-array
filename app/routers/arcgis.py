import requests
import json
from fastapi import APIRouter
from ..models import ArcGISRequest, DataResponseModel



router = APIRouter(
    prefix="/arcgis",
    tags=["ArcGIS"]
)


@router.post("/", response_model = DataResponseModel)
def request_data(payload: ArcGISRequest):
    response = getResponse(payload)
    fields = getFields(response["data"]["fields"])
    processed_data = processData(response["data"], fields)
    return {"data": processed_data, "fields": fields}


def getFields(raw_fields_data):
    fields = {}
    for i, field in enumerate(raw_fields_data):
        fields[field["name"]] = {
            "order": i + 1,
            "type": field.get("type", None)
        }
    return fields


def processData(data, fields):
    headers = [field for field in fields.keys()]

    wkid = data.get("spatialReference", {}).get("wkid", None)
    if wkid:
        headers.append("wkid")
    
    features = data["features"]

    has_centroid = "centroid" in features[0]
    if has_centroid:
        headers.append("centroid")
    
    has_geometry = "geometry" in features[0]
    if has_geometry:
        headers.append("geometry_type")
        headers.append("geometry_coordinates")
        has_rings = "rings" in features[0]["geometry"]
        has_xy = "x" in features[0]["geometry"]
        
    processed_data = [headers]
    for feature in features:
        record = []
        attributes = feature.get("attributes", {})
        for field in fields.keys():
            record.append(attributes.get(field, None))
        
        if wkid:
                record.append(wkid)

        if has_centroid:
            centroid = feature.get("centroid", {})
            record.append(json.dumps([centroid.get("x", None), centroid.get("y", None)]))
        
        if has_geometry:
            geometry = feature.get("geometry", {})
            if has_rings:
                coordinates = geometry.get("rings",[])
                if len(coordinates) > 1:
                    record.append("MultiPolygon")
                else:
                    record.append("Polygon")
                record.append(json.dumps(coordinates))
            elif has_xy:
                record.append("Point")
                record.append(json.dumps([geometry.get("x", None), geometry.get("y", None)]))
            else:
                record.append(None)
                record.append(None)
        
        processed_data.append(record.copy())
        
    return processed_data

        
def getResponse(payload: ArcGISRequest):
    with requests.Session() as session:
        response = session.get(payload.url, timeout=20)
    return {"data": response.json(), "headers": response.headers}