from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import uuid
cluster = MongoClient(
    "mongodb+srv://test:test@cluster0.lghkz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["test"]
collection = db["test"]
app = Flask(__name__, static_url_path='/static')
print(app.static_url_path)


@app.route("/")
def index():
    paragraphs = [
        'section 1',
        'section 2',
        'section 3'
    ]
    return render_template('thebalvenie-index.html', title='home', data=paragraphs)


@app.route("/our-whisky-range-product")
def our_whisky_range_product():
    return render_template('our-whisky-range-product.html', title='home')


@app.route("/our-whisky-range")
def our_whisky_range():
    return render_template('our-whisky-range.html', title='home')


@app.route("/our-whisky-range-2")
def our_whisky_range_product_2():
    return render_template('our-whisky-range-2.html', title='home')


@app.route("/our-five-rare-crafts")
def our_five_rare_crafts():
    return render_template('our-five-rare-crafts.html', title='home')


@app.route("/other-crafts")
def other_crafts():
    return render_template('other-crafts.html', title='home')


@app.route("/our-craftsmen")
def our_craftsmen():
    return render_template('our-craftsmen.html', title='home')


@app.route("/the-distillery-story")
def the_distillery_story():
    return render_template('the-distillery-story.html', title='home')


@app.route("/ambassadors")
def ambassadors():
    return render_template('ambassadors.html', title='home')


@app.route("/warehouse-24")
def warehouse_24():
    return render_template('warehouse-24.html', title='home')


@app.route("/dcs3")
def dcs3():
    return render_template('dcs3.html', title='home')


@app.route("/create", methods=['POST'])
def create():
    product_tran_dict = {1: "百富雙桶12年單一麥芽威士忌", 2: "百富雙桶17年單一麥芽威士忌", 3: "百富加勒比海蘭姆桶14年單一麥芽威士忌",
                         4: "百富波特桶21年單一麥芽威士忌", 5: "百富30年單一麥芽威士忌", 6: "百富40年單一麥芽威士忌", 7: "百富17年泥媒桶單一麥芽威士忌", 8: "百富三桶12年單一麥芽威士忌",
                         9: "百富25年單一酒桶單一麥芽威士忌", 10: "百富TUN 1509 號桶 第一批次單一麥芽威士忌",
                         11: "百富TUN 1509 號桶 第二批次單一麥芽威士忌", 12: "百富12年單一酒桶單一麥芽威士忌", 13: "百富50年珍稀酒款 4567號桶",
                         14: "百富21年馬德拉桶單一麥芽威士忌", 15: "百富三桶16年單一麥芽威士忌",
                         16: "百富TUN 1509 號桶 第三批次單一麥芽威士忌", 17: "百富TUN 1858號桶 第四批次單一麥芽威士忌",
                         18: "百富TUN 1858號桶 第五批次單一麥芽威士忌", 19: "百富15年單一雪莉桶單一麥芽威士忌",
                         20: "百富50年珍稀酒款 4570號桶"}
    datas = request.get_json()
    order_id = str(uuid.uuid4())
    print(datas)
    for data in datas['post_datas']:
        collection.insert_one({'_id': str(uuid.uuid4()),
                               'order_id': order_id, 'product_id': data['id'],
                               'product_name': product_tran_dict[data['id']],
                               'total_count': data['count']})
    print(datas)
    # return jsonify({'message': '購買數量{0} 成功 訂單號碼為{1}'.format(datas['total_count'], order_id)})
    return jsonify({'message': '購買數量 {0} 成功 訂單編號為{1}'.format(data['count'], order_id)})


@ app.route("/get_detail_page", methods=['GET'])
def get_detail_page():
    order_id = request.args.get('order_id')
    print(order_id)
    datas = collection.find(
        {'order_id': order_id})
    final_datas = {}
    for data in collection.find():
        final_datas = data
        print(final_datas)

    return render_template('test.html', title='test', datas=final_datas)


@ app.route("/get_detail", methods=['GET'])
def get_detail():
    params = request.form

    datas = collection.find(
        {'order_id': request.form.get('order_id')})
    final_datas = {}
    for data in collection.find():
        final_datas = data
        print(final_datas)

    return jsonify({'message': '讀取產品資料成功', 'datas': final_datas})


@ app.route("/delete", methods=['POST'])
def delete():
    params = request.form
    print(params)
    datas = collection.delete_one(
        {'order_id': request.form.get('order_id')})
    final_datas = {}
    print(datas.deleted_count)
    return jsonify({'message': '刪除訂單成功', 'datas': final_datas})


@ app.route("/update", methods=['POST'])
def update():
    params = request.form
    print(params)
    # datas = collection.update_one(
    #     {'order_id': request.form.get('order_id')},
    #     {'total_count': request.form.get({'$set': {'total_count': 999}})})

    datas = collection.update_one(
        {'order_id': request.form.get('order_id')},
        {'$set': {'total_count': request.form.get('total_count')}})

    final_datas = {}

    print(final_datas)
    return jsonify({'message': '訂單更改成功', 'datas': final_datas})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
