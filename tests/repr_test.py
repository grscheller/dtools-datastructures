# Copyright 2023-2024 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from typing import Any, Optional
from grscheller.datastructures.split_ends import SplitEnd
from grscheller.datastructures.queues import DoubleQueue, FIFOQueue, LIFOQueue
from grscheller.datastructures.tuples import FTuple
from grscheller.datastructures.core.fp import Maybe, Nothing, Some, Either, Left, Right

class Test_repr:
    def test_DoubleQueue(self) -> None:
        ca1: DoubleQueue[object] = DoubleQueue()
        assert repr(ca1) == 'DoubleQueue()'
        dq2 = eval(repr(ca1))
        assert dq2 == ca1
        assert dq2 is not ca1

        ca1.pushR(1)
        ca1.pushL('foo')
        assert repr(ca1) == "DoubleQueue('foo', 1)"
        dq2 = eval(repr(ca1))
        assert dq2 == ca1
        assert dq2 is not ca1

        assert ca1.popL() == 'foo'
        ca1.pushR(2)
        ca1.pushR(3)
        ca1.pushR(4)
        ca1.pushR(5)
        assert ca1.popL() == 1
        ca1.pushL(42)
        ca1.popR()
        assert repr(ca1) == "DoubleQueue(42, 2, 3, 4)"
        dq2 = eval(repr(ca1))
        assert dq2 == ca1
        assert dq2 is not ca1

    def test_FIFOQueue(self) -> None:
        sq1: FIFOQueue[object] = FIFOQueue()
        assert repr(sq1) == 'FIFOQueue()'
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

        sq1.push(1)
        sq1.push('foo')
        assert repr(sq1) == "FIFOQueue(1, 'foo')"
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

        assert sq1.pop() == 1
        sq1.push(2)
        sq1.push(3)
        sq1.push(4)
        sq1.push(5)
        assert sq1.pop() == 'foo'
        sq1.push(42)
        sq1.pop()
        assert repr(sq1) == 'FIFOQueue(3, 4, 5, 42)'
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

    def test_LIFOQueue(self) -> None:
        sq1: LIFOQueue[object] = LIFOQueue()
        assert repr(sq1) == 'LIFOQueue()'
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

        sq1.push(1)
        sq1.push('foo')
        assert repr(sq1) == "LIFOQueue(1, 'foo')"
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

        assert sq1.pop() == 'foo'
        sq1.push(2, 3)
        sq1.push(4)
        sq1.push(5)
        assert sq1.pop() == 5
        sq1.push(42)
        assert repr(sq1) == 'LIFOQueue(1, 2, 3, 4, 42)'
        sq2 = eval(repr(sq1))
        assert sq2 == sq1
        assert sq2 is not sq1

    def test_ftuple(self) -> None:
        ft1:FTuple[object] = FTuple()
        assert repr(ft1) == 'FTuple()'
        ft2 = eval(repr(ft1))
        assert ft2 == ft1
        assert ft2 is not ft1

        ft1 = FTuple(42, 'foo', [10, 22])
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22])"
        ft2 = eval(repr(ft1))
        assert ft2 == ft1
        assert ft2 is not ft1

        list_ref = ft1[2]
        if type(list_ref) == list:
            list_ref.append(42)
        else:
            assert False
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22, 42])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22])"
        popped = ft1[2].pop()                                     # type: ignore
        assert popped == 42
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22])"

        # beware immutable collections of mutable objects
        ft1 = FTuple(42, 'foo', [10, 22])
        ft2 = ft1.copy()
        ft1[2].append(42)                                         # type: ignore
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22, 42])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22, 42])"
        popped = ft2[2].pop()
        assert popped == 42
        assert repr(ft1) == "FTuple(42, 'foo', [10, 22])"
        assert repr(ft2) == "FTuple(42, 'foo', [10, 22])"

    def test_SplitEnd_procedural_methods(self) -> None:
        ps1: SplitEnd[object] = SplitEnd()
        assert repr(ps1) == 'SplitEnd()'
        ps2 = eval(repr(ps1))
        assert ps2 == ps1
        assert ps2 is not ps1

        ps1.push(1)
        ps1.push('foo')
        assert repr(ps1) == "SplitEnd(1, 'foo')"
        ps2 = eval(repr(ps1))
        assert ps2 == ps1
        assert ps2 is not ps1

        assert ps1.pop() == 'foo'
        ps1.push(2)
        ps1.push(3)
        ps1.push(4)
        ps1.push(5)
        assert ps1.pop() == 5
        ps1.push(42)
        assert repr(ps1) == "SplitEnd(1, 2, 3, 4, 42)"
        ps2 = eval(repr(ps1))
        assert ps2 == ps1
        assert ps2 is not ps1

    def test_SplitEnd_functional_methods(self) -> None:
        fs1: SplitEnd[object] = SplitEnd()
        assert repr(fs1) == 'SplitEnd()'
        fs2 = eval(repr(fs1))
        assert fs2 == fs1
        assert fs2 is not fs1

        fs1 = fs1.cons(1).cons('foo')
        assert repr(fs1) == "SplitEnd(1, 'foo')"
        fs2 = eval(repr(fs1))
        assert fs2 == fs1
        assert fs2 is not fs1

        assert fs1.head() == 'foo'
        fs3 = fs1.tail()
        if fs3 is None:
            assert False
        fs3 = fs3.cons(2).cons(3).cons(4).cons(5)
        assert fs3.head() == 5
        if fs3:
            fs4 = fs3.tail().cons(42)                             # type: ignore
        else:
            assert False
        assert repr(fs4) == 'SplitEnd(1, 2, 3, 4, 42)'
        fs5 = eval(repr(fs4))
        assert fs5 == fs4
        assert fs5 is not fs4

    def test_maybe(self) -> None:
        mb1: Maybe[object] = Nothing()
        mb2: Maybe[object] = Some()
        mb3: Maybe[object] = Some(None)
        assert mb1 == mb2 == mb3 == Nothing()
        assert repr(mb2) == 'Nothing()'
        mb4 = eval(repr(mb3))
        assert mb4 == mb3

        def lt5OrNone(x: int) -> Optional[int]:
            if x < 5:
                return x
            else:
                return None

        def lt5OrNoneMaybe(x: int) -> Maybe[int]:
            if x < 5:
                return Some(x)
            else:
                return Nothing()

        mb5 = Some(lt5OrNone(2))
        mb6 = lt5OrNoneMaybe(2)
        mb7 = lt5OrNoneMaybe(3)
        mb8 = Some(lt5OrNone(7))
        mb9 = lt5OrNoneMaybe(8)

        assert mb5 == mb6
        assert mb6 != mb7
        assert mb8 == mb9

        assert repr(mb5) == repr(mb6) ==  'Some(2)'
        assert repr(mb7) ==  'Some(3)'
        assert repr(mb8) == repr(mb9) ==  'Nothing()'

        foofoo = Some(Some('foo'))
        foofoo2 = eval(repr(foofoo))
        assert foofoo2 == foofoo
        assert repr(foofoo) == "Some(Some('foo'))"

    def test_either(self) -> None:
        e1: Either[int, str] = Right('Nobody home!')
        e2: Either[int, str] = Left(None, 'Nobody home!')
        e3: Either[int, str] = Left(None)
        assert e1 == e2 == Right('Nobody home!')
        e5 = eval(repr(e2))
        assert e2 == Right('Nobody home!')
        assert e5 == e2
        assert e5 != e3
        assert e5 is not e2
        assert e5 is not e3

        def lt5OrNone(x: int) -> Optional[int]:
            if x < 5:
                return x
            else:
                return None

        def lt5OrNoneEither(x: int) -> Either[int, str]:
            if x < 5:
                return Left(x)
            else:
                return Right(f'was to be {x}')

        e1 = Left(lt5OrNone(2))
        e2 = lt5OrNoneEither(2)
        e3 = lt5OrNoneEither(3)
        e7: Either[int, str] = Left(lt5OrNone(7), 'was to be 7')
        e8 = lt5OrNoneEither(8)

        assert e1 == e2
        assert e2 != e3
        assert e7 != e8
        assert e7 == eval(repr(e7))

        assert repr(e1) == repr(e2) ==  'Left(2)'
        assert repr(e3) ==  'Left(3)'
        assert repr(e7) == "Right('was to be 7')"
        assert repr(e8) ==  "Right('was to be 8')"

        # foo00: Either[Either[str, str], str] = Left(Left('00', 'foo'))
        # foo01: Either[Either[str, str], str] = Left(Right('01'))
        # foo10: Either[Either[str, str], Either[str,str]] = Right(Left('10', 'foo'))
        # foo11: Either[Either[str, str], Either[str,str]] = Right(Right('foo'))
        # assert repr(foo00) == "Left(Left('00'))"
        # assert repr(foo01) == "Left(Right('01'))"
        # assert repr(foo10) == "Right(Left('foo'))"
        # assert repr(foo11) == "Right(Right('foo'))"

        # foo10clone = eval(repr(foo10))
        # assert foo10clone != foo11
        # assert foo10clone == foo10
        # assert foo10clone is not foo10

class Test_repr_mix:
    def test_mix1(self) -> None:
        thing1: Either[object, str] = Left(FIFOQueue(
            FTuple(42, Some(42), Left(None, 'nobody home')),
            SplitEnd([1, 2, 3, Nothing()], 42, Left(LIFOQueue('foo', 'bar')))
        ))
        
        repr_str = "Left(FIFOQueue(FTuple(42, Some(42), Right('nobody home')), SplitEnd([1, 2, 3, Nothing()], 42, Left(LIFOQueue('foo', 'bar')))))"
        assert repr(thing1) == repr_str

        thing2 = eval(repr(thing1))
        assert thing2 == thing1
        assert thing2 is not thing1

        repr_thing1 = repr(thing1)
        repr_thing2 = repr(thing2)
        assert repr_thing2 == repr_thing1

        assert repr_thing1 == repr_str
        assert repr_thing2 == repr_str
