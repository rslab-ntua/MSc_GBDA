import geopandas as gpd
import json
import shapely
import requests

def _wkt2esri(wkt:str)->str:
    """Converts WKT geometries to arcGIS geometry strings.
    
    Args:
        wkt (str): WKT geometry string
    Returns:
        str: ESRI arcGIS polygon geometry string
    """
    geom = shapely.wkt.loads(wkt)
    rings = None
    # Testing for polygon type
    if geom.geom_type == 'MultiPolygon':
        rings = []
        for pg in geom.geoms:
            rings += [list(pg.exterior.coords)] + [list(interior.coords) for interior in pg.interiors]    
    elif geom.geom_type == 'Polygon':
        rings = [list(geom.exterior.coords)] + [list(interior.coords) for interior in geom.interiors]
    else:
        print("Shape is not a polygon")
        return None
            
    # Convert to esri geometry json    
    esri = json.dumps({'rings': rings})

    return esri

def corine(aoi:str, to_file:bool = False, fname:str = "corine_2018.shp")->tuple:
    """Downloads Corine Land Cover 2018 data from Copernicus REST API.
    
    Args:
        aoi (str): Path to file with the region of interest
        to_file (bool, optional): Save result to file. Defaults to False
        fname (str, optional): Path and name of the created file. Defaults to "corine_2018.shp"
    Returns:
        tuple: Corine Land Cover 2018 data as GeoDataFrame and the path to saved file
    """
    HTTP_OK = 200

    geoms = gpd.read_file(aoi).dissolve()
    polygons = list(geoms.geometry)
    wkt = f"{polygons[0]}"
    esri = _wkt2esri(wkt)
    # Build URL for retrieving data
    server = "https://image.discomap.eea.europa.eu/arcgis/rest/services/Corine/CLC2018_WM/MapServer/0/query?"
    payload = {
        "geometry": esri, 
        "f": "GeoJSON",
        "inSR": geoms.crs.to_epsg(),
        "geometryType": "esriGeometryPolygon",
        "spatialRel": "esriSpatialRelIntersects",
        "returnGeometry": True
        }
    print ("Starting retrieval...")
    request = requests.get(server, params = payload)
    # Check if server didn't respond to HTTP code = 200
    if request.status_code != HTTP_OK:
        raise requests.exceptions.HTTPError("Failed retrieving POWER data, server returned HTTP code: {} on following URL {}.".format(request.status_code, request.url))
    # In other case is successful
    print ("Successfully retrieved data!")
    json_data = request.json()
    data = gpd.GeoDataFrame.from_features(json_data)
    if to_file:
        data.to_file(fname)
    
    return data, fname

# Example usage to download shapefile based on a given geometry
# data, fname = corine("<path to geojson file defining geometry>", True, "<path to output shape file>")