import tomllib
from flask import redirect, send_file, abort
import custom_abort

def nav_entry(app, website_dir):
    @app.route("/<path:continent>/")
    @app.route("/<path:continent>/<path:street>")
    def _(continent, street = None):
        street_info = understand_map(grab_map(website_dir), (continent, street))
        if street_info == None:
            abort(404)
        else: return walk_street(street_info, website_dir)

def grab_map(website_dir):
    with open(f"{website_dir}/routing/map.toml", "rb") as f:
        out = tomllib.load(f)
        print(out)
    f.close()
    return out

def understand_map(map, destination: tuple):
    continent, street = destination[0], destination[1]
    if street == None: street = "cd"
    return map.get(continent, {}).get(street)
                    
def walk_street(street_info, website_dir):
    try:
        if street_info[0] == "REDIRECT":
            url:str = street_info[1]
            if url.startswith("http://") or url.startswith("https://"): 
                return redirect(url, 301)
            else: redirect(f"https://{url}", 301)
        if street_info[0] == "FILE":
            path:str = street_info[1]
            if path.startswith("~"):
                return send_file(f'{website_dir}/{path[2:]}'), 200
            else: 
                return send_file(f'{path}'), 200
        if street_info[0] == "DOWNLOAD":
            path:str = street_info[1]
            if path.startswith("~"):
                return send_file(f'{website_dir}/{path[2:]}', as_attachment=True), 200
            else: 
                return send_file(f'{path}', as_attachment=True), 200
        if street_info[0] == "ERROR_CODE":
            code = str(street_info[1])
            if code.startswith("9"):
                return custom_abort.abort(code)
            else: return abort(int(code))
    except: return abort(500)