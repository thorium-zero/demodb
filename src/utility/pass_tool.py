import bcrypt


class PassTool:
    @staticmethod
    def make_hash(password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    @staticmethod
    def check_password(password: str, password_hash: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash)
