from grscheller.datastructures.dqueue import Dqueue
from grscheller.datastructures.functional import Maybe

class TestStack:
    def test_push_then_pop(self):
        dq = Dqueue()
        pushed = 42; dq.pushL(pushed)
        popped = dq.popL().getOrElse()
        assert pushed == popped
        assert dq.isEmpty()
        assert dq.popL().getOrElse(42) == 42
        pushed = 0; dq.pushL(pushed)
        popped = dq.popR().getOrElse(42)
        assert pushed == popped == 0
        assert dq.isEmpty()
        pushed = 0; dq.pushR(pushed)
        popped = dq.popL().getOrElse()
        assert popped is not None
        assert pushed == popped
        assert dq.isEmpty()
        pushed = ''; dq.pushR(pushed)
        popped = dq.popR().getOrElse()
        assert pushed == popped
        assert dq.isEmpty()
        dq.pushR('first').pushR('second').pushR('last')
        assert dq.popL().getOrElse() == 'first'
        assert dq.popR().getOrElse() == 'last'
        assert not dq.isEmpty()
        dq.popL()
        assert dq.isEmpty()

    def test_iterators(self):
        data = [1, 2, 3, 4]
        dq = Dqueue(*data)
        data.reverse()
        ii = 0
        for item in reversed(dq):
            assert data[ii] == item
            ii += 1
        assert ii == 4

        data.reverse()
        data.append(42)
        dq.pushR(42)
        ii=0
        for item in dq:
            assert data[ii] == item
            ii += 1
        assert ii == 5

    def test_capacity(self):
        dq = Dqueue(1, 2)
        assert dq.fractionFilled() == 2/4
        dq.pushL(0)
        assert dq.fractionFilled() == 3/4
        dq.pushR(3)
        assert dq.fractionFilled() == 4/4
        dq.pushR(4)
        assert dq.fractionFilled() == 5/8
        assert len(dq) == 5
        assert dq.capacity() == 8
        dq.resize()
        assert dq.fractionFilled() == 5/5
        dq.resize(20)
        assert dq.fractionFilled() == 5/25

    def test_equality(self):
        dq1 = Dqueue(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'))
        dq2 = Dqueue(2, 3, 'Forty-Two').pushL(1).pushR((7, 11, 'foobar'))
        assert dq1 == dq2

        tup2 = dq2.popR().getOrElse((42, 'Hitchhiker'))
        assert dq1 != dq2

        dq2.pushR((42, 'foofoo'))
        assert dq1 != dq2

        dq1.popR().getOrElse((38, 'Nami'))
        dq1.pushR((42, 'foofoo')).pushR(tup2)
        dq2.pushR(tup2)
        assert dq1 == dq2

        holdA = dq1.popL().getOrElse(666)
        dq1.resize(42)
        holdB = dq1.popL().getOrElse(777)
        holdC = dq1.popR().getOrElse(888)
        dq1.pushL(holdB).pushR(holdC).pushL(holdA).pushL(200)
        dq2.pushL(200)
        assert dq1 == dq2

    def test_maybe(self):
        m42 = Dqueue().pushL(42).popR()
        assert m42 == Maybe(42)
        assert m42 != Maybe(21)
        assert m42.getOrElse(21) == 42
        assert m42.getOrElse(21) != 21
