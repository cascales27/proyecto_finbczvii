//aqui deberia de haber una const para poder en reciberespuestacm realizar el calculo. la creo dentro de la funcion
xhr = new XMLHttpRequest()
xhr1 = new XMLHttpRequest()


function recibeRespuesta() { //aqui debe haber una funcion que reciba la respuesta y cree el movimiento

    if (this.readyState === 4 && (this.status === 200 || this.status === 201)) {
        const respuesta = JSON.parse(this.responseText)

        if (respuesta.status !== 'success') {
            alert("Se ha producido un error en acceso a servidor " + respuesta.mensaje)
            return
        }

        alert(respuesta.mensaje)

        llamaApiMovimientos()
        llamaApiStatus()
    }
}

function muestraMovimientos() {
    if (this.readyState === 4 && this.status === 200) {
        const respuesta = JSON.parse(this.responseText) //heredado del kakebo,muestra los movimientos y los actualiza en una lista
        console.log(respuesta)
        if (respuesta.status != 'success') {
            alert("Se ha producido un error en la consulta de movimientos")
            return
        }

        const tbody = document.querySelector(".tabla-movimientos tbody")
        tbody.innerHTML = ""

        for (let i = 0; i < respuesta.movimientos.length; i++) {
            const movimiento = respuesta.movimientos[i]
            const fila = document.createElement("tr")

            const dentro = `
                <td>${movimiento.date}</td>
                <td>${movimiento.time}</td>
                <td>${movimiento.moneda_from}</td>
                <td>${movimiento.cantidad_from}</td>
                <td>${movimiento.moneda_to}</td>
                <td>${movimiento.cantidad_to}</td>
            `
            fila.innerHTML = dentro

            tbody.appendChild(fila)
        }
    }
}

//aqui debe haber una funcion de reciberespuestacm en la que se utilizara la constante que se ha creado arriba del todo


function recibeRespuestaCM() { //pendiente
    const movimiento = {}
    if (this.readyState === 4 && (this.status === 200 || this.status === 201)) {
        const respuesta = JSON.parse(this.responseText)

        if (respuesta.status.error_message !== null) {
            alert("Se ha producido un error en acceso a Coin Market: " + respuesta.status.error_message)
            return
        }

        movimiento.moneda_from = document.querySelector("#moneda_from").value

        movimiento.concepto = document.querySelector("#cantidad_from").value

        movimiento.categoria = document.querySelector("#moneda_to").value

        movimiento.cantidad_to = respuesta.data.quote[movimiento.moneda_to].price

        document.querySelector("#cantidad_to").setAttribute("placeholder", movimiento.cantidad_to)

    }
}

//aqui debe haber una funcion que reciba la respuesta y actualice resultados(status)
function detallaMovimientoStatus() {

    if (this.readyState === 4 && this.status === 200) {
        const respuesta = JSON.parse(this.responseText)

        if (respuesta.status !== 'success') {
            alert("se ha producido un error en acceso a servidor" + respuesta.mensaje)
            return
        }

        document.querySelector("#invertido").setAttribute("placeholder", respuesta.data.invertido)

        document.querySelector("#valores_actuales").setAttribute("placeholder", respuesta.data.valores_actuales)

        resultadoTot = respuesta.data.valores_actuales - respuesta.data.invertido
        document.querySelector("#resultado").setAttribute("placeholder", respuesta.data.resultadoTot)

        const tbody = document.querySelector(".tabla-saldos tbody")
        tbody.innerHTML = ""


        for (let i = 0; i < respuesta.data.lista_monedas.length; i++) {
            const fila = document.createElement("tr")

            const dentro = `
                <td>${respuesta.data.lista_monedas[i]}</td>
                <td>${respuesta.data.lista_saldo_from[i]}</td>
                <td>${respuesta.data.lista_saldo_to[i]}</td>
                <td>${respuesta.data.lista_saldo[i]} €</td>
            `
            fila.innerHTML = dentro

            tbody.appendChild(fila)

        }
    }

}

function llamaApiMovimientos() {
    xhr.open('GET', `http://localhost:5000/api/v1/movimientos`, true) // llama a la funcion de muestra movimientos con xhr para llamadas asincronas
    xhr.onload = muestraMovimientos
    xhr.send()
}



function llamaApiCoinmarket(evento) {
    evento.preventDefault() //esta funcion llama apicoinmarket y actua el xhr para llamadas asincronas
    const movimiento = {}
    movimiento.moneda_from = document.querySelector("#moneda_from").value
    movimiento.cantidad_from = document.querySelector("#cantidad_from").value
    movimiento.moneda_to = document.querySelector("#moneda_to").value

    xhr.open("GET", `http://localhost:5000/api/v1/par/${movimiento.moneda_from}/${movimiento.moneda_to}/${movimiento.cantidad_from}`, true)

    xhr.onload = muestraMovimientos
    xhr.send()

}


function llamaApiCreaMovimiento(evento) {
    evento.preventDefault() // esta funcion llama apicreamovimiento y con xhr actualiza la pantalla

    xhr.open("POST", `http://localhost:5000/api/v1/movimiento`, true)
    xhr.onload = recibeRespuestaCM

    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

    xhr.send(JSON.stringify(movimiento)) //<-- falta el valor dentro
}


function llamaApiStatus() {
    xhr1.open("GET", `http://localhost:5000/api/v1/status`, true)
    xhr1.onload = detallaMovimientoStatus //esta funcion llama apistatus y con xhr,en este caso difernte al anterior, actualiza la pantalla
    xhr1.send()
}



window.onload = function() {
    llamaApiMovimientos() //llama a la ventana con las dos ultimas llamadas

    llamaApiStatus()

    document.querySelector("#calcular") //captura el click al pulsar el boton calcular
        .addEventListener("click", llamaApiCoinmarket)

    document.querySelector("#ok") //captura el click al pulsar el boton ok
        .addEventListener("click", llamaApiCreaMovimiento)
}