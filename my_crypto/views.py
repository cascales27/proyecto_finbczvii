import sqlite3
import requests
from flask.json import jsonify
from my_crypto import app
from my_crypto.dataaccess import DBmanager
from flask import jsonify, render_template, request, Response   #<-- modulos importados
from http import HTTPStatus
from datetime import datetime
from config import APICOINMARKET_KEY


# aqui se tiene que inicializar las monedas y las variables para el calculo de saldos
Todasmonedas = ['EUR', 'BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'BNB', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX']

dbManager = DBmanager(app.config.get('DATABASE')) # <-- la base de datos inicializada


queryEurFrom = "SELECT sum(cantidad_from) FROM movimientos WHERE moneda_from = 'EUR';"

queryEurTo = "SELECT sum(cantidad_to) FROM movimientos WHERE moneda_to = 'EUR';"

queryBtcFrom = "SELECT sum(cantidad_from) FROM movimientos WHERE moneda_from = 'BTC';"

queryBtcTo = "SELECT sum(cantidad_from) FROM movimientos WHERE moneda_from = 'BTC';"

queryEthFrom = "SELECT sum(cantidad_from) FROM movimientos WHERE moneda_from = 'ETH';"

queryEthTo = "SELECT sum(cantidad_to) FROM movimientos WHERE moneda_to = 'ETH';"

queryAdaFrom = "SELECT sum(cantidad_from) FROM movimientos WHERE moneda_from = 'ADA';"

queryAdaTo = "SELECT sum(cantidad_to) FROM movimientos WHERE moneda_to = 'ADA';"

queryTrxFrom = "SELECT sum(cantidad_from) FROM movimientos WHERE moneda_from = 'TRX';"

queryTrxTo = "SELECT sum(cantidad_to) FROM movimientos WHERE moneda_to = 'TRX';"



totalInv = queryEurFrom - queryEurTo
# aqui una funcion que calcule el saldo en diferentes monedas
def saldoCalculado():

    return



# aqui una funcion que calcule el saldo total


@app.route('/')
def listaMovimientos():   # ruta que devuelve el render template(lista de movimientos via html)
    return render_template('spa.html')


@app.route('/api/v1/movimientos')
def movimientosAPI():
    query = "SELECT * FROM movimientos ORDER BY date;"
    
    try:
        lista = dbManager.consultaMuchasSQL(query)
        print(lista)
        return jsonify({'status': 'success', 'movimientos': lista}) #esta es de kakebo, devuelve los movimientos que hay
    except sqlite3.Error as e:
        print("error", e)
        return jsonify({'status': 'fail', 'mensaje': str(e)})
    



# aqui tiene que haber otra ruta, una get con el id y otra post para que se pueda validar la fecha y la hora en el servidor.
@app.route('/api/v1/movimiento/<int:id>', methods=['GET'])
@app.route('/api/v1/movimiento', methods=['POST'])
def detalleMovimiento(id=None):

    try:
        if request.method in ('GET'):
            movimiento = dbManager.consultaUnaSQL("SELECT * FROM movimientos WHERE id = ?", [id])
        
            if movimiento:
                return jsonify({
                    "status": "success",
                    "data": movimiento
                })
            else:
                return jsonify({"status": "fail", "mensaje": "movimiento no encontrado"}), HTTPStatus.NOT_FOUND

        

        if request.method == 'POST':
            fechaHoraYDia = str(datetime.now())
            fechaHoy = fechaHoraYDia[:6]
            horaAhora = fechaHoraYDia[15:30]

            
    

            if request.json['moneda_from'] == request.json['moneda_to']:
                return jsonify({"status": "fail", "mensaje": "Las monedas deben de ser diferentes"}), HTTPStatus.OK

            if request.json['moneda_from'] != 'EUR':

              if queryBtcFrom < queryBtcTo:
                return jsonify({"status": "fail", "mensaje": "Saldo insuficiente"}), HTTPStatus.OK
              elif queryEthFrom < queryEthTo:
                return jsonify({"status": "fail", "mensaje": "Saldo insuficiente"}), HTTPStatus.OK
              elif queryAdaFrom < queryAdaTo:
                return jsonify({"status": "fail", "mensaje": "Saldo insuficiente"}), HTTPStatus.OK
              elif queryTrxFrom < queryTrxTo:
                return jsonify({"status": "fail", "mensaje": "Saldo insuficiente"}), HTTPStatus.OK
                #if #aqui tenemos que validar que hay saldo suficiente en cryptos para relizar la operación 

            dbManager.modificaTablaSQL("""
                INSERT INTO movimientos 
                       (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to)
                VALUES (:date, :time, :moneda_from, :cantidad_from, :moneda_to, :cantidad_to) 
                """, request.json)
            return jsonify({"status": "success", "moneda_from": request.json['moneda_from'], "moneda_to": request.json['moneda_to'], "mensaje": "registro creado"}), HTTPStatus.CREATED


    except sqlite3.Error as e:
        return jsonify({"status": "fail", "mensaje": "Error en base de datos: {}".format(e)}), HTTPStatus.BAD_REQUEST



# aqui otra ruta para que llame a la api de coin market, la primera con from, to y quantity y la segunda con from y to, preguntar a ramon.


@app.route('/api/v1/par/<_from>/<_to>/<quantity>')
@app.route('/api/v1/par/<_from>/<_to>')
def par(_from, _to, quantity = 1.0):
    url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={quantity}&symbol={_from}&convert={_to}&CMC_PRO_API_KEY={APICOINMARKET_KEY}"
    resultado = requests.get(url)
    return Response(resultado) 


# la ruta para el status, tiene que llamar a la funcion que se realiza arriba para calcular el saldo, posteriormente con un bucle(probablemente for)
#calcular el saldo, tambien tiene que llamar a la api de coin market y crear varias listas con las diferntes monedas, y devolver al final un json


@app.route('api/v1/status')
def statusINV():

    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert=EUR&CMC_PRO_API_KEY={}'

    try:
        #aqui utilizando la segunda funcion que se hace arriba, se monta un bucle o varios para poder calcular el status
        totalInv()


        print("****************")
        return jsonify({'status':'succsess'})

    except sqlite3.Error as e:
        print('error', e)
        return jsonify({'status': 'fail', 'mensaje': str(e)}), HTTPStatus.BAD_REQUEST