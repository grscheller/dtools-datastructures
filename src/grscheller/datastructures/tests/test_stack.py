from grscheller.datastructures.stack import Stack

class TestStack:
    def test_push_then_pop(self):
        q1 = Stack()
        pushed = 42; q1.push(pushed)
        popped = q1.pop()
        assert pushed == popped == 42

    def test_pop_from_empty_stack(self):
        q1 = Stack()
        popped = q1.pop()
        assert popped is None

        q2 = Stack(1,2,3,42)
        while not q2.isEmpty():
            assert q2.head() is not None
            q2.pop()
        assert q2.isEmpty()
        assert q2.pop() is None

    def test_stack_len(self):
        q0 = Stack()
        q1 = Stack(*range(0,2000))

        assert len(q0) == 0
        assert len(q1) == 2000
        q0.push(42)
        q1.pop()
        q1.pop()
        assert len(q0) == 1
        assert len(q1) == 1998

    def test_tail(self):
        q1 = Stack()
        q1.push("fum").push("fo").push("fi").push("fe")
        q2 = q1.tail()
        q3 = q1.copy()
        assert q2 is not None
        q4 = q2.copy()

        if q2 is None:
            assert False
        q1.pop()
        while not q1.isEmpty():
            assert q1.pop() == q2.pop()
        assert q2.isEmpty()
        assert q1.pop() is None
        assert q1.tail().isEmpty()
        
        q4.push(q3.head())
        assert q3 is not q4
        assert q3.head() is q4.head()
        while not q3.isEmpty():
            assert q3.pop() == q4.pop()
        assert q3.isEmpty()
        assert q4.isEmpty()

    def test_stack_iter(self):
        giantStack = Stack(*reversed(["Fe", "Fi", "Fo", "Fum"]))
        giantTalk = giantStack.head()
        for giantWord in giantStack.tail():
            giantTalk += ", " + giantWord
        assert giantTalk == "Fe, Fi, Fo, Fum"
        assert len(giantStack) == 4

