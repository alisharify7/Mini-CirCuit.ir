async function push_data(data, url=null) {
    url = url || form.action
    let response = await fetch(url, {
        method: "post",
        body: data,
    })
    let responseJson = await response.json()
    return {data: responseJson, code: response.status}
}

function createFormData(htmlElements) {
    const formData = new FormData();
    htmlElements.forEach(each => {
        const name = each.name;
        const value = each.value;
        if (name && value) {
            formData.append(name, value);
        }
    })
    return formData;
}

function num_eng2persian(m) {
    const mapper = {
        9: "۹",
        8: "۸",
        7: "۷",
        6: "۶",
        5: "۵",
        4: "۴",
        3: "۳",
        2: "۲",
        1: "۱",
        0: "۰"
    };
    let p = "";
    m = m.split("").forEach(each => {
        if (each in mapper) {
            p += mapper[each]
        } else {
            p += each
        }
    })
    return p
}

function hasValue(input) {
    if (input.type === "checkbox" && input.id !== "attachment-file") {
        return input.checked;
    }
    else if (input.type.toLowerCase().toLowerCase() !== "file") {
        return new Boolean(input.value.trim()).valueOf();
    }
}

function addClass(input, className) {
    if (!input.classList.contains(className)) {
        input.classList.add(className);
    }
}

function removeClass(input, className) {
    if (input.classList.contains(className)) {
        input.classList.remove(className);
    }
}

function getinputs(hidden=false) {
    let inputs = form.querySelectorAll("input, select");
    let queue = [];
    inputs.forEach(each => {
        if (each.type !== "submit" && each.type != "file" && each.id !== "attachment-file") {
            if(each.type == "hidden" && hidden){
                queue.push(each)
            }else{
            queue.push(each)
            }
        }
    })
    return queue
}

function validateForm() {
    let allValid = true;
    let inputs = getinputs();

    for (const input of inputs) {
        if (hasValue(input)) {
            addClass(input, "is-valid");
            removeClass(input, "is-invalid");
        } else {
            allValid = false;
            addClass(input, "is-invalid");
            removeClass(input, "is-valid");
        }
    }
    return allValid
}

function watch_keyboard_and_validateForm() { // watch keyboard and validate it
    inputs = getinputs();
    inputs.forEach(each => {
        each.addEventListener("keyup", e => {
            validateForm();
        })
    })
    inputs.forEach(each => {
        each.addEventListener("change", e => {
            validateForm();
        })
    })
}

function html_error_parser(e) {
    let lis = ""
    Object.entries(e).forEach(each => {
        lis += `<li>${each[0]}: ${each[1]}</li>`
    })
    let temp = `
        <div class="border-top border-primary persian-font pt-3">
        <p class="text-center">خطایی برای محاسبه قیمت رخ داد. لطفا بعدا امتحان کنید</p>
            <ul class="list-unstyled" dir=ltr>
                ${lis}
            </ul>
        </div>`;
    return temp
}

function show_price_and_day(price, day, message=null) {
    const container = document.querySelector(".price-result-container");
    const price_handler = document.querySelector(".price_handler");
    const day_handler = document.querySelector(".day_handler");
    price_handler.textContent = `هزینه تقریبی: ${num_eng2persian(price.toString())} می باشد`;
    day_handler.textContent = `زمان تقریبی تحویل سفارش ${num_eng2persian(day.toString())} روز کاری می باشد.`;
    const message_container = document.querySelector(".price-result-container .message");
    message_container.innerHTML = message || "";

    removeClass(container, "d-none")
}
