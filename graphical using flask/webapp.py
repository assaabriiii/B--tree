from flask import Flask, redirect, url_for, request, render_template
from waitress import serve
from main import BPlusTree
app = Flask(__name__)

# Default tree
# tree = BPlusTree(4)
# tree.insert(4)
# print(tree.getDictTree())
ttype = True # True for numeric, False for string

@app.route('/tree', methods = ['POST', 'GET'])
def tree_page():
    ins = ''
    d = ''
    if request.method == 'POST':
        ins = request.form['insert']
        d = request.form['delete']
        print("debug1")
        if str(ins) != '' and ins != None:
            print("debug2")
            if ttype:
                print("debug3")
                if ins.isdigit():
                    print("debug4")
                    insert_key = int(ins)
                else:
                    print("debug5")
                    print(tree.getDictTree())
                    return render_template('tree.html', tree_data=tree.getDictTree())
            else:
                print("debug6")
                insert_key = str(ins)

            # Process input submission
            if tree._search(insert_key) == None:
                print("debug7")
                print(f"inserting {insert_key} and {int(ins)}")
                tree.insert(int(ins))
                # tree.insert(insert_key, str(ins))

        if str(d) != '' and d != None:
            print("debug8")
            if ttype:
                print("debug9")
                if d.isdigit():
                    print("debug10")
                    delete_key = int(d)
                else:
                    print("debug11")
                    print(tree.getDictTree())
                    return render_template('tree.html', tree_data=tree.getDictTree())
            else:
                print("debug12")
                delete_key = str(d)

            # TODO: Implement delete
            # if tree.search(delete_key) != None:
                # print(str(d), tree.test_find(delete_key).pointers)

                # tree.delete(delete_key, str(d))
    print("debug13")
    print(tree.getDictTree())
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
    #app.run(debug = True)
    serve(app, host="0.0.0.0", port=8000)
