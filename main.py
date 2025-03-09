from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return self.title


@app.route('/')
def index():  # put application's code here
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


@app.route('/learn_more')
def learm_more():  # put application's code here
    return render_template('learn_more.html')


@app.route('/buy/<int:id>')
def item_buy(id):
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount":  int(Item.query.get(id).price)*100
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            title = request.form['title']
            price = request.form['price']
            isActive = True
            item = Item(title=title, price=price, isActive=isActive)
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)