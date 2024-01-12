import requests
import os

# Don't share API key
my_secret = [YOUR-API-KEY-HERE]

# Get currency and rate. If currency_from is provided, return the exchange rate
def get_currency_and_rate(prompt, currency_from=""):
  data={"result": "error"}
  while data["result"] =="error":
    currency=input(prompt).upper()
    request_url = "https://v6.exchangerate-api.com/v6/" + my_secret + "/latest/" + currency

    # Get data from the web API
    response = requests.get(request_url)
    # Convert the JSON data object into a Python-friendly format.
    data = response.json()

    # Check if the API request was successful. If not, print an error message.
    if data["result"]=="error":
      print("")
      print("===> Error detected: ", data["error-type"])
      print("===> Please enter a valid currency...")
      print("")
    else:
      if currency_from =="":
        rate=data["conversion_rates"][currency]
      else:
        rate=1/data["conversion_rates"][currency_from]
      #return tuple of currency and exchange rate
      return currency, rate

def proceed():  
  # Get currency to convert from
  currency_from, rate = get_currency_and_rate("Enter currency to convert from: ")
  
  # Get currency to convert to and the exchange rate
  currency_to, rate = get_currency_and_rate("Enter currency to convert to: ", currency_from)
  
  # Get amount to convert with error checking.
  amt = 0
  while amt <= 0:
    amt = float(input("Enter " + currency_from + " amount to convert: "))
    if amt<=0:
      print("")
      print("===> Error detected: amount is not greater than zero.")
      print("===> Please enter a positive number...")
      print("")
  
  conversion_result=amt*rate
  
  print("")
  print("====================================")
  print("Conversion Rate (" + currency_from + " to " + currency_to+"): ", str(round(rate,2)))
  print(str(amt)+" " + currency_from + " = "+str(round(conversion_result,2))+" "+ currency_to)
  print("====================================")
  print("")

answer="Y"
while answer.upper()=="Y":
  try:
    #clear screen for windows
    os.system('cls')
    #clear screen for linux or os x
    os.system('clear')
  except:
    pass
  proceed()
  answer=""
  while answer.upper()!="Y" and answer.upper()!="N":
    answer=input("Convert another(Y/N) ")
print("Thank you for using Spartacus Systems Currency Converter!")
