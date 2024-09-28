function ShowDataOnModal(data) {
    const ModalStenCilOrder = new bootstrap.Modal('#modal-order')
    let body = document.querySelector("#modalOrderTbody")
    let headers = ['type', 'status', 'thickness', 'side', 'size', 'quantity', 'file', 'request', 'address']
    document.querySelector("#TrackingCode").textContent = data["identifier"]

    headers.forEach(each => {
        let tr = document.createElement("tr")
        let thead = document.createElement("th")
        let td = document.createElement("td")
        let span = document.createElement("span")

        thead.textContent = each
        span.textContent = data[each] || "ندارد"

        td.appendChild(span)
        tr.appendChild(thead)
        tr.appendChild(td)
        body.appendChild(tr)
    })

    ModalStenCilOrder.show()
}


async function get_order_history_info(key) {
    let response = await fetch(`/user/order/stencils/api/order/stencil/?key=${key}`, {
        method: "GET"
    })
    let data = await response.json()

    if (response.status !== 200) {
        Swal.fire({
            icon: "warning",
            title: data.status,
            text: data.message,
            confirmButtonText: "باشه"
        })
    } else {
        ShowDataOnModal(data.data)
    }
}

async function ShowModalOrderInfo(key) {
    await get_order_history_info(key)
}