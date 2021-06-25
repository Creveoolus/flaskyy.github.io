from flask import Flask, redirect, url_for, render_template, request, session, flash
import time

app = Flask(__name__)
app.secret_key = "sex"

@app.route("/")
@app.route("/home")
def home():
	return render_template("index.html")

@app.route("/404")
@app.route("/<page>")
def notFound(page=None):
	if page is None:
		page = 404
	return render_template("404.html", page=page)

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		user = request.form["nn"]
		password = request.form["password"]
		session["user"] = user
		session["password"] = password

		flash(f"Successfuly logged in, {user}!", "info")
		return redirect(url_for("home"))
	else:
		if "user" in session:
			flash(f"Alredy logged in, {session['user']}!", "warning")
			return redirect(url_for("home"))

		return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
	if request.method == "POST":
		user = request.form["nn"]
		email = request.form["email"]
		password = request.form["password"]

		if len(user) < 3 or len(user) > 18:
			flash("Nickname must have 3-18 symbols!", "error")
			return redirect(url_for("register"))
		else:
			if len(password) < 8 or len(password) > 16:
				flash("Password must have 8-16 symbols!", "error")
				return redirect(url_for("register"))
			else:
				session["user"] = user
				session["email"] = email
				session["password"] = password

				flash(f"Successfuly registered, {user}!", "info")
				return redirect(url_for("home"))
	else:
		if "user" in session:
			flash(f"Alredy logged in, {session['user']}!", "warning")
			return redirect(url_for("home"))

		return render_template("register.html")

@app.route("/me")
def me():
	if "user" in session:
		user = session["user"]
		return render_template("user.html", usr=user)
	else:
		flash("Login, to see you'r user page!", "warning")
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	if "user" in session:
		user = session["user"]
		flash(f"Successfuly logged out, {user}!", "info")
	session.pop("user", None)
	return redirect(url_for("login"))

# @app.route("/admin")
# def admin():
# 	return redirect(url_for("home"))

if __name__ == '__main__':
	app.run(debug=True)