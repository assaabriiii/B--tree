from flask import Flask, redirect, url_for, request, render_template
from waitress import serve
from bplustree import BPlusTree
app = Flask(__name__)
import json


ttype = True # True for numeric, False for string


@app.route('/tree', methods = ['POST', 'GET'])
def tree_page():
    ins = ''
    d = ''
    if request.method == 'POST':
        ins = request.form['insert']
        d = request.form['delete']
        save_file_name = request.form['save']

        if str(ins) != '' and ins != None:
            if ttype:
                if ins.isdigit():
                    insert_key = int(ins)
                else:
                    return render_template('tree.html', tree_data=tree.getDictTree())
            else:
                insert_key = str(ins)

            if tree.search(insert_key) == None:
                tree.insert(insert_key, str(ins))

        if str(d) != '' and d != None:
            if ttype:
                if d.isdigit():
                    delete_key = int(d)
                else:
                    return render_template('tree.html', tree_data=tree.getDictTree())
            else:
                delete_key = str(d)

            if tree.search(delete_key) != None:
                print(str(d), tree.test_find(delete_key).pointers)
                tree.delete(delete_key, str(d))


        if str(save_file_name) != '' and save_file_name != None:
            with open(f'{save_file_name}.json', 'w') as file:
                json.dump(tree.getDictTree(), file, indent=4)

    return render_template('tree.html', tree_data=tree.getDictTree())

@app.route('/', methods = ['POST', 'GET'])
def index():
    global tree
    global ttype
    if request.method == 'POST':
        print("Submitted")
        tree_order = request.form['treeOrder']
        tree_type = request.form['treeType']
        if tree_order != None and tree_type != None:
            print("Tree is created")
            tree = BPlusTree(int(tree_order))
            print(tree.getDictTree())
            ttype = str(tree_type) == 'numeric'
            return redirect(url_for('tree_page'))

    return render_template('index.html')

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)
