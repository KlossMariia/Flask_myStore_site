from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, default='', nullable=True)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self) -> str:
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST','GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        item = Item(title=title,price=price,description=description)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Some mistake occured'
    else:
        return render_template('create.html')

@app.route('/delete', methods=['POST','GET'])
def delete():
    if request.method == "POST":
        pk = int(request.form['pk'])
        item = Item(id=pk)
        try:
            Item.query.filter_by(id=pk).delete()
            db.session.commit()
            return redirect('/')
        except:
            return 'Some mistake occured'
    else:
        return render_template('delete.html')


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,secret_key='test')
    checkout = Checkout(api=api)
    data = {
        'currency': 'USD',
        'amount': str(item.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)



if __name__ == "__main__":
    app.run(debug=True)