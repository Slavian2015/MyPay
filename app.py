from flask import Flask, request, render_template, redirect
from models import db, BookModel
import os
import logging
import helper_functions as hf

app = Flask(__name__)


data_dir = "/data"

logging.basicConfig(filename=data_dir + "my_flask_logs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

database_file = "sqlite:///{}".format(os.path.join(data_dir, "data.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()
    logger.info("DB table is created")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        data = request.form.to_dict()
        if data['currency'] == "EUR":
            new_payment = BookModel(amount=data['amount'], currency=data['currency'], description=data['description'])
            db.session.add(new_payment)
            db.session.commit()

            new_data = new_payment.json()
            logger.info(f"Added new order: Amount ({new_data['amount']}), "
                        f"Currency ({new_data['amount']}), "
                        f"Created_at ({new_data['created_at']}), "
                        f"Description ({new_data['amount']}), "
                        f"shop_order_id ({new_data['amount']})")

            new_data['sign'] = hf.my_pay(amount=new_data['amount'], shop_order_id=new_data['shop_order_id'])
            return render_template("direct_pay.html", data=data)
        elif data['currency'] == "USD":
            new_payment = BookModel(amount=data['amount'], currency=data['currency'], description=data['description'])
            db.session.add(new_payment)
            db.session.commit()

            new_data = new_payment.json()

            logger.info(f"Added new order: Amount ({new_data['amount']}), "
                        f"Currency ({new_data['amount']}), "
                        f"Created_at ({new_data['created_at']}), "
                        f"Description ({new_data['amount']}), "
                        f"shop_order_id ({new_data['amount']})")

            reponse = hf.piastrix_request(amount=new_data['amount'], shop_order_id=new_data['shop_order_id'])
            r = reponse.status_code
            if r == 200:
                new_url = reponse.json()
                if new_url['error_code'] == 0:
                    return redirect(new_url['data']['url'])
                else:
                    logger.error(f"Error: {new_url}")
                    return render_template("error_page.html", data=new_url)
            else:
                logger.error(f"Error: {reponse.text}")
                return render_template("error_page.html", data=reponse.text)
        elif data['currency'] == "RUB":
            new_payment = BookModel(amount=data['amount'], currency=data['currency'], description=data['description'])
            db.session.add(new_payment)
            db.session.commit()

            new_data = new_payment.json()

            logger.info(f"Added new order: Amount ({new_data['amount']}), "
                        f"Currency ({new_data['amount']}), "
                        f"Created_at ({new_data['created_at']}), "
                        f"Description ({new_data['amount']}), "
                        f"shop_order_id ({new_data['amount']})")

            reponse = hf.my_invoice(amount=new_data['amount'], shop_order_id=new_data['shop_order_id'])
            r = reponse.status_code

            if r == 200:
                new_url = reponse.json()
                if new_url['error_code'] == 0:
                    return render_template("invoice_pay.html", data=new_url)
                else:
                    logger.error(f"Error: {new_url}")
                    return render_template("error_page.html", data=new_url)
            else:
                logger.error(f"Error: {reponse.text}")
                return render_template("error_page.html", data=reponse.text)
        else:
            return render_template("home.html")
    return render_template("home.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=False, port=port)


# sudo docker image build -t my-pay .
# sudo docker run -p 5000:5000 -d my-pay

# sudo docker run −it 357c08fd8e472c8057468b8ab819ace00823809f33f987fb179bf11abd52cb91 bash


# heroku container:push web --app mypaysys
# sudo heroku container:release web --app mypaysys