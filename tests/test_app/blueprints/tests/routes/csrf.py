from flask import render_template, session, request

from flask_imp.security import include_csrf


def include(bp):
    @bp.get("/csrf-get-to-post")
    @include_csrf()
    def csrf_get_to_post():
        return render_template(bp.tmpl("get-to-post.html"), crsf=session["csrf"])

    @bp.get("/csrf-session")
    @include_csrf()
    def csrf_session():
        return session["csrf"]

    @bp.post("/csrf-post-pass")
    @include_csrf()
    def csrf_post_to_me_pass():
        return request.form.get("csrf")

    @bp.post("/csrf-post-fail")
    @include_csrf()
    def csrf_post_to_me_fail():
        return request.form.get("csrf")
