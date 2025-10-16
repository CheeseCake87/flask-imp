from test_app import imp, db

from flask_imp.auth import (
    generate_salt,
    generate_password,
    encrypt_password,
    generate_private_key,
)


def include(bp):
    @bp.route("/database-creation", methods=["GET"])
    def database_creation_test():
        db.drop_all()
        db.create_all()
        return "Database created."

    @bp.route("/database-population", methods=["GET"])
    def database_population_test():
        db.drop_all()
        db.create_all()

        m_example_user = imp.model("ExampleUser")
        m_example_user_bind = imp.model("ExampleUserBind")
        m_example_table = imp.model("ExampleTable")

        if not m_example_user.get_by_id(1):
            salt = generate_salt()
            gen_password = generate_password("animals")
            password = encrypt_password(gen_password, salt)

            new_example_user = m_example_user(
                username="David",
                password=password,
                salt=salt,
                private_key=generate_private_key(salt),
                disabled=False,
            )
            db.session.add(new_example_user)
            new_example_user_bind = m_example_user_bind(
                username="David",
                password=password,
                salt=salt,
                private_key=generate_private_key(salt),
                disabled=False,
            )
            db.session.add(new_example_user_bind)
            db.session.flush()
            new_example_user_rel = m_example_table(
                user_id=new_example_user.user_id, thing=gen_password
            )
            db.session.add(new_example_user_rel)
            db.session.flush()
            db.session.commit()

            user_in_example_table = imp.model("ExampleTable").get_by_user_id(
                new_example_user.user_id
            )

            if user_in_example_table:
                return (
                    f"{new_example_user.username} created and {user_in_example_table.thing}"
                    f"in ExampleTable, and {new_example_user_bind.username} created in ExampleUserBind."
                )

        return "Failed Auto Test, User already exists."
