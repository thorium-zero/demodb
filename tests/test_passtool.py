from src.utility.pass_tool import PassTool


def test_check_password():
    a = "абырвал"
    a_hash = PassTool.make_hash(a)
    assert PassTool.check_password(a, a_hash)


def test_check_password_incorrect():
    a = "абырвал"
    b = "Aбырвал"
    a_hash = PassTool.make_hash(a)
    assert not PassTool.check_password(b, a_hash)