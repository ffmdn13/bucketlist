import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get('MONGODB_URI')
DB_NAME = os.environ.get('DB_NAME')

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bucket', methods = ['POST'])
def list_post():
    list_receive = request.form['list_data']
    count = db.bucketlist.count_documents({})
    num = count + 1

    doc = {
        'number': num,
        'list': list_receive,
        'done': 0
    }
    db.bucketlist.insert_one(doc)
    return jsonify({'msg': 'List saved!'})

@app.route('/bucket/done', methods = ['POST'])
def list_done():
    num_receive = request.form['num_give']
    db.bucketlist.update_one(
        {'number': int(num_receive)},
        {'$set': {'done': 1}}
    )

    return jsonify({'msg': 'Update done!'})

@app.route('/bucket/delete', methods = ['POST'])
def delete_list():
    num_receive = request.form['delete_num']
    db.bucketlist.delete_one({'number': int(num_receive)})

    return jsonify({'msg': 'List deleted!'})

@app.route('/bucket', methods = ['GET'])
def get_list():
    bucket_list = list(db.bucketlist.find({}, {'_id': False}))
    return jsonify({'data': bucket_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port = 5000, debug = True)