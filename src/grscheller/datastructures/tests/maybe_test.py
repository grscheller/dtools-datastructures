from grscheller.datastructures.core import Maybe, MaybeMutable

def add2(x):
    return x + 2

class TestIdentity:
    def test_maybe(self):
        no1 = Maybe()
        no2 = Maybe()
        o1 = Maybe(42)
        o2 = Maybe(40)
        assert o1 is o1
        assert o1 is not o2
        o3 = o2.map(add2)
        assert o3 is not o2
        assert o1 is not o3
        assert no1 is no1
        assert no1 is not no2
        assert o1 is not no1
        assert no2 is not o2

    def test_maybemutable(self):
        no1 = MaybeMutable()
        no2 = MaybeMutable()
        o1 = MaybeMutable(42)
        o2 = MaybeMutable(40)
        assert o1 is o1
        assert o1 is not o2
        o3 = o2.map(add2)
        assert o3 is o2
        assert o1 is not o3
        assert no1 is no1
        assert no1 is not no2
        assert o1 is not no1
        assert no2 is not o2

class TestEquality:
    def test_maybe(self):
        no1 = Maybe()
        no2 = Maybe()
        o1 = Maybe(42)
        o2 = Maybe(40)
        assert o1 == o1
        assert o1 != o2
        o3 = o2.map(add2)
        assert o3 != o2
        assert o1 == o3
        assert no1 == no1
        assert no1 == no2
        assert o1 != no1
        assert no2 != o2

    def test_maybemutable(self):
        no1 = MaybeMutable()
        no2 = MaybeMutable()
        o1 = MaybeMutable(42)
        o2 = MaybeMutable(40)
        assert o1 == o1
        assert o1 != o2
        o3 = o2.map(add2)
        assert o3 == o2
        assert o1 == o3
        assert no1 is no1
        assert no1 == no2
        assert o1 != no1
        assert no2 != o2
