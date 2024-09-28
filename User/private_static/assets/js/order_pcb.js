async function setup(url){
    validateForm();
    await watch_keyboard_pressed(url);
}


function watch_keyboard_pressed() { // watch keyboard and validate it
    inputs = getinputs();
    inputs.forEach(each => {
        each.addEventListener("keyup", async e => {
            let is_form_valid = validateForm();
            if (!is_form_valid) {
                document.querySelector("#Submit").disabled = true;
            }
            if (is_form_valid){
                await form_valid_get_price(url);
            }
        })
    })
    inputs.forEach(each => {
        each.addEventListener("change", async e => {
            let is_form_valid = validateForm();
            if (!is_form_valid) {
                document.querySelector("#Submit").disabled = true;
            }
            if (is_form_valid){
                await form_valid_get_price(url);
            }
        })
    })
}

async function form_valid_get_price(url){
    document.querySelector("#Submit").disabled = true;
    const form = createFormData(getinputs());
    let response = await push_data(data=form, url=url);
    if (response.code == 200){
        show_price_and_day(price=response.data.price, day=response.data.day, message=response.data.message)
        document.querySelector("#Submit").disabled = false;
    }else{
        document.querySelector("#Submit").disabled = true;
        show_price_and_day(price="0", day="0", message=html_error_parser(response.data.message))
    }
}
setup(url)

