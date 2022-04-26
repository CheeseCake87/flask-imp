from ....builtins.functions.security import login_required
from .. import bp
from .. import struc
from .. import sql_do
from flask import current_app
from flask import render_template
from sqlalchemy.exc import MultipleResultsFound


@bp.route("/endpoints", methods=["GET"])
@login_required("auth", "account.login")
def test_function():
    render = "renders/test_function.html"
    structure = struc.name()
    extend = struc.extend("backend.html")
    footer = struc.include("footer.html")
    #
    # # print("Print out functions to the terminal or pass them to the render")
    #
    # #
    # # sqlalchemy .one() checks for only one result, if the query returns multiple results it fails
    # # with MultipleResultsFound found on import: from sqlalchemy.exc import MultipleResultsFound
    # #
    # try:
    #     membership_one = sql_do.query(
    #         FlMembership
    #     ).filter(
    #         FlMembership.user_id == 1
    #     ).one()
    # except MultipleResultsFound:
    #     print("multi results found")
    #
    # try:
    #     membership_one_membership_id = sql_do.query(
    #         FlMembership
    #     ).filter(
    #         FlMembership.membership_id == 1
    #     ).one()
    #     print("")
    #     print("membership_one_membership_id type:", type(membership_one_membership_id))
    #     print("membership_one_membership_id:", membership_one_membership_id.group_id)
    #     print("")
    # except MultipleResultsFound:
    #     print("multi results found")
    #
    # #
    # # sqlalchemy .one() - END
    # #
    #
    # #
    # # sqlalchemy .first() outputs the first record found, ignores any others found. If no records found
    # # returns None value
    # #
    # membership_first = sql_do.query(
    #     FlMembership
    # ).filter(
    #     FlMembership.user_id == 1
    # ).first()
    # # not able to loop through list as type is Class
    # try:
    #     for value in membership_first:
    #         print(value)
    # except TypeError:
    #     print("type error while looping membership_first")
    # print("")
    # # return type Class
    # print("membership_first type:", type(membership_first))
    # print("membership_first:", membership_first)
    # print("membership_first user_id:", membership_first.user_id)
    # print("")
    # # you are able to loop through columns by using the method __dict__
    # try:
    #     for key, value in membership_first.__dict__.items():
    #         print("Column:", key, value)
    # except AttributeError:
    #     print("type error while looping dict membership_first")
    # # here is an example of record not found
    # membership_first_no_results = sql_do.query(
    #     FlMembership
    # ).filter(
    #     FlMembership.user_id == 999
    # ).first()
    # print("")
    # # return type is None
    # print("membership_first_no_results type:", type(membership_first_no_results))
    # print("membership_first_no_results:", membership_first_no_results)
    # try:
    #     print("membership_first_no_results user_id:", membership_first_no_results.user_id)
    # except AttributeError:
    #     print("This shows AttributeError")
    # print("")
    # #
    # # sqlalchemy .first() - END
    # #
    #
    # #
    # # sqlalchemy .all() outputs all records found as type List
    # #
    # membership_all = sql_do.query(
    #     FlMembership
    # ).filter(
    #     FlMembership.user_id == 1
    # ).all()
    # print("")
    # # return type List
    # print("membership_all type:", type(membership_all))
    # # can loop over
    # for value in membership_all:
    #     print("membership_all value type:", type(value))
    # # when no results are found the return List will be empty, does not error
    # membership_all_no_results = sql_do.query(
    #     FlMembership
    # ).filter(
    #     FlMembership.user_id == 999
    # ).all()
    # print("")
    # # return type List
    # print("membership_all_no_results type:", type(membership_all_no_results))
    # # can loop over
    # for value in membership_all_no_results:
    #     print("membership_all value type:", type(value))
    # #
    # # sqlalchemy .all() - END
    # #
    #
    # #
    # # there are two methods to perform a query, you can add the action to the object like seen on membership_all_count
    # # then you can load the query into the object and add the action later, like seen on membership_all_blank
    # #
    # membership_all_count = sql_do.query(
    #     FlMembership
    # ).filter(
    #     FlMembership.user_id == 1
    # ).count() # action added to the object creation
    # membership_all_blank = sql_do.query(
    #     FlMembership
    # ).filter(
    #     FlMembership.user_id == 1
    # ) # action left off the object creation, and added to the object call below: membership_all_blank.count()
    # print("membership_all_count count:", membership_all_count)
    # print("membership_all_count count type:", type(membership_all_count))
    # print("")
    # print("membership_all_blank count:", membership_all_blank.count())
    # print("membership_all_blank count type:", type(membership_all_blank.count()))
    return render_template(
        render,
        structure=structure,
        extend=extend,
        footer=footer
    )
