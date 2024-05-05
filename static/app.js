async function send_post(url) {
    let data = {};
    // Send POST request
    let response = await fetch(url, {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data),
    });
}
async function increase_focus() {
    send_post("/increase_focus");
}
async function decrease_focus() {
    send_post("/decrease_focus");
}
async function set_auto_focus() {
    send_post("/set_auto_focus");
}
async function zero_focus() {
    send_post("/zero_focus");
}

