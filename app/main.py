from fastapi import FastAPI
from .routers import socrata, arcgis

description = """
API helps format data from various sources into two-dimensional array with field types for schema generation.

## Data Sources

You will be able to format data from:

* **ArcGIS** (in json format)
* **Socrata** (in json format)
* **GeoJSON** (not implemented yet)
* **CSV** (not implemented yet)
"""

tags_metadata = [
    {
        "name": "Socrata",
        "description": "",
        "externalDocs": {
            "description": "URL Example Reference",
            "url": "https://dev.socrata.com/foundry/data.lacity.org/dik5-hwp6",
        },
    },
    {
        "name": "ArcGIS",
        "description": "",
        "externalDocs": {
            "description": "URL Example Reference",
            "url": "https://geohub.lacity.org/datasets/lahub::neighborhood-council-boundaries-2018/api",
        },
    },
]


app = FastAPI(
    title="Return 2Dim Array",
    description=description,
    version="1.0.0",
    terms_of_service="https://www.blank.org/",
    contact={
        "name": "JBTR Analytics",
        "url": "https://www.blank.org/",
        "email": "jbtranalytics@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)


app.include_router(socrata.router)
app.include_router(arcgis.router)
