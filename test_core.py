from core import fill_template, fill_for_channels, build_all, plan_job

def test_fill_template():
    assert fill_template("[a]_[b]", {"a": "x", "b": "y"}) == "x_y"

def test_fill_template_token():
    assert fill_template("[a]_[b]", {"a": "x"}) == "x_[b]", "missing token left as-is (intentional for now)"

def test_fill_for_channels():
    assert len(fill_for_channels("[a]_[b]", {}, ["51", "loro"])) == 2

def test_build_all():
    assert len(build_all({"x": "[a]_[b]"}, {}, {"x": ["51", "loro"]})) == 2

def test_plan_job():
    assert plan_job("parent_[a]", {"mix": "child_[a]"}, {"a": "x"}, {"mix": ["51"]}) == {"parent": "parent_x", "children": ["child_x"]}