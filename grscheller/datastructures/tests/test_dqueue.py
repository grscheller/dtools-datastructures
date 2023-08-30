from grscheller.datastructures.dqueue import Dqueue

class TestStack:
    def test_push_then_pop(self):
        dq = Dqueue()
        pushed = 42; dq.pushL(pushed)
        popped = dq.popL()
        assert pushed == popped
        assert dq.isEmpty()
        pushed = 0; dq.pushL(pushed)
        popped = dq.popR()
        assert pushed == popped == 0
        assert dq.isEmpty()
        pushed = 0; dq.pushR(pushed)
        popped = dq.popL()
        assert pushed == popped
        assert dq.isEmpty()
        pushed = ''; dq.pushR(pushed)
        popped = dq.popR()
        assert pushed == popped
        assert dq.isEmpty()
        dq.pushR('first').pushR('second').pushR('last')
        assert dq.popL() == 'first'
        assert dq.popR() == 'last'
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
        for item in iter(dq):
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
