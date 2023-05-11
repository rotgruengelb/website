from flask import redirect, send_file, abort, render_template, make_response
import custom_abort


def errors(app):

    @app.route("/404")
    def f_404():
        return abort(404)
    @app.errorhandler(404)
    def _404(e):
        return render_template(f'errors/404.html'),404
    
    @app.route("/500")
    def f_500():
        return abort(500)
    @app.errorhandler(500)
    def _500(e):
        return render_template(f'errors/500.html'),500

    @app.route("/410")
    def f_410():
        return abort(410)
    @app.errorhandler(410)
    def _410(e):
        return render_template(f'errors/410.html'),410
    
    @app.route("/900")
    def f_900():
        return custom_abort.abort(900)

    @app.route("/910")
    def f_910():
        return custom_abort.abort(910)

    @app.route("/920")
    def f_920():
        return custom_abort.abort(920)


def bots(app, website_dir):

    @app.route('/robots.txt', methods=['GET'])
    def robots_txt():
        try: 
            response = make_response(open(f'{website_dir}/static/robots.txt').read())
            response.headers["Content-type"] = "text/plain"
        except:
            response = make_response(abort(404))
        return response

    @app.route('/sitemap.xml', methods=['GET'])
    def sitemap_xml():
        try: 
            response = make_response(open(f'{website_dir}/static/sitemap.xml').read())
            response.headers["Content-type"] = "text/plain"
        except:
            response = make_response(abort(404))
        return response
