from grscheller.datastructures.stack import Stack

class TestStack:
    def test_push_then_pop(self):
        s1 = Stack()
        pushed = 42; s1.push(pushed)
        popped = s1.pop()
        assert pushed == popped == 42

    def test_pop_from_empty_stack(self):
        s1 = Stack()
        popped = s1.pop()
        assert popped is None

        s2 = Stack(1,2,3,42)
        while not s2.isEmpty():
            assert s2.head() is not None
            s2.pop()
        assert s2.isEmpty()
        assert s2.pop() is None

    def test_stack_len(self):
        s0 = Stack()
        s1 = Stack(*range(0,2000))

        assert len(s0) == 0
        assert len(s1) == 2000
        s0.push(42)
        s1.pop()
        s1.pop()
        assert len(s0) == 1
        assert len(s1) == 1998

    def test_tail(self):
        s1 = Stack()
        s1.push("fum").push("fo").push("fi").push("fe")
        s2 = s1.tail()
        s3 = s1.copy()
        assert s2 is not None
        s4 = s2.copy()

        if s2 is None:
            assert False
        s1.pop()
        while not s1.isEmpty():
            assert s1.pop() == s2.pop()
        assert s2.isEmpty()
        assert s1.pop() is None
        assert s1.tail().isEmpty()
        
        s4.push(s3.head())
        assert s3 is not s4
        assert s3.head() is s4.head()
        while not s3.isEmpty():
            assert s3.pop() == s4.pop()
        assert s3.isEmpty()
        assert s4.isEmpty()

    def test_stack_iter(self):
        giantStack = Stack(*reversed(["Fe", "Fi", "Fo", "Fum"]))
        giantTalk = giantStack.head()
        for giantWord in giantStack.tail():
            giantTalk += ", " + giantWord
        assert giantTalk == "Fe, Fi, Fo, Fum"
        assert len(giantStack) == 4

    def test_equality(self):
        s1 = Stack(range(3))
        s2 = s1.cons(42)
        assert s1 is not s2
        assert s1 is not s2.tail()
        assert s1 != s2
        assert s1 == s2.tail()

        assert s2.head() == 42
        assert s2 != 42

        s3 = Stack(range(10000))
        s4 = s3.copy()
        assert s3 is not s4
        assert s3 == s4
        
        s3.push(s4.pop())
        assert s3 is not s4
        assert s3 != s4
        s3.pop()
        s3.pop()
        assert s3 == s4

        s5 = Stack(*[1,2,3,4])
        s6 = Stack(*[1,2,3,42])
        assert s5 != s6
        for aa in range(10000):
            s5.push(aa)
            s6.push(aa)
        assert s5 != s6

        ducks = ["huey", "dewey"]
        s7 = Stack(ducks)
        s8 = Stack(ducks)
        s9 = Stack(["huey", "dewey"])
        assert s7 == s8
        assert s7 == s9
        assert s7.head() == s8.head()
        assert s7.head() is s8.head()
        assert s7.head() == s9.head()
        assert s7.head() is not s9.head()
        ducks.append("lewey")
        assert s7 == s8
        assert s7 != s9
        if s9.head() is not None:
            s9.head().append("lewey")
        assert s7 == s9
