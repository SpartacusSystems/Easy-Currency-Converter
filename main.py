import os
import requests

# Don't share API key
my_secret = [YOUR-API-KEY-HERE]

# Clear screen function
def clear_screen():  
  try:
    #clear screen for windows
    os.system('cls')
    #clear screen for linux or os x
    os.system('clear')
  except:
    pass
  
# Get currency and rates.
def get_currency_and_rates(prompt):
  data = {"result": "error"}
  while data["result"] == "error":
    currency = input(prompt).upper()
    request_url = "https://v6.exchangerate-api.com/v6/" + my_secret + "/latest/" + currency

    # Get data from the web API
    response = requests.get(request_url)

    # Convert the JSON data object into a Python-friendly format.
    try:
      data = response.json()
    except:
      data = {
        "result": "error", 
        "error-type": "Invalid input"
      }
          
    if data["result"] == "error":
      print("")
      print("===> Error detected: ", data["error-type"])
      print("===> Please enter a valid currency...")
      print("")
    else:
      rates={}
      conv_rates = data["conversion_rates"]
      for r in conv_rates:
        rates[r] = conv_rates[r]
        
      #return tuple of currency and exchange rates
      return currency, rates

def proceed():
  # Get currency to convert from
  currency_from, rates = get_currency_and_rates("Enter currency to convert from: ")

  # Get currency to convert to and the exchange rate
  err=True
  while err:
    currency_to=input("Enter currency to convert to: ").upper()
    
    if currency_to == currency_from:
      print("")
      print("===> Error detected: Same currency")
      print("===> Please enter a different currency...")
      print("")
    elif currency_to in rates:
      err=False
      rate = rates[currency_to]
    else:
      print("")
      print("===> Error detected: Invalid currency")
      print("===> Please enter a valid currency...")
      print("")
  
  # Get amount to convert
  amt = 0
  while amt <= 0:
    amt = float(input("Enter " + currency_from + " amount to convert: "))
    if amt <= 0:
      print("")
      print("===> Error detected: amount is not greater than zero.")
      print("===> Please enter a positive number...")
      print("")
  
  conversion_result = amt*rate
  
  print("")
  print("====================================")
  print("Conversion Rate (" + 
        currency_from + 
        " to " + currency_to+"): ", 
        str(round(rate,2)))
  print(str(amt)+" " + 
        currency_from + " = "+
        str(round(conversion_result,2))+" "+ 
        currency_to)
  print("====================================")
  print("")

answer = "Y"
while answer.upper() == "Y":
  clear_screen()
  print("Easy Currency Converter v2.0")
  print("")
  proceed()
  answer = ""

  # Only accept Y or N
  while answer.upper() != "Y" and answer.upper() != "N":
    answer = input("Convert another(Y/N) ")

clear_screen()
print("Thank you for using Easy Currency Converter v2.0!")
