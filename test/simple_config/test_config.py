from simple_config.config import Config


class Root(Config):
    def __init__(self, **kwargs):
        self.section_a = SectionA()
        self.list_of_section_a = [SectionA]  # type: list[SectionA]
        super().__init__(**kwargs)


class SectionA(Config):
    def __init__(self, **kwargs):
        self.name = "hoge"
        self.something = 10
        self.some_list = [1, 2]
        self.child_section = ChildSection()
        super().__init__(**kwargs)


class ChildSection(Config):
    def __init__(self, **kwargs):
        self.my_name = "child"
        self.my_age = 20
        super().__init__(**kwargs)


DICT = {
    "section_a": {
        "something": 999,
        "child_section": {
            "my_age": 888
        }
    },

    "list_of_section_a": [
        {
            "name": "section_a(1)",
            "some_list": [3, 4, 5],
            "child_section": {"my_name": "a(1):child"}
        },
        {
            "name": "section_a(2)",
            "some_list": [6, 7, 8],
            "child_section": {"my_name": "a(2):child", "my_age": 777}
        },
    ]
}


def test_no_args():
    config = Root()
    assert "hoge" == config.section_a.name
    assert [] == config.list_of_section_a
    assert [1, 2] == config.section_a.some_list
    assert "child" == config.section_a.child_section.my_name


def test_with_args():
    config = Root(**DICT)
    assert 999 == config.section_a.something
    assert 888 == config.section_a.child_section.my_age
    assert "child" == config.section_a.child_section.my_name
    assert 2 == len(config.list_of_section_a)
    assert [3, 4, 5] == config.list_of_section_a[0].some_list
    assert 777 == config.list_of_section_a[1].child_section.my_age


def test_in():
    config = Root()
    assert "name" in config.section_a
    assert not ("age" in config.section_a)


def test_to_dict():
    config = Root(**DICT)
    d = config.to_dict()
    assert 999 == d["section_a"]["something"]
    assert 888 == d["section_a"]["child_section"]["my_age"]
    assert 2 == len(d["list_of_section_a"])
    assert [3, 4, 5] == d["list_of_section_a"][0]["some_list"]
