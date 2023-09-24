from grscheller.datastructures.stack import Stack
from grscheller.datastructures.functional import Nothing

class TestStack:
    def test_push_then_pop(self):
        s1 = Stack()
        pushed = 42; s1.push(pushed)
        popped = s1.pop().getOrElse(())
        assert pushed == popped == 42

    def test_pop_from_empty_stack(self):
        s1 = Stack()
        popped = s1.pop().getOrElse(())
        assert popped is not ()
        assert popped is None
        popped = s1.pop().getOrElse('Forty-Two')
        assert popped == 'Forty-Two'

        s2 = Stack(1, 2, 3, 42)
        while not s2.isEmpty():
            assert s2.head().getOrElse() is not Nothing
            s2.pop()
        assert s2.isEmpty()
        assert s2.pop() is Nothing

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
        ms2 = s1.tail()
        s3 = s1.copy()
        assert ms2 is not Nothing
        ms4 = ms2.map(lambda x: x.copy())
        #s5 = ms2.get().copy()

        if ms2 is Nothing:
            assert False
        s1.pop()
        while not s1.isEmpty():
            assert s1.pop() == ms2.map(lambda x: x.pop()).getOrElse('wee wee wee')
        assert len(ms2.getOrElse()) == 0
        assert s1.pop() is Nothing
        assert s1.tail() is Nothing
        
        ms4.push(s3.head())
        assert s3 is not ms4
        assert s3.head() is ms4.head().get()
        while not s3.isEmpty():
            assert s3.pop() == ms4.pop()
        assert s3.isEmpty()
        assert ms4.isEmpty()

    def test_stack_iter(self):
        giantStack = Stack(*reversed(["Fe", "Fi", "Fo", "Fum"]))
        giantTalk = giantStack.head().getOrElse()
        gs = giantStack.tail().getOrElse(Stack(*reversed(['I', 'am', 'Tom', 'Thumb.']))):
            for giantWord in gs:
            giantTalk += " " + giantWord
        assert giantTalk == "Fe Fi Fo Fum"
        assert len(giantStack) == 4

    def test_equality(self):
        s1 = Stack(*range(3))
        s2 = s1.cons(42)
        assert s1 is not s2
        assert s1 is not s2.tail().get()
        assert s1 != s2
        assert s1 == s2.tail().get()

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
        if s9.head() is not Nothing:
            s9.head().getOrElse([]).append("lewey")
        assert s7 == s9

    def test_storeNones(self):
        s10 = Stack()
        s10.push(None)
        s10.push(None)
        s10.push(None)
        s10.push(42)
        assert len(s10) == 1
        s10.pop()
        assert s10.isEmpty()
