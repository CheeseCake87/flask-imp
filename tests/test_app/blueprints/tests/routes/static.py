from flask import render_template


def include(bp):
    @bp.route("/static", methods=["GET"])
    def static_test():
        return render_template(bp.tmpl("static.html"))
