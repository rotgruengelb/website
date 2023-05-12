from flask import render_template

def custom_abort(status_code):
    if status_code is not None:
        return render_template(f"errors/{status_code}.html"), int(status_code)
    else:
        return render_template("errors/404.html"), 404