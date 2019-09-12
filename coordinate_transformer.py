import pyproj

# lat = [46.25058]
# lon = [14.34885]


def transform_wgs84_to_gk(lon, lat):
	proj_wgs84 = pyproj.Proj(init="epsg:4326")
	gk_string = "+proj=tmerc +lon_0=15E +ellps=bessel +x_0=500000 +y_0=-5000000  +k=0.9999 +towgs84=426.9466,142.5844,460.0891,4.907790,4.488389,-12.423059,17.1131 -f %.2f"

	proj_gk = pyproj.Proj(gk_string)

	x, y = pyproj.transform(proj_wgs84, proj_gk, lon, lat)
	return x, y

