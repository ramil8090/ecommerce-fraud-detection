import requests

def http_request(input_data):
    url = 'http://localhost:9696/predict'
    return requests.post(url, json=input_data).json()

def process(input_data, expected_fraud):
    response = http_request(input_data=input_data)
    is_fraud = response['is_fraud']
    fraud_probability = response['fraud_probability']
    print(f'Expected fraud: {expected_fraud}')
    print(f'Actual fraud: {is_fraud}')
    print(f'Is fraud probability: {fraud_probability}')

# Test non-fraud
input_data = {
    "account_age_days":141,
    "total_transactions_user":47,
    "avg_amount_user":147.93,
    "amount":84.75,
    "country":"FR",
    "bin_country":"FR",
    "channel":"web",
    "merchant_category":"travel",
    "promo_used":0,
    "avs_match":1,
    "cvv_result":1,
    "three_ds_flag":1,
    "shipping_distance_km":370.95,
    "day":5,
    "month":1,
    "hour":4,
    "night_hours":1
}
process(input_data=input_data, expected_fraud=False)

print()

# Test fraud
input_data = {
    "account_age_days":30,
    "total_transactions_user":47,
    "avg_amount_user":147.93,
    "amount":84.75,
    "country":"FR",
    "bin_country":"US",
    "channel":"web",
    "merchant_category":"travel",
    "promo_used":1,
    "avs_match":0,
    "cvv_result":0,
    "three_ds_flag":0,
    "shipping_distance_km":1000.95,
    "day":5,
    "month":1,
    "hour":4,
    "night_hours":1
}
process(input_data=input_data, expected_fraud=True)