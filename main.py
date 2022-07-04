from flask import Flask, render_template, request, redirect, url_for
from os.path import join
from utils import insert_data, get_data, update_record

app = Flask(__name__)
app.config['DEBUG'] = True

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file_path = join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(uploaded_file_path)
            insert_data(uploaded_file_path)

        return redirect(url_for('index'))
    except Exception:
        return "Error while uploading File"


@app.route("/api/search/results", methods=['GET', 'POST'])
def get_products():
    try:
        data = get_data()
        return render_template('results.html', data=data)
    except Exception:
        return "This store_id is not present"


@app.route("/api/update/product/<store_id>", methods=['GET', 'POST'])
def update_product(store_id):
    try:
        if request.method == 'GET':
            data = get_data('store_id', store_id)
            return render_template('update_product.html', data=data)

        elif request.method == 'POST':
            sku = request.form['sku']
            prod_desc = request.form['prod_desc']

            price = request.form['price']
            order_date = request.form['order_date']

            data=update_record(store_id, sku, prod_desc, price, order_date)
            return data

    except Exception:
        return "This store_id is not present"


@app.route("/api/search/store_id/<store_id>", methods=['GET'])
def get_store_id(store_id):
    try:
        data = get_data('store_id', store_id)
        return render_template('results.html', data=data)
    except Exception:
        return "This store_id is not present"


@app.route("/api/search/SKU/<sku>", methods=['GET'])
def get_sku(sku):
    try:
        data = get_data('SKU', sku)
        return render_template('results.html', data=data)

    except Exception:
        return "This SKU is not present"


@app.route("/api/search/product/<product>", methods=['GET'])
def get_product(product):
    try:
        data = get_data('product_name', product)
        return render_template('results.html', data=data)
    except Exception:
        return "This Product is not present"


@app.route("/api/search/price/<price>", methods=['GET'])
def get_price(price):
    try:
        data = get_data('price', price)
        return render_template('results.html', data=data)
    except Exception:
        return "This Product is not present"


@app.route("/api/search/date/<order_date>", methods=['GET'])
def get_order_date(order_date):
    try:
        data = get_data('order_date', order_date)
        return render_template('results.html', data=data)
    except Exception:
        return "This Product is not present"


if __name__ == '__main__':
    app.run(port=5000)
