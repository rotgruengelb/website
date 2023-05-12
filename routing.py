import tomllib
from flask import abort, redirect, send_file
import custom_abort


def nav_entry(app, website_dir):
    @app.route("/<path:continent>/")
    @app.route("/<path:continent>/<path:street>")
    def _(continent, street=None):
        street_info = understand_map(grab_map(website_dir), (continent, street))
        if street_info == None:
            abort(404)
        else:
            return walk_street(street_info, website_dir)


def grab_map(website_dir):
    with open(f"{website_dir}/routing/map.toml", "rb") as f:
        out = tomllib.load(f)
        print(out)
    f.close()
    return out


def understand_map(map_, destination):
    continent = destination[0]
    if street != None: street = destination[1]
    else: street = "cd"
    return map_.get(continent, {}).get(street)


def walk_street(street_info, website_dir):
    try:
        street_type = street_info[0]
        if street_type == "REDIRECT":
            url = street_info[1]
            if url.startswith("http://") or url.startswith("https://"):
                return redirect(url, 301)
            else:
                redirect(f"https://{url}", 301)
        if street_type == "FILE":
            path = street_info[1]
            if path.startswith("~"):
                return send_file(f"{website_dir}/{path[2:]}", 200)
            else:
                return send_file(path, 200)
        if street_type == "DOWNLOAD":
            path = street_info[1]
            if path.startswith("~"):
                return send_file(f"{website_dir}/{path[2:]}", as_attachment=True), 200
            else:
                return send_file(path, as_attachment=True), 200
        if street_type == "ERROR_CODE":
            code = str(street_info[1])
            if code.startswith("9"):
                return custom_abort.abort(code)
            else:
                return abort(int(code))
    except:
        return abort(500)
