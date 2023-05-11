from flask import render_template

def abort(code):
    if code != None:
        return render_template(f'errors/{code}.html'), int(code)
    else:
        return render_template(f'errors/404.html'),404