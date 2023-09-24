from grscheller.datastructures.stack import Stack
from grscheller.datastructures.functional import Maybe, Nothing

class TestStack:
    def test_push_then_pop(self):
        s1 = Stack()
        pushed = 42; s1.push(pushed)
        popped = s1.pop().getOrElse(())
        assert pushed == popped == 42

    def test_pop_from_empty_stack(self):
        s1 = Stack()
        popped = s1.pop().getOrElse(())
        assert popped is ()
        assert popped is not None
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
        assert ms2 is not Nothing
        ms4 = ms2.map(lambda x: x.copy())
        assert ms4 == ms2
        assert ms4.flatMap(lambda x: Maybe(x.tail())) == ms2.map(lambda x: x.tail())
        assert ms4.getOrElse(Stack(*[1, 2, 3])) == ms2.getOrElse(Stack(*[3, 2, 1])) 
        while not s1.isEmpty():
            s1.pop()
        assert s1.pop() is Nothing
        assert s1.tail() is Nothing

    def test_stack_iter(self):
        giantStack = Stack(*reversed(["Fe", " Fi", " Fo", " Fum"]))
        giantTalk = giantStack.head().getOrElse("Teeny Tiny")
        assert giantTalk == "Fe"
        generalThumb = ['I', ' am', ' General', ' Tom', ' Thumb.']
        gs = giantStack.tail().getOrElse(Stack(*reversed(generalThumb)))
        for giantWord in gs:
            giantTalk = giantTalk + giantWord
        assert len(giantStack) == 4
        assert giantTalk == "Fe Fi Fo Fum"

    def test_equality(self):
        s1 = Stack(*range(3))
        s2 = s1.cons(42)
        assert s1 is not s2
        assert s1 is not s2.tail().getOrElse(Stack())
        assert s1 != s2
        assert s1 == s2.tail().getOrElse(Stack())

        assert s2.head().getOrElse(7) == 42
        assert s2.pop().getOrElse(0) == 42

        s3 = Stack(range(10000))
        s4 = s3.copy()
        assert s3 is not s4
        assert s3 == s4
        
        s3.push(s4.pop().getOrElse(-1))
        assert s3 is not s4
        assert s3 != s4
        s3.pop()
        s3.pop()
        assert s3 == s4

        s5 = Stack(*[1,2,3,4])
        s6 = Stack(*[1,2,3,42])
        assert s5 != s6
        for aa in range(10):
            s5.push(aa)
            s6.push(aa)
        assert s5 != s6

        ducks = ["huey", "dewey"]
        s7 = Stack(ducks)
        s8 = Stack(ducks)
        s9 = Stack(["huey", "dewey", "louie"])
        assert s7 == s8
        assert s7 != s9
        assert s7.head() == s8.head()
        assert s7.head() is not s8.head()
        assert s7.head() != s9.head()
        assert s7.head() is not s9.head()
        ducks.append("louie")
        assert s7 == s8
        assert s7 == s9
        s7.push(['moe', 'larry', 'curlie'])
        s8.push(['moe', 'larry'])
        assert s7 != s8
        s8.head().getOrElse([]).append("curlie")
        assert s7 == s8

    def test_doNotStoreNones(self):
        s10 = Stack()
        s10.push(None)
        s10.push(None)
        s10.push(None)
        s10.push(42)
        s10.push(None)
        assert len(s10) == 1
        s10.pop()
        assert s10.isEmpty()
