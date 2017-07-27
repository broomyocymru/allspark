from allspark.core import util

def test_replace_name():
    # Basic replacemet
    result = util.template_replace("<name>", "test1")
    assert result == "test1"

    # Leading and trailing text
    result = util.template_replace("pre <name> post", "test1")
    assert result == "pre test1 post"

    # Leading and trailing whitespace
    result = util.template_replace(" <name> ", "test1")
    assert result == " test1 "
