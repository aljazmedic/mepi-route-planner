import csv, json, geopy, requests, pprint
import vectors, math
from bs4 import BeautifulSoup
from coordinate_transformer import transform_wgs84_to_gk


def read_data(path: str) -> dict:
	r = []
	with open(path) as rf:
		reader = csv.reader(rf, delimiter=";")
		
		for row in reader:
			r.append({"name":row[0]})
	return r


def get_lat_lon(agent: geopy.Nominatim, sess: requests.Session, e: dict) -> dict:
	d = agent.geocode(e["name"], exactly_one=True).raw
	print(d)
	e["coords"] = {"lat": float(d["lat"]), "lon": float(d["lon"])}

	x, y = transform_wgs84_to_gk([e["coords"]["lon"]], [e["coords"]["lat"]])
	x, y = x[0], y[0]
	e["GK"] = [x, y]
	"""
	# nmv
	data_nmv = {
		"locations":
			[
				{
					"latitude": e["coords"]["lat"],
					"longitude": e["coords"]["lon"]
				}
			]
	}
	nmv_req = sess.post("https://api.open-elevation.com/api/v1/lookup", data=data_nmv)
	e["nmv"] = nmv_req.json()["results"][0]["elevation"]
	""""""
	# GK coords
	"""
	return e

# luka.colaric@sckr.si
def angle_between(v1: vectors.Vector, v2: vectors.Vector) -> float:
	print(v1, v2)
	dot = v1.x*v2.x+v1.y*v2.y
	angle = math.acos(dot / (v1.magnitude()*v2.magnitude())) * (360 / 2 / math.pi)
	print(angle)
	if v2.x < v1.x:
		return 360 - angle
	return angle


def azimut(e1: dict, e2: dict) -> dict:
	e1_g = vectors.Vector(*e1["GK"], 0)
	e2_g = vectors.Vector(*e2["GK"], 0)
	delta = e2_g.substract(e1_g)
	print(delta)
	delta = delta.multiply(1 / delta.magnitude())
	e2["azimut"] = angle_between(vectors.Vector(1, 0, 0), delta)
	return e2


if __name__ == "__main__":
	pp = pprint.PrettyPrinter(indent=4)
	geo_agent = geopy.Nominatim(user_agent="mepi-route-planner")
	requests_sess = requests.Session()
	route = read_data("data.csv")
	for e in route:
		get_lat_lon(geo_agent, requests_sess, e)
	for i in range(1, len(route)):
		route[i] = azimut(route[i-1], route[i])
	pp.pprint(route)
