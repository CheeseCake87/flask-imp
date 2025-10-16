from flask_imp.auth import encrypt_password, authenticate_password


def include(bp):
    @bp.route("/auth/password/correct", methods=["GET"])
    def auth_test_password_correct():
        password = "password"

        encrypted_password = encrypt_password(password, "salt", 512, 1, "start")

        result = authenticate_password(
            password, encrypted_password, "salt", 512, 1, "start"
        )

        return f"{result}"

    @bp.route("/auth/password/incorrect", methods=["GET"])
    def auth_test_password_incorrect():
        password = "password"

        encrypted_password = encrypt_password(password, "salt", 512, 1, "start")

        result = authenticate_password("wrong", encrypted_password, "salt", 512, 1,
                                       "start")

        return f"{result}"

    @bp.route("/auth/password/correct/long", methods=["GET"])
    def auth_test_password_correct_long():
        password = "password"

        encrypted_password = encrypt_password(password, "salt", 512, 3, "start")

        result = authenticate_password(
            password, encrypted_password, "salt", 512, 3, "start"
        )

        return f"{result}"
