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

function handle_create_response() {
	if (this.readyState == 4) {
		let result = JSON.parse(this.responseText);
		let status = result["status"];
		
		if (status != "done") {
			show_error(result["message"], result["status"]);
			return;
		}
		
		show_congrats();
	}
}

function do_create_request() {
	let handle = document.getElementById("handle").value;
	let password0 = document.getElementById("password0").value;
	let password1 = document.getElementById("password1").value;
	let email = document.getElementById("email").value;
	
	if (password0 != password1) {
		show_error("The passwords don't match!", "client:password_mismatch");
		return;
	}
	
	let data = {
		handle: handle,
		password: password0,
		email: email
	}
	
	request("POST", "/api/user/create", JSON.stringify(data), handle_create_response);
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
			para("<a href=\"/create\" in-app>Create an account</a>") +
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

function show_create() {
	var main_view = document.getElementById("app-main");
	
	main_view.innerHTML = div("login-main-div", "login-main", 
		div("login-panel", "panel",
			h1("Create an account") +
			para("Choose a handle name, password and add an email to create your account.") +
			div("login-panel-handle-0", "textbox-width-restrict", textbox("handle", "Handle")) +
			div("login-panel-handle-0", "textbox-width-restrict", password("password0", "Password")) +
			div("login-panel-handle-0", "textbox-width-restrict", password("password1", "Password (again)")) +
			div("login-panel-handle-0", "textbox-width-restrict", textbox("email", "Email")) +
			para("<a href=\"/login\" in-app>Already have an account?</a>") +
			"<div id=\"login-error\"></div><div class=\"login-dialogue-button-container\">" +
				"<div class=\"login-dialogue-button-container-left\">" +
					button("action-cancel-create", "Cancel", "window.history.back()", true) +
				"</div>" +
				"<div class=\"login-dialogue-button-container-right\">" +
					button("action-submit-create", "Create account", "do_create_request()") +
				"</div>" +
			"</div>"
		)
	);
}

function show_oops() {
	var main_view = document.getElementById("app-main");
	
	main_view.innerHTML = div("login-main-div", "login-main", div("login-panel", "panel", h1("Oops!") + para("It looks like you're lost! Maybe you want to <a href=\"/login\" in-app>log in</a> or <a href=\"/create\" in-app>create an account</a>?") + para("<button class=\"button secondary\" onclick=\"window.history.back()\">Go back</button>")));
}

function show_congrats() {
	var main_view = document.getElementById("app-main");
	
	main_view.innerHTML = div("login-main-div", "login-main", div("login-panel", "panel", h1("Dashboard") + para("The user dashboard is empty right now.") + para("<a href=\"/login\" in-app><button class=\"button secondary\">Log in</button></a>")));
}

function show_dash() {
	var main_view = document.getElementById("app-main");
	
	main_view.innerHTML = div("login-main-div", "login-main", div("login-panel", "panel", h1("Welcome!") + para("Your account has been created! You can now log in to it.")));
}

function switch_view(view) {
	switch (view) {
		case "login":
			show_login();
			break;
		case "create":
			show_create();
			break;
		case "dash":
			show_dash();
			break;
		default:
			show_oops();
			break;
	}
}

function update_view(new_url) {
	window.history.pushState(null, "", new_url); // Push new history
	switch_view(new_url.slice(1));
}

function on_link_clicked(e) {
	if (e.target.matches("[in-app]")) {
		e.preventDefault();
		let new_url = (new URL(e.target.href)).pathname;
		console.log(new_url);
		update_view(new_url);
	}
}

function setup_links() {
	document.body.addEventListener("click", on_link_clicked);
}

function setup_history() {
	window.addEventListener("popstate", (event) => {
		switch_view(location.pathname.slice(1));
	});
}

function main() {
	setup_links();
	setup_history();
	switch_view(location.pathname.slice(1));
}
