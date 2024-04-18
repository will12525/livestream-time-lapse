async function increase_focus() {
    var url = "/increase_focus";
    let data = {};
    // Send POST request
    let response = await fetch(url, {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data),
    });
}
async function decrease_focus() {
    var url = "/decrease_focus";
    let data = {};
    // Send POST request
    let response = await fetch(url, {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data),
    });
}
async function set_auto_focus() {
    var url = "/set_auto_focus";
    let data = {};
    // Send POST request
    let response = await fetch(url, {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data),
    });
}

