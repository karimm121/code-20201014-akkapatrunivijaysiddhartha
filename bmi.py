
def get_data_validations(data):
	if not isinstance(data,list):
		print(f"unhandled data format")
		return False 
	if not isinstance(data[0],dict):
		print(f"unhandled data format")
		return False 
	return True


def get_data(data=None):
	if not get_data_validations(data):
		return False
	bmis = {}
	index = 0
	for individual_details in data:
		individual_gender,individual_height,individual_weight = individual_details["Gender"],\
						    int(individual_details["HeightCm"])/100,\
						    int(individual_details["WeightKg"])
		individual_height *= individual_height
		bmi = individual_weight/individual_height
		bmis[index] = round(bmi,1) 
		index += 1
	return bmis

def get_bmi_data_validations(chart):
	if chart == None:
		return False
	return True

def get_bmi_data(chart=None):
	if not get_bmi_data_validations(chart):
		return False
	try:
		import pandas as pd
	except ModuleNotFoundError as module_error:
		print("pandas has to be installed to run this file")
		return
	else:
		bmi_chart_data = pd.read_csv(chart)
		bmi_data ={}
		BMICategory,bmi_range,health_risk=bmi_chart_data['BMICategory'],\
					  bmi_chart_data['BMIRange(kg/m2)'],\
					  bmi_chart_data['HealthRisk']
	
	for categories,ranges,risks in [(BMICategory,bmi_range,health_risk)]:
		bmi_data["ranges"] ={}
		iterations = len(categories)
		for iteration in range(iterations):
			bmi_data["ranges"][ranges[iteration]] = [categories[iteration],risks[iteration]]
	bmi_range_keys=bmi_data["ranges"].keys()
	bmis = get_data(DATA)
	overweight = 0
	BMICategory=BMIRange=HealthRisk=""

	def get_details():

		BMICategory = bmi_data["ranges"][bmi_range_key][0]
		BMIRange = bmi_range_key
		HealthRisk = bmi_data["ranges"][bmi_range_key][1]
		return BMICategory,BMIRange,HealthRisk


	for bmi in bmis.keys():

		for bmi_range_key in bmi_range_keys:	

			if "-" in bmi_range_key and bmi_data["ranges"][bmi_range_key][0] == "Overweight" :
				lower_limit,upper_limit = bmi_range_key.split('-')
				if bmis[bmi] >= float(lower_limit)  and bmis[bmi] <= float(upper_limit):
					overweight += 1

			if "-" in bmi_range_key:
				lower_limit,upper_limit = bmi_range_key.split('-')
				if bmis[bmi] >= float(lower_limit)  and bmis[bmi] <= float(upper_limit):
					BMICategory,BMIRange,HealthRisk = get_details()

			elif "below" in bmi_range_key:
				if bmis[bmi] <= float(bmi_range_key.split("and")[0]):
					BMICategory,BMIRange,HealthRisk = get_details()

			elif "above" in bmi_range_key:
				if bmis[bmi] >= float(bmi_range_key.split("and")[0]):
					BMICategory,BMIRange,HealthRisk = get_details()

		data = DATA[bmi]
		data["BMICategory"],data["BMIRange"],data["HealthRisk"] = BMICategory , BMIRange, HealthRisk

	return DATA, overweight

DATA=[{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },\
 { "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },\
 { "Gender": "Male", "HeightCm": 180, "WeightKg": 77 },\
 { "Gender": "Female", "HeightCm": 166, "WeightKg": 62},\
 {"Gender": "Female", "HeightCm": 150, "WeightKg": 70},\
 {"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]

chart='BMI-CHART.csv'
if __name__ == "__main__":

	import os
	if not os.path.isfile(chart):
		print(f"{chart} file for BMI Category is not found")

	else:
		DATA,overweights = get_bmi_data(chart)
		for data in DATA:
			print(data)
		print(f"overweights count: {overweights}")
