from flask import Flask, jsonify, request, render_template,json
import urllib3, requests

app = Flask(__name__)
#HOST = '0.0.0.0'
#PORT = 8080

# wml_credentials={
#   "password": "31dbf7ca-13bc-4b59-97ad-93db13a5c5f3",
#   "url": "https://us-south.ml.cloud.ibm.com",
#   "username": "59f50ecd-4ee3-4410-a687-077315fa06c3"
# }

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/result', methods=['POST','GET'])
def result():

	if request.method == 'POST':
		# PassengerId = request.args.get('passengerid')
		income = request.form.get('income')
		applied = request.form.get('applied')
		residence = request.form.get('residence')
		address = request.form.get('address')
		employer = request.form.get('employer')
		cards = request.form.get('cards')
		debt = request.form.get('debt')
		loans = request.form.get('loans')
		amount = request.form.get('amount')
		price = request.form.get('price')
		location = request.form.get('location')  

		print(income)
		print(applied)
		print(residence)
		print(address)
		print(employer)
		print(cards)
		print(debt)
		print(loans)
		print(amount)
		print(price)
		print(location)



		apikey = "7nGUIe30VuAvMitbKVTXtGOxwFT1OSzGIklmrPRsjrnv"

		# Get an IAM token from IBM Cloud
		url     = "https://iam.bluemix.net/oidc/token"
		headers = { "Content-Type" : "application/x-www-form-urlencoded" }
		data    = "apikey=" + apikey + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
		IBM_cloud_IAM_uid = "bx"
		IBM_cloud_IAM_pwd = "bx"
		response  = requests.post( url, headers=headers, data=data, auth=( IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd ) )
		iam_token = response.json()["access_token"]
		ml_instance_id = "1f796ca3-54a1-494b-8e35-6dde99cf5888"
		print(iam_token)  

		header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token, 'ML-Instance-ID': ml_instance_id}

		payload_scoring = {"fields": ["Income", "AppliedOnline", "Residence", "YearCurrentAddress", "YearsCurrentEmployer", "NumberOfCards", "CCDebt", "Loans", "LoanAmount", "SalePrice", "Location"], "values": [[int(income), applied, residence, int(address), int(employer), int(cards), int(debt), int(loans), int(amount),int(price), int(location)]]}
		print(payload_scoring)
		response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/v3/wml_instances/1f796ca3-54a1-494b-8e35-6dde99cf5888/deployments/594e78c6-1723-4fa2-9ee4-53ab61f7ea65/online', json=payload_scoring, headers=header)

		jsonResult = json.loads(response_scoring.text) 
		# print (jsonResult)
		print (jsonResult['values'][0]) 

		if (jsonResult['values'][0][0]) == "YES":
			prob = (jsonResult['values'][0][1])*100 
			finalResult = "The customer will default the mortgage with " + str(prob) + "% confidence"
			print(finalResult)
			return render_template('result.html', value = finalResult)
			# return ("The customer is approved to get a mortgage with " + str(prob) + " probabilty") 

		elif (jsonResult['values'][0][0]) == "NO": 
			probb = (jsonResult['values'][0][1])*100 
			finalResult = "The customer will not default the mortgage with " + str(probb) + "% confidence"
			print(finalResult)
			return render_template('result.html', value = finalResult)
			# return ("The customer is not approved for a mortgage with " + str(probb) + " probabilty")

		return (json.dumps(jsonResult))



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
