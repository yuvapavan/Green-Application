import stripe
from flask import *
import requests
from flask import jsonify

app = Flask(__name__)

stripe_keys = {
  'secret_key': 'sk_live_eNfkQJRfFEd9Jkc13aHEIncb',
  'publishable_key': 'pk_live_jCH7egbWIZJqWz8bI4zvPS9s'
}

stripe.api_key = stripe_keys['secret_key']





# @app.route('/')
# def index():
#     return json.dumps({key=stripe_keys['publishable_key']}) 

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='kurapatiyuva.pavan@gmail.com',
        source=request.args.get('stripeToken')
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return json.dumps({'amount':amount})



@app.route('/run_post')
def run_post():
    url = "http://127.0.0.1:5000/stripes"
    data = {'stripeAmount': '199', 'stripeCurrency': 'USD', 'stripeToken': '122', 'stripeDescription': 'Test post'}
    headers = {'Content-Type' : 'application/json'}
    data=json.dumps(data)
    r = requests.post(url,data,headers=headers)

    #return json.dumps(r.json(), indent=4)
    return r.text


@app.route('/stripes', methods=["POST"])
def stripeTest():

    if request.method == "POST":
        json_dict = request.get_json()

        stripeAmount = json_dict['stripeAmount']
        stripeCurrency = json_dict['stripeCurrency']
        stripeToken = json_dict['stripeToken']
        stripeDescription = json_dict['stripeDescription']


        data = {'stripeAmountRet': stripeAmount, 'stripeCurrencyRet': stripeCurrency, 'stripeTokenRet': stripeToken, 'stripeDescriptionRet': stripeDescription}
        return jsonify(data)
    else:

        return json.dumps({"data":"Error"})

if __name__ == '__main__':
    app.run(debug=True,threaded=True)