/**
 * HTML elements - should probably use the DOM or a better UI creator more.
 */

function div(id, cls, content) {
	return "<div id=\"" + id + "\" class=\"" + cls + "\">" + content + "</div>";
}

function h1(text) {
	return "<h1>" + text + "</h1>";
}

function para(text) {
	return "<p>" + text + "</p>";
}

function textbox_typed(type, id, title) {
	return "<div class=\"textbox-label\"><p><b>" + title + "</b></p><p><div class=\"textbox-outer\"><input id=\"" + id + "\" class=\"textbox\" name=\"" + id + "\" type=\"" + type + "\" placeholder=\"" + title + "\"></div></p></div>";
}

function textbox(id, title) {
	return textbox_typed("text", id, title);
}

function password(id, title) {
	return textbox_typed("password", id, title);
}

function button(id, text, onclick, sec = false) {
	return "<button class=\"button" + (sec ? " secondary" : "") + "\" id=\"" + id + "\" type=\"button\" onclick=\"" + onclick + "\">" + text + "<button>";
}

/**
 * Utilities
 */

function request(method, url, body, handler) {
	let xhr = new XMLHttpRequest();
	xhr.onreadystatechange = handler;
	xhr.open(method, url);
	xhr.send(body);
}

/**
 * Login
 */

function show_error(string, status) {
	let e = document.getElementById("login-error");
	e.innerHTML = "<p class=\"error\">" + string + " (Status string " + status + ")</p>";
}

function handle_login_response() {
	if (this.readyState == 4) {
		let result = JSON.parse(this.responseText);
		console.log(result);
		let status = result["status"];
		
		if (status != "done") {
			show_error(result["message"], result["status"]);
			return;
		}
		
		show_error(this.responseText, "done");
	}
}

function do_login_request() {
	let data = {
		handle: document.getElementById("handle").value,
		password: document.getElementById("password").value,
		areas: []
	}
	
	request("POST", "/api/user/login", JSON.stringify(data), handle_login_response);
}

/**
 * User interface
 */

function show_login() {
	var main_view = document.getElementById("app-main");
	
	main_view.innerHTML = div("login-main-div", "login-main", 
		div("login-panel", "panel",
			h1("Log in") +
			para("Enter your handle and password to continue.") +
			div("login-panel-handle-0", "textbox-width-restrict", textbox("handle", "Handle")) +
			div("login-panel-handle-0", "textbox-width-restrict", password("password", "Password")) +
			para("<a href=\"/login\">Create an account</a>") +
			"<div id=\"login-error\"></div><div class=\"login-dialogue-button-container\">" +
				"<div class=\"login-dialogue-button-container-left\">" +
					button("action-cancel-login", "Cancel", "window.history.back()", true) +
				"</div>" +
				"<div class=\"login-dialogue-button-container-right\">" +
					button("action-submit-login", "Log in", "do_login_request()") +
				"</div>" +
			"</div>"
		)
	);
}

function main() {
	show_login();
}
