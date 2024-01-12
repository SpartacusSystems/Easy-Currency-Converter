import os
import sys
import requests

# Don't share API key
my_secret = [YOUR-API-KEY-HERE]

# Global variable which will contain the valid currency codes
valid_codes=[]

# Clear screen function
def clear_screen():  
  try:
    #clear screen for windows
    os.system('cls')
    #clear screen for linux or os x
    os.system('clear')
  except:
    pass
    
# Function to get the supported currency codes
def get_valid_codes():
  global valid_codes
  request_url = "https://v6.exchangerate-api.com/v6/" + my_secret + "/codes"  
  try:
    # Get data from the web API
    response = requests.get(request_url)
    # Convert the JSON data object into a Python-friendly format.
    data = response.json()
  except:
    # Possible server / internet connection issue
    print("")
    print("===> Error detected: Unable to connect to server")
    print("===> Exiting the program...")
    print("")
    sys.exit("Thank you for using Easy Currency Converter v3.0!")

  # Store the codes in the global variable
  for code in data["supported_codes"]:
    valid_codes.append(code[0])
  
# Function to get the conversion rates for a particular currency.
def get_rates(currency):
  request_url = "https://v6.exchangerate-api.com/v6/" + my_secret + "/latest/" + currency
  
  # Get data from the web API
  response = requests.get(request_url)
  
  # Convert the JSON data object into a Python-friendly format.
  data = response.json()

  # Extract the conversion rates from the data object and save it to a dictionary
  rates = {}
  conv_rates = data["conversion_rates"]
  for r in conv_rates:
    rates[r] = conv_rates[r]

  # Return the extracted rates dictionary
  return rates

# Function to get a valid currency code; the check variable is for checking for duplicate currency codes
def get_currency(prompt, check=""):
  currency = ""
  err = True
  while err:
    # Get input from user
    currency = input(prompt).upper()

    # Check if user input is valid
    if currency == check:
      # User entered the same currency as the check variable
      print("")
      print("===> Error detected: Same currency")
      print("===> Please enter a different currency...")
      print("")
    elif currency in valid_codes:
      # User entered a valid currency code
      err = False
    else:
      # User entered an invalid currency code
      print("")
      print("===> Error detected: Invalid currency")
      print("===> Please enter a valid currency...")
      print("")
      
  return currency
  
# This function is the heart of the program
def proceed():
  # Get currency to convert from
  currency_from = get_currency("Enter currency to convert from: ")

  # Get currency to convert to
  currency_to = get_currency("Enter currency to convert to: ", currency_from)
  
  # Get amount to convert
  # Do not allow user to enter 0 or a negative amount
  amt = 0
  while amt <= 0:
    amt = float(input("Enter " + currency_from + " amount to convert: "))
    if amt <= 0:
      print("")
      print("===> Error detected: amount is not greater than zero.")
      print("===> Please enter a positive number...")
      print("")

  # Get the conversion rates
  rates = get_rates(currency_from)

  # Get the conversion rate for the currency pair
  rate = rates[currency_to]

  # Calculate the converted amount
  conversion_result = amt*rate
  
  print("")
  print("====================================")

  # Output the conversion rate
  print("Conversion Rate (" + 
        currency_from + 
        " to " + currency_to+"): ", 
        str(round(rate,2)))

  # Output the conversion result
  print(str(amt)+" " + 
        currency_from + " = "+
        str(round(conversion_result,2))+" "+ 
        currency_to)
  print("====================================")
  print("")

# Main
# Get list of valid currency codes
get_valid_codes()
answer = "Y"

# Run the program until the user enters "N"
while answer.upper() == "Y":
  clear_screen()
  print("Easy Currency Converter v3.0")
  print("")
  proceed()
  answer = ""

  # Only accept Y or N
  while answer.upper() != "Y" and answer.upper() != "N":
    answer = input("Convert another(Y/N) ")

# Clear the screen and send a goodbye greeting before exiting
clear_screen()
print("Thank you for using Easy Currency Converter v3.0!")
