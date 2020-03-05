from . import bp


@bp.route("/")
def hello():
    return "<h1>Hello bug tracker</h1>"
