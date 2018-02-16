from simple_config.config import Config


class ChildSection(Config):
    my_name = "child"


class SectionA(Config):
    name = "hoge"
    something = 10
    some_list = [1, 2]
    child_section = ChildSection


class Root(Config):
    def __init__(self, **kwargs):
        self.section_a = SectionA
        super().__init__(**kwargs)


def test_hoge():
    config = Root()
    assert config.section_a.child_section.my_name == "child"
