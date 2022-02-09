from flask import make_response
from json import dumps


def json_response(data: dict, code: int = 200):
	response = make_response(dumps(data, ensure_ascii=False), code)
	response.headers["Content-Type"] = "application/json"

	return response