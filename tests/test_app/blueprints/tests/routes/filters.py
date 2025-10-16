from flask import render_template


def include(bp):
    @bp.route("/filters", methods=["GET"])
    def filters_test():
        return render_template(bp.tmpl("filters.html"))
