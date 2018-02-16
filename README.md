About
======

This is a config utility.

Features
--------

* For config information which have structure of a dictionary and tree.
* You must define classes and instance variables for each dictionary. 
  * It is a little troublesome but useful because PyCharm complement property names and infer the types.
* You can define default values in the classes and change them by a dictionary object recursively.
  * It is nice to use with yaml config files.

Requirements
----------

* Python3

How to use
===========

Install
---------

```bash
pip install moke_config
```

Code
---------

Like this.

```python
import os
from moke_config.config import Config, EnvValue


class Root(Config):
    def __init__(self):
        self.section_a = SectionA()
        self.list_of_section_a = [SectionA]  # type: list[SectionA]
        self.working_dir = EnvValue("WD", "/my_working_dir")
        self.end_point = EnvValue("END_POINT", "your_endpoint")

    data_path = property(lambda self: "%s/data" % self.working_dir)


class SectionA(Config):
    def __init__(self):
        self.name = "hoge"
        self.something = 10
        self.some_list = [1, 2]
        self.child_section = ChildSection()


class ChildSection(Config):
    def __init__(self):
        self.my_name = "child"
        self.my_age = 20


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


def test_with_args():
    os.environ["END_POINT"] = "moon"
    config = Root.create(DICT)
    assert "/my_working_dir" == config.working_dir
    assert "moon" == config.end_point
    assert 999 == config.section_a.something
    assert 888 == config.section_a.child_section.my_age
    assert "child" == config.section_a.child_section.my_name
    assert 2 == len(config.list_of_section_a)
    assert [3, 4, 5] == config.list_of_section_a[0].some_list
    assert 777 == config.list_of_section_a[1].child_section.my_age
```

