import requests

try:
	from errors import Unauthorized
except ModuleNotFoundError:
	from .errors import Unauthorized


def auth_required(func):
	"""
	Декратор, вызывающий ошибку, если передаваемая функция
	делает неавторизованный запрос
	"""

	def wrapper(*args, **kwargs):
		r: requests.Response = func(*args, **kwargs)
		result = r.json()

		if not result["ok"]:
			if r.status_code == 401:
				raise Unauthorized()

		return r.json()

	return wrapper


def merge_data(func):
	"""
	Декоратор, принимающий на вход функцию, которая возвращает словарь, среди
	элементов которого есть списки, состоящие из словарей
	Возвращает список, являющийся результатом слияния всех списков словаря.
	В каждый элемент-словарь исходных списков добавляется поле "type", обозначающее,
	к какому списку элемент-словарь принадлежал изначально
	Пример:
	:param func: () => {'a': 1, 'b': [{'field1': 1}, 'field2': 2], 'c': ['field3': 5]}:
	:returns dict: [{'field1': 1, type: 'b'}, {'field2': 2, type: 'b'}, {'field3': 5, type: 'c'}]
	"""

	def wrapper(*args, **kwargs):
		def add_type(item, type_):
			item["type"] = type_
			return item

		result: dict = func(*args, **kwargs)
		concatenated = []

		if isinstance(result, dict):
			for data_type, value in result.items():
				if isinstance(value, list):
					concatenated += list(map(lambda item: add_type(item, data_type), value))
		else:
			raise TypeError("Function should return dict, not '%s'" % type(result))

		return concatenated
	return wrapper
