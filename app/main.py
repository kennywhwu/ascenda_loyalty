from flask import Flask, request, jsonify
from app.merge_utils import merge_hotels
from app.adapters.acme_adapter import AcmeAdapter
from app.adapters.patagonia_adapter import PatagoniaAdapter
from app.adapters.paperflies_adapter import PaperfliesAdapter

app = Flask(__name__)

@app.route('/hotels', methods=['GET'])
def get_hotels():
    destination = int(request.args.get('destination'))
    hotel_ids = request.args.getlist('hotels')

    suppliers = {
        "acme": AcmeAdapter().fetch_data(),
        "patagonia": PatagoniaAdapter().fetch_data(),
        "paperflies": PaperfliesAdapter().fetch_data(),
    }

    merged_hotels = merge_hotels(suppliers, destination, hotel_ids)
    return jsonify(merged_hotels)

if __name__ == '__main__':
    app.run(debug=True)
