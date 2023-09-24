from grscheller.datastructures.functional import Maybe, Nothing

def add2(x):
    return x + 2

class TestMaybe:
    def test_identity(self):
        n1 = Maybe()
        n2 = Maybe()
        o1 = Maybe(42)
        o2 = Maybe(40)
        assert o1 is o1
        assert o1 is not o2
        o3 = o2.map(add2)
        assert o3 is not o2
        assert o1 is not o3
        assert n1 is n1
        assert n1 is not n2
        assert o1 is not n1
        assert n2 is not o2

    def test_equality(self):
        n1 = Maybe()
        n2 = Maybe()
        o1 = Maybe(42)
        o2 = Maybe(40)
        assert o1 == o1
        assert o1 != o2
        o3 = o2.map(add2)
        assert o3 != o2
        assert o1 == o3
        assert n1 == n1
        assert n1 == n2
        assert o1 != n1
        assert n2 != o2

    def test_iterate(self):
        o1 = Maybe(38)
        o2 = o1.map(add2).map(add2)
        n1 = Maybe()
        l1 = []
        l2 = []
        for v in n1:
            l1.append(v)
        for v in o2:
            l2.append(v)
        assert len(l1) == 0
        assert len(l2) == 1
        assert l2[0] == 42

    def test_get(self):
        o1 = Maybe(1)
        n1 = Maybe()
        assert o1.getOrElse(42) == 1
        assert n1.getOrElse(42) == 42
        assert o1.getOrElse() == 1
        assert n1.getOrElse() is ()
        assert n1.getOrElse() == ()
        assert n1.getOrElse(None) is None
        assert n1.getOrElse(None) == None

    def test_nothing(self):
        o1 = Maybe(42)
        n1 = Maybe()
        n2 = n1
        assert o1 != Nothing
        assert n1 == Nothing
        assert n1 is not Nothing
        assert n1 is n1
        assert n1 is n2
        assert Nothing is Nothing
