from flask import render_template, flash, redirect, url_for, request
from app import app, db, email
from app.models import Grouporder, Orders
from app.forms import OrderForm, GroupOrderForm, ShareLinkForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/GroupOrdering', methods=['GET', 'POST'])
def index():
    form = GroupOrderForm()
    if form.validate_on_submit():
        if form.placeOrder.data:
            group_order = Grouporder(username=form.username.data, n_friends=form.n_friends.data)
            db.session.add(group_order)
            db.session.commit()
            sharing_link = url_for('group_order', gid=group_order.id)
            return redirect(url_for('shareLink', sharing_link=sharing_link, n_friends=form.n_friends.data))
        else:
            orders = Grouporder.query.filter_by(username=form.username.data)
            all_order_with_user = {}
            for order in orders:
                all_order_with_user[order.timestamp.strftime("%c")] = Orders.query.filter_by(groupId=order.id)
            sorted(all_order_with_user.items(), reverse=False)
            return render_template('checkOrder.html', orders=all_order_with_user)
    return render_template('index.html', form=form)


@app.route('/groupOrder/<int:gid>', methods=['GET', 'POST'])
def group_order(gid):
    form = OrderForm()
    if form.validate_on_submit():
        order = Orders(username=form.username.data,
                       groupId=gid,
                       orderName=form.orderName.data,
                       quantity=form.quantity.data,
                       size=form.size.data)
        db.session.add(order)
        db.session.commit()
        order_details = Grouporder.query.get(gid)
        total_friends_expected = order_details.n_friends
        order_till_now = Orders.query.filter_by(groupId=gid)
        if total_friends_expected == order_till_now.count():
            email_to_list = [order_details.username]
            email_from = 'poojatank999@gmail.com'
            email.send_email(email_from, email_to_list, "Order status ", render_template('returnStatus.html',
                                                                                         order=order_till_now))
        flash('Your order placed Successfully {}'.format(
            form.username.data))

        return redirect('/index')
    return render_template('orderForm.html', form=form)


@app.route('/shareLink', methods=['GET', 'POST'])
def shareLink():
    form = ShareLinkForm()
    n_friends= request.args.get('n_friends')
    sharing_link = (request.host_url)[:-1] + request.args.get('sharing_link')
    n_friends = int(n_friends)
    for i in range(n_friends):
        if not form.is_submitted():
            form.recipients_emails.append_entry()
    if form.validate_on_submit():
        email_from = form.users_email.data
        email_to_list = []
        for e in form.recipients_emails:
            email_to_list.append(e.data['email'])
            #flash(e.data['email'])

        #flash(email_to_list)

        email.send_email(email_from, email_to_list, sharing_link, render_template('shareMailBody.html',
                                                                                  sharing_link=sharing_link))

    return render_template('shareLink.html',
                           sharing_link=sharing_link,
                           form=form,
                           n_friends=n_friends)
