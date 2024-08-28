from datetime import datetime

from cloudinary import uploader

from app import app, db, dao, login as app_login
from flask import render_template, request, redirect, session, flash


@app_login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)
    return None;


@app.route('/')
def index():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/select-flight', methods=['get', 'post'])
def select_flight():
    try:
        from_loc = request.args.get('from-location')
        to_loc = request.args.get('to-location')
        if not from_loc:
            raise Exception('Vui lòng chọn địa điểm khởi hành')
        if not to_loc:
            raise Exception('Vui lòng chọn địa điểm đến')

        quantity = request.args.get('quantity')
        flight_date = request.args.get('flight-date')
        flight_date = flight_date if flight_date != '' else None

        if flight_date and datetime.strptime(flight_date, "%Y-%m-%d") <= datetime.now():
            raise Exception('Ngày đi phải sau ngày hiện tại!!!')

        from_code = dao.get_airport_id(from_loc)
        to_code = dao.get_airport_id(to_loc)

        order = session.get('order', {})
        if session.get('customers'):
            del session['customers']

        order['from-code'] = from_code
        order['from'] = from_loc
        order['to-code'] = to_code
        order['to'] = to_loc
        order['quantity'] = quantity
        order['flight_date'] = flight_date

        session['order'] = order
        flights = dao.search_flight(from_code, to_code, flight_date)
        flight = dao.get_flight_by_id(request.args.get('flight'))
        ticket_class = dao.get_ticket_class_by_id(request.args.get('ticket-class'))

        if flights == []:
            raise Exception('Không tồn tại chuyến bay nào phù hợp!!!')

        global terms
        terms = None
        if flight:
            terms = dao.get_terms(flight.id)
        if flight and ticket_class:
            print(utils.check_date(datetime.now(), flight.gio_bay), dao.get_regulation_value(
                RegulationEnum.ORDER_TIME.value))
            if utils.check_date(datetime.now(), flight.gio_bay) <= dao.get_regulation_value(
                    RegulationEnum.ORDER_TIME.value):

                raise Exception('Ngoài thời gian cho phép đặt vé!!')
            session['order']['flight'] = flight.id
            session['order']['ticket-class'] = ticket_class.id

        return render_template('select-flight.html',
                               flight_list=flights, flight=flight, ticket_class=ticket_class, terms=terms)
    except Exception as e:
        flash(str(e.args[0]), 'error')
        print(e)
        return redirect(utils.get_prev_url())

