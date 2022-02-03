from flask import Flask, render_template, request, redirect, url_for

from forms import Insert

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret1234"

items = [
    {"id": 1, "todo_item": "john_test1", "status": "in progress"},
]


@app.route('/', methods=['GET', 'POST'])
def home():  # put application's code here
    return render_template('pages/home.html', items=items)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    form = Insert()
    if request.method == 'POST':
        item = {'id': form.id.data,
                'todo_item': form.todo_item.data,
                'status': form.status.data
                }
        items.append(item)
        return redirect(url_for('home'))

    return render_template('pages/insertform.html', form=form)


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    print(id)
    for item in items:
        if (item['id'] == int(id)):
            items.remove(item)
            break
    return redirect(url_for('home'))


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    form = Insert()
    if (request.method == 'GET'):
        item = [item for item in items if (item['id'] == int(id))][0]
        print(item)
        form.id.data = item['id']
        form.todo_item.data = item['todo_item']
        form.status.data = item['status']
        return render_template('pages/editform.html', form=form, item=item)
    else:
        for item in items:
            if (item['id'] == int(id)):
                item['id'] = form.id.data
                item['todo_item'] = form.todo_item.data
                item['status'] = form.status.data
                break
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
