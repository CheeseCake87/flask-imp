from flask_imp.auth import (
    hash_password_assert,
    authenticate_password,
    encrypt_password,
    hash_password,
)


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

        result = authenticate_password(
            "wrong", encrypted_password, "salt", 512, 1, "start"
        )

        return f"{result}"

    @bp.route("/auth/password/correct/long", methods=["GET"])
    def auth_test_password_correct_long():
        password = "password"

        encrypted_password = encrypt_password(password, "salt", 512, 3, "start")

        result = authenticate_password(
            password, encrypted_password, "salt", 512, 3, "start"
        )

        return f"{result}"

    @bp.route("/auth/hash/correct", methods=["GET"])
    def auth_test_hash_correct():
        hashed_password = hash_password("password")
        return f"{hash_password_assert('password', hashed_password)}"

    @bp.route("/auth/hash/incorrect", methods=["GET"])
    def auth_test_hash_incorrect():
        hashed_password = hash_password("password")
        return f"{hash_password_assert('wrong', hashed_password)}"

    @bp.route("/auth/hash/invalid", methods=["GET"])
    def auth_test_hash_invalid():
        return f"{hash_password_assert('password', 'not-a-hash')}"
