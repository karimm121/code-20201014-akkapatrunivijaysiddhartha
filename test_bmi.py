#!/usr/local/bin/python3

try:
	import pytest
except ModuleNotFoundError as module_error:
	print("pytest is required to run this program")
else:
	import bmi
	def test_get_data():
		assert bmi.get_data(["hello"]) == False 
		assert bmi.get_data({1:["hello"]}) == False
		assert bmi.get_data() == False

	def test_get_bmi_data():
		assert bmi.get_bmi_data() == False
