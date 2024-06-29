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

from typing import Any, Tuple
from grscheller.datastructures.arrays import PArray

class TestPArray:
    def test_map1(self) -> None:
        pa1 = PArray(0, 1, 2, 3, size=-6, sentinel=-1)
        pa2 = pa1.map(lambda x: x+1, size=7, sentinel=42)
        pa3 = pa1.map(lambda x: x+1, size=7, mapsentinel=True)
        pa4 = pa1.map(lambda x: x+1, size=7)
        assert pa1[0] + 1 == pa2[0] == 0
        assert pa1[1] + 1 == pa2[1] == 0
        assert pa1[2] + 1 == pa2[2] == 1
        assert pa1[3] + 1 == pa2[3] == 2
        assert pa1[4] + 1 == pa2[4] == 3
        assert pa1[5] + 1 == pa2[5] == 4
        assert pa2[6] == 42
        assert pa1._sentinel == -1
        assert pa2._sentinel == 42
        assert pa3._sentinel == 0
        assert pa4._sentinel == -1

    def test_map2(self) -> None:
        pa1 = PArray(0, 1, 2, 3, size=6, sentinel=-1)
        pa2 = pa1.map(lambda x: x+1)
        assert pa1[0] + 1 == pa2[0] == 1
        assert pa1[1] + 1 == pa2[1] == 2
        assert pa1[2] + 1 == pa2[2] == 3
        assert pa1[3] + 1 == pa2[3] == 4
        assert pa1[4] + 1 == pa2[4] == 0
        assert pa1[5] + 1 == pa2[5] == 0

    def test_map3(self) -> None:
        pa1 = PArray(1, 2, 3, 10)

        pa2 = pa1.map(lambda x: x*x-1)
        assert pa2 is not None
        assert pa1 is not pa2
        assert pa1 == PArray(1, 2, 3, 10)
        assert pa2 == PArray(0, 3, 8, 99)
        
    def test_sentinel(self) -> None:
        pa1 = PArray(size=1, sentinel=1)
        pa2 = PArray(size=1, sentinel=2)
        assert pa1 != pa2
        assert pa1[0] == 1
        assert pa2[0] == 2
        assert not pa1
        assert not pa2
        assert len(pa1) == 1
        assert len(pa2) == 1

        foo = 42
        baz = 'hello world'

        try:
            foo = pa1[0]
        except IndexError:
            assert False
        else:
            assert True
        finally:
            assert True
            assert foo == 1

        try:
            baz = pa2[42]
        except IndexError:
            assert False
        else:
            assert True
        finally:
            assert True
            assert baz == None

        pa1 = PArray(size=1, sentinel=12)
        pa2 = PArray(size=1, sentinel=30)
        assert pa1 != pa2
        assert not pa1
        assert not pa2
        assert len(pa1) == 1
        assert len(pa2) == 1

        pa0 = PArray()
        pa1 = PArray(sentinel=())
        pa2 = PArray(None, None, None, size=2)
        pa3 = PArray(None, None, None, size=2, sentinel=())
        assert len(pa0) == 0
        assert pa0.sentinel() == ()
        assert len(pa1) == 0
        assert pa1.sentinel() == ()
        assert len(pa2) == 2
        assert pa2.sentinel() == ()
        assert len(pa3) == 2
        assert pa3.sentinel() == ()
        assert pa2[0] == pa2[1] == ()
        assert pa3[0] == pa3[1] == ()
        assert not pa0
        assert not pa1
        assert not pa2
        assert not pa3

        pa1 = PArray(1, 2, size=3, sentinel=42)
        pa2 = PArray(1, 2, None, size=3, sentinel=42)
        assert pa1 == pa2
        assert pa1 is not pa2
        assert pa1
        assert pa2
        assert len(pa1) == 3
        assert len(pa2) == 3
        assert pa1[0] == 1
        assert pa2[0] == 1
        assert pa1[1] == 2
        assert pa2[1] == 2
        assert pa1[2] == 42
        assert pa2[2] == 42
        assert pa1[-1] == 42
        assert pa2[-1] == 42
        assert pa1[-2] == 2
        assert pa2[-2] == 2
        assert pa1[-3] == 1
        assert pa2[-3] == 1

        pa1 = PArray(1, 2, size=-3)
        pa2 = PArray((), 1, 2)
        assert pa1 == pa2
        assert pa1 is not pa2
        assert pa1
        assert pa2
        assert len(pa1) == 3
        assert len(pa2) == 3

        pa5 = PArray(*range(1,4), size=-5, sentinel=42)
        assert pa5 == PArray(42, 42, 1, 2, 3)

    def test_set_then_get(self) -> None:
        pa = PArray(size=5, sentinel=0)
        assert pa[1] == 0
        pa[3] = set = 42
        got = pa[3]
        assert set == got

    def test_equality(self) -> None:
        pa1 = PArray(1, 2, 'Forty-Two', (7, 11, 'foobar'))
        pa2 = PArray(1, 3, 'Forty-Two', [1, 2, 3])
        assert pa1 != pa2
        pa2[1] = 2
        assert pa1 != pa2
        pa1[3] = pa2[3]
        assert pa1 == pa2

    def test_len_getting_indexing_padding_slicing(self) -> None:
        pa1 = PArray(*range(2000))
        assert len(pa1) == 2000

        pa1 = PArray(*range(542), size=42)
        assert len(pa1) == 42
        assert pa1[0] == 0
        assert pa1[41] == pa1[-1] == 41
        assert pa1[2] == pa1[-40]

        pa2 = PArray(*range(1042), size=-42)
        assert len(pa2) == 42
        assert pa2[0] == 1000
        assert pa2[41] == 1041
        assert pa2[-1] == 1041
        assert pa2[41] == pa2[-1] == 1041
        assert pa2[1] == pa2[-41] == 1001
        assert pa2[0] == pa2[-42]

        pa3 = PArray(*[1, 'a', (1, 2)], size=5, sentinel=42)
        assert pa3[0] == 1
        assert pa3[1] == 'a'
        assert pa3[2] == (1, 2)
        assert pa3[3] == 42
        assert pa3[4] == 42
        assert pa3[-1] == 42
        assert pa3[-2] == 42
        assert pa3[-3] == (1, 2)
        assert pa3[-4] == 'a'
        assert pa3[-5] == 1

        pa4 = PArray(*[1, 'a', (1, 2)], size=-6, sentinel=42)
        assert pa4[0] == 42
        assert pa4[1] == 42
        assert pa4[2] == 42
        assert pa4[3] == 1
        assert pa4[4] == 'a'
        assert pa4[5] == (1, 2)
        assert pa4[-1] == (1, 2)
        assert pa4[-2] == 'a'
        assert pa4[-3] == 1
        assert pa4[-4] == 42
        assert pa4[-5] == 42
        assert pa4[-6] == 42

    def test_indexing(self) -> None:

        pa1 = PArray(*[1, 'a', (1, 2)], size=5, sentinel=42)

        try:
            foo = pa1[5] 
            assert foo is None
        except IndexError:
            assert False
        except Exception:
            print(error)
            assert False
        else:
            assert True

        try:
            bar = pa1[-6] 
            assert bar is None
        except IndexError:
            assert False
        except Exception:
            assert False
        else:
            assert True

    def test_assigning_none(self) -> None:

        pa1 = PArray(*[1, 'a', (1, 2)], size=5, sentinel=42)

        try:
            pa1[1] = None
        except IndexError:
            assert False
        except ValueError:
            assert False
        else:
            assert True
            assert pa1[1] == 42

        try:
            pa1[0] += 1
        except IndexError:
            assert False
        except ValueError:
            assert False
        else:
            assert True
            assert pa1[0] == 2

    def test_bool(self) -> None:
        pa_allNotNone = PArray(True, 0, '')
        pa_allNone = PArray(None, None, None, sentinel=42)
        pa_firstNone = PArray(None, False, [])
        pa_lastNone = PArray(0.0, True, False, None)
        pa_someNone = PArray(0, None, 42, None, False)
        pa_sentinelNone = PArray(sentinel = None)
        pa_sentinelNotNone = PArray(sentinel = False)
        assert pa_allNotNone
        assert not pa_allNone
        assert pa_firstNone
        assert pa_lastNone
        assert pa_someNone
        assert not pa_sentinelNone
        assert not pa_sentinelNotNone

        pa_Nones = PArray(None, size=4321, sentinel=())
        pa_0 = PArray(0, 0, 0)
        pa_42s = PArray(*([42]*42))
        pa_42s_d42 = PArray(*([42]*42), sentinel=42)
        pa_emptyStr = PArray('')
        pa_hw = PArray('hello', 'world')
        assert not pa_Nones
        assert pa_0
        assert pa_42s
        assert not pa_42s_d42
        assert pa_emptyStr
        assert pa_hw

    def test_reversed_iter(self) -> None:
        """Tests that prior state of pa is used, not current one"""
        pa = PArray(1,2,3,4,5)
        parevIter = reversed(pa)
        aa = next(parevIter)
        assert pa[4] == aa == 5
        pa[2] = 42
        aa = next(parevIter)
        assert pa[3] == aa == 4
        aa = next(parevIter)
        assert pa[2] != aa == 3
        aa = next(parevIter)
        assert pa[1] == aa == 2
        aa = next(parevIter)
        assert pa[0] == aa == 1

    def test_reverse(self) -> None:
        pa1 = PArray(1, 2, 3, 'foo', 'bar')
        pa2 = PArray('bar', 'foo', 3, 2, 1)
        assert pa1 != pa2
        pa2.reverse()
        assert pa1 == pa2
        pa1.reverse()
        assert pa1 != pa2
        assert pa1[1] == pa2[-2]

        pa4 = pa2.copy()
        pa5 = pa2.copy()
        assert pa4 == pa5
        pa4.reverse()
        pa5.reverse()
        assert pa4 != pa2
        assert pa5 != pa2
        pa2.reverse()
        assert pa4 == pa2

    def test_copy_map(self) -> None:
        def ge3(n: int) -> int|None:
            if n < 3:
                return None
            return n

        pa4 = PArray(*range(43), size = 5)
        pa5 = PArray(*range(43), size = -5)
        pa4_copy = pa4.copy()
        pa5_copy = pa5.copy()
        assert pa4 == pa4_copy
        assert pa4 is not pa4_copy
        assert pa5 == pa5_copy
        assert pa5 is not pa5_copy
        assert pa4[0] == 0
        assert pa4[4] == pa4[-1] == 4
        assert pa5[0] == 38
        assert pa5[4] == pa5[-1] == 42

        pa0 = PArray(None, *range(1, 6), size=7, sentinel=0)
        pa0b = PArray(*range(1, 6), size=-7, sentinel=0)
        assert pa0 == PArray(1, 2, 3, 4, 5, 0, 0)
        assert pa0b == PArray(0, 0, 1, 2, 3, 4, 5)
        assert pa0._sentinel == 0
        assert pa0b._sentinel == 0
        pa1 = pa0.copy()
        pa2 = pa0.copy(sentinel=4)
        assert pa1 == pa2 == pa0
        assert pa1._sentinel == 0
        assert pa2._sentinel == 4

        pa0 = pa0.map(ge3)
        pa3 = pa1.map(ge3)
        pa4 = pa2.map(ge3)
        assert pa0.sentinel() == 0
        assert pa3.sentinel() == 0
        assert pa4.sentinel() == 4
        assert pa0 == PArray(0, 0, 3, 4, 5, 0, 0)
        assert pa3 == PArray(0, 0, 3, 4, 5, 0, 0)
        assert pa4 == PArray(4, 4, 3, 4, 5, 4, 4)
        assert pa3.copy(size=6).copy(size=-3) == PArray(4, 5, 0)
        assert pa3.copy(size=6).copy(size=3) == PArray(0, 0, 3)
        assert pa4.copy(size=6).copy(size=-3) == PArray(4, 5, 4)
        assert pa4.copy(size=6).copy(size=3) == PArray(4, 4, 3)
        pa5 = pa3.copy(sentinel=2)
        pa6 = pa4.copy(sentinel=2)
        assert pa6 != pa5
        pa7 = pa5.copy(sentinel=-1)
        pa8 = pa6.copy(sentinel=-1)
        assert pa8 != pa7
        assert pa8.sentinel() == pa7.sentinel() == -1
        assert pa8.map(ge3) != pa7.map(ge3)
        assert pa8.sentinel() == pa7.sentinel() == -1
        assert pa7.map(ge3) == PArray(-1, -1, 3, 4, 5, -1, -1, sentinel = -1)

        pa0 = PArray(5,4,3,2,1)
        assert pa0.copy(size=3) == PArray(5, 4, 3)
        assert pa0.copy(size=-3) == PArray(3, 2, 1)
        pa1 = pa0.map(ge3)
        assert (pa1[0], pa1[1], pa1[2], pa1[3], pa1[4]) == (5, 4, 3, (), ())
        pa2 = pa0.copy(sentinel=0).map(ge3)
        assert (pa2[0], pa2[1], pa2[2], pa2[3], pa2[4]) == (5, 4, 3, 0, 0)
        pa2 = pa0.map(ge3, sentinel=42)
        assert (pa2[0], pa2[1], pa2[2], pa2[3], pa2[4]) == (5, 4, 3, 42, 42)

    def test_backQueue(self) -> None:
        pa1 = PArray(42, 'foo', 'bar', sentinel=42)
        pa2 = pa1.copy()
        pa3 = pa1.copy(sentinel=63)
        pa2[1] = None
        pa3[1] = None
        assert repr(pa2) == "PArray(42, 42, 'bar', size=3, sentinel=42)"
        assert repr(pa3) == "PArray(42, 63, 'bar', size=3, sentinel=63)"

        pa1 = PArray(16, 'foo', 'bar', 100, 101, '102', sentinel=42)
        pa2 = pa1.copy(size=-4)
        pa3 = pa1.copy(size=4)
        assert repr(pa2) == "PArray('bar', 100, 101, '102', size=4, sentinel=42)"
        assert repr(pa3) == "PArray(16, 'foo', 'bar', 100, size=4, sentinel=42)"

        pa2[2] = None
        pa2[1] = None
        pa2[0] = None
        assert repr(pa2) == "PArray(42, 16, 'foo', '102', size=4, sentinel=42)"

        pa3[-1] = None
        assert repr(pa3) == "PArray(16, 'foo', 'bar', 101, size=4, sentinel=42)"
        pa3[-2] = None
        assert repr(pa3) == "PArray(16, 'foo', '102', 101, size=4, sentinel=42)"
        pa3[-3] = None
        assert repr(pa3) == "PArray(16, 42, '102', 101, size=4, sentinel=42)"

        pa4 = PArray(*range(1, 8), size=5, sentinel=0)
        pa5 = PArray(*range(1, 8), size=-5, sentinel=0)
        assert repr(pa4) == "PArray(1, 2, 3, 4, 5, size=5, sentinel=0)"
        assert repr(pa5) == "PArray(3, 4, 5, 6, 7, size=5, sentinel=0)"
    
        pa4[0] = pa4[1] = pa4[2] = pa4[3] = None
        pa5[1] = pa5[0] = pa5[2] = pa5[3] = None

        assert repr(pa5) == "PArray(1, 2, 42, 0, 7, size=5, sentinel=0)"
    
    def test_flatMap(self) -> None:
        def ge1(n: int|Tuple[()]) -> int|None:
            if n == ():
                return None
            if n >= 1:
                return n
            return None

        def lt2or42(n: Any) -> int|None:
            if n == ():
                return 42
            if n < 2:
                return n
            return None

        def lt3(n: Any) -> int|None:
            if n < 3:
                return n
            return None

        # Keep sentinels all the same
        pa0 = PArray(*range(10), sentinel=6)
        pa1 = pa0.flatMap(lambda x: PArray(*range(x%5)))
        pa2 = pa0.flatMap(lambda x: PArray(*range(x%5), sentinel=6))
        pa3 = pa0.flatMap(lambda x: PArray(*range(x%5)), sentinel=6)
        pa4 = pa0.flatMap(lambda x: PArray(*range(x%5), sentinel=7), sentinel=6)
        assert pa1 == pa2 == pa3 == pa4
        assert pa1 == PArray(0,0,1,0,1,2,0,1,2,3,0,0,1,0,1,2,0,1,2,3)
        assert pa0._sentinel == 6
        assert pa1._sentinel == 6
        assert pa2._sentinel == 6
        assert pa3._sentinel == 6
        assert pa4._sentinel == 6
        pa11 = pa1.map(ge1)
        pa12 = pa2.map(ge1)
        pa13 = pa3.map(ge1)
        pa14 = pa4.map(ge1)
        assert pa11 == pa12 == pa13 == pa14
        assert pa11 == PArray(6,6,1,6,1,2,6,1,2,3,6,6,1,6,1,2,6,1,2,3)
        assert pa11.sentinel() == pa12.sentinel() == pa13.sentinel()
        assert pa13.sentinel() == pa14.sentinel() == 6
        pa11 = pa1.map(lt2or42)
        pa12 = pa2.map(lt2or42)
        pa13 = pa3.map(lt2or42)
        pa14 = pa4.map(lt2or42)
        assert pa11 == pa12 == pa13 == pa14
        assert pa11 == PArray(0,0,1,0,1,6,0,1,6,6,0,0,1,0,1,6,0,1,6,6)
        assert pa11._sentinel() == 6
        assert pa12._sentinel() == 6
        assert pa13._sentinel() == 6
        assert pa14._sentinel() == 6

        # Vary up the sentinels
        pa0 = PArray(*range(10), sentinel=6)
        assert pa0._sentinel == 6
        pa1 = pa0.flatMap(lambda x: PArray(*range(x%5)))
        pa2 = pa0.flatMap(lambda x: PArray(*range(x%5), sentinel=7))
        pa3 = pa0.flatMap(lambda x: PArray(*range(x%5)), sentinel=8)
        pa4 = pa0.flatMap(lambda x: PArray(*range(x%5), sentinel=-1), sentinel=9)
        assert pa1._sentinel == 6
        assert pa2._sentinel == 6
        assert pa3._sentinel == 8
        assert pa4._sentinel == 9
        assert pa1 == pa2 == pa3 == pa4
        assert pa1 == PArray(0,0,1,0,1,2,0,1,2,3,0,0,1,0,1,2,0,1,2,3)
        pa11 = pa1.map(lt2or42)
        pa12 = pa2.map(lt2or42)
        pa13 = pa3.map(lt2or42)
        pa14 = pa4.map(lt2or42)
        assert pa11 == PArray(0,0,1,0,1,6,0,1,6,6,0,0,1,0,1,6,0,1,6,6)
        assert pa12 == PArray(0,0,1,0,1,6,0,1,6,6,0,0,1,0,1,6,0,1,6,6)
        assert pa13 == PArray(0,0,1,0,1,8,0,1,8,8,0,0,1,0,1,8,0,1,8,8)
        assert pa14 == PArray(0,0,1,0,1,9,0,1,9,9,0,0,1,0,1,9,0,1,9,9)
        assert pa11._sentinel() == 6
        assert pa12._sentinel() == 6
        assert pa13._sentinel() == 8
        assert pa14._sentinel() == 9

        # Vary up the sentinels, no sentinel set on initial PArray
        pa0 = PArray(*range(10))
        assert pa0.sentinel() == ()
        pa1 = pa0.flatMap(lambda x: PArray(*range(x%5)))
        pa2 = pa0.flatMap(lambda x: PArray(*range(x%5), sentinel=7))
        pa3 = pa0.flatMap(lambda x: PArray(*range(x%5)), sentinel=8)
        pa4 = pa0.flatMap(lambda x: PArray(*range(x%5), sentinel=-1), sentinel=9)
        assert pa1 == pa2 == pa3 == pa4
        assert pa1 == PArray(0,0,1,0,1,2,0,1,2,3,0,0,1,0,1,2,0,1,2,3)
        assert pa1.sentinel() == ()
        assert pa2.sentinel() == ()
        assert pa3.sentinel() == 8
        assert pa4.sentinel() == 9
        pa11 = pa1.map(lt2or42)
        pa12 = pa2.map(lt2or42)
        pa13 = pa3.map(lt2or42)
        pa14 = pa4.map(lt2or42)
        assert pa11 == PArray(0,0,1,0,1,(),0,1,(),(),0,0,1,0,1,(),0,1,(),())
        assert pa12 == PArray(0,0,1,0,1,(),0,1,(),(),0,0,1,0,1,(),0,1,(),())
        assert pa13 == PArray(0,0,1,0,1,8,0,1,8,8,0,0,1,0,1,8,0,1,8,8)
        assert pa14 == PArray(0,0,1,0,1,9,0,1,9,9,0,0,1,0,1,9,0,1,9,9)
        assert pa11._sentinel() == ()
        assert pa12._sentinel() == ()
        assert pa13._sentinel() == 8
        assert pa14._sentinel() == 9

        # Let f change sentinel, set sentinel set on initial PArray
        pa0 = PArray(*range(3), sentinel=6)
        assert pa0.sentinel() == 6
        pa1 = pa0.flatMap(lambda x: PArray(*range(x)))
        pa2 = pa0.flatMap(lambda x: PArray(*range(x), sentinel=x*x))
        pa3 = pa0.flatMap(lambda x: PArray(*range(x)), sentinel=8)
        pa4 = pa0.flatMap(lambda x: PArray(*range(x), sentinel=-1), sentinel=9)
        fpa5 = pa0.flatMap(lambda x: PArray(*range(x), sentinel=pa0.sentinel()))
        fpa6 = pa0.flatMap(lambda x: PArray(*range(x), sentinel=8), sentinel=8)
        assert pa1 == PArray(0, 0, 1)
        assert pa2 == PArray(0, 0, 1)
        assert pa3 == PArray(0, 0, 1)
        assert pa4 == PArray(0, 0, 1)
        assert fpa5 == PArray(0, 0, 1)
        assert fpa6 == PArray(0, 0, 1)
        assert pa1._sentinel() == 6
        assert pa2._sentinel() == 6
        assert pa3._sentinel() == 8
        assert pa4._sentinel() == 9
        assert fpa5._sentinel() == 6
        assert fpa6._sentinel() == 8

        pa0 = PArray(*range(1, 6), sentinel=-1)
        assert pa0.sentinel() == -1
        pa1 = pa0.flatMap(lambda x: PArray(*range(x, x+2), sentinel=x+1))
        pa2 = pa0.flatMap(lambda x: PArray(*range(x-1, x+1), None, 42, sentinel=x*x))
        pa3 = pa0.flatMap(lambda x: PArray(*range(x+1, x+3)), sentinel=8)
        pa4 = pa0.flatMap(lambda x: PArray(*range(x-2, x+1), sentinel=-1), size=-8, sentinel=9)
        assert pa1 == PArray(1,2,2,3,3,4,4,5,5,6)
        assert pa2 == PArray(0,1,42,1,2,42,2,3,42,3,4,42,4,5,42)
        assert pa3 == PArray(2,3,3,4,4,5,5,6,6,7)
        assert pa4 == PArray(2,3,2,3,4,3,4,5)
        assert pa1._sentinel() == -1
        assert pa2._sentinel() == -1
        assert pa3._sentinel() == 8
        assert pa4._sentinel() == 9
        pa11 = pa1.map(lt3)
        pa12 = pa2.map(lt3)
        pa13 = pa3.map(lt3)
        pa14 = pa4.map(lt3)
        assert pa11 == PArray(1,  2,  2, -1, -1, -1, -1, -1, -1, -1)
        assert pa12 == PArray(0,  1, -1,  1,  2, -1,  2, -1, -1, -1, -1, -1, -1, -1, -1)
        assert pa13 == PArray(2,  8,  8,  8,  8,  8,  8,  8,  8,  8)
        assert pa14 == PArray(2,  9,  2,  9,  9,  9,  9,  9)
        assert pa11._sentinel() == -1
        assert pa12._sentinel() == -1
        assert pa13._sentinel() == 8
        assert pa14._sentinel() == 9

        def bar(x: int) -> PArray[int, int]:
            return PArray(2, x, 3*x, size=4, sentinel=7*x)

        pa0 = PArray(1, 2, size=3, sentinel=-1)
        pa01 = pa0.flatMap(bar)
        assert repr(pa01) == 'PArray(2, 1, 3, 7, 2, 2, 6, 14, 2, -1, -3, -7, size=12, sentinel=-1)'
        assert eval(repr(pa01)) == PArray(2, 1, 3, 7, 2, 2, 6, 14, 2, -1, -3, -7)

        pa02 = pa0.flatMap(bar, size=15)
        assert repr(pa02) == 'PArray(2, 1, 3, 7, 2, 2, 6, 14, 2, -1, -3, -7, -1, -1, -1, size=15, sentinel=-1)'

        pa1 = PArray(1, 2, size=4, sentinel=-2, backlog=(9,10,11))
        pa11 = pa1.flatMap(bar, size=12)
        assert repr(pa11) == 'PArray(2, 1, 3, 7, 2, 2, 6, 14, 2, 9, 27, 63, size=12, sentinel=-2)'

        # Python always evaluates/assigns left to right
        pa11[0] = pa11[1] = pa11[2] = pa11[3] = None
        pa11[4] = pa11[5] = pa11[6] = pa11[7] = None
        pa11[8] = pa11[9] = pa11[10] = pa11[11] = None
        assert repr(pa11) == 'PArray(2, 10, 30, 70, -2, -2, -2, -2, -2, -2, -2, -2, size=12, sentinel=-2)'
 
    def test_mergeMap(self) -> None:
        def lt3(n: int) -> Optional[int]:
            if n < 3:
                return n
            return None

        pa0 = PArray(*range(1, 6), sentinel=-1)
        assert pa0.sentinel() == -1
        pa1 = pa0.mergeMap(lambda x: PArray(*range(x, x+2), sentinel=x+1))
        pa2 = pa0.mergeMap(lambda x: PArray(*range(x-1, x+1), sentinel=x*x))
        pa3 = pa0.mergeMap(lambda x: PArray(*range(x+1, x+3)), sentinel=8)
        pa4 = pa0.mergeMap(lambda x: PArray(*range(x-2, x+1), sentinel=-1), size=-8, sentinel=9)
        assert pa1 == PArray(1,2,3,4,5,2,3,4,5,6)
        assert pa2 == PArray(0,1,2,3,4,1,2,3,4,5)
        assert pa3 == PArray(2,3,4,5,6,3,4,5,6,7)
        assert pa4 == PArray(2,3,4,1,2,3,4,5)
        assert pa1._sentinel() == -1
        assert pa2._sentinel() == -1
        assert pa3._sentinel() == 8
        assert pa4._sentinel() == 9
        pa11 = pa1.map(lt3)
        pa12 = pa2.map(lt3)
        pa13 = pa3.map(lt3)
        pa14 = pa4.map(lt3)
        assert pa11 == PArray(1,2,-1,-1,-1,2,-1,-1,-1,-1)
        assert pa12 == PArray(0,1,2,-1,-1,1,2,-1,-1,-1)
        assert pa13 == PArray(2,8,8,8,8,8,8,8,8,8)
        assert pa14 == PArray(2,9,9,1,2,9,9,9)
        assert pa11._sentinel() == -1
        assert pa12._sentinel() == -1
        assert pa13._sentinel() == 8
        assert pa14._sentinel() == 9

        def bar(x: int) -> PArray[int, int]:
            return PArray(2, x, 3*x, size=4, sentinel=7*x)

        pa0 = PArray(1, 2, size=3, sentinel=-1)
        pa01 = pa0.mergeMap(bar)
        assert repr(pa01) == 'PArray(2, 2, 2, 1, 2, -1, 3, 6, -3, 7, 14, -7, size=12, sentinel=-1)'
        assert eval(repr(pa01)) == PArray(2, 2, 2, 1, 2, -1, 3, 6, -3, 7, 14, -7)

        pa02 = pa0.mergeMap(bar, size=15)
        assert repr(pa02) == 'PArray(2, 2, 2, 1, 2, -1, 3, 6, -3, 7, 14, -7, -1, -1, -1, size=15, sentinel=-1)'

        pa1 = PArray(1, 2, size=4, sentinel=-2, backlog=(9,10,11))
        pa11 = pa1.mergeMap(bar, size=11)
        assert repr(pa11) == 'PArray(2, 2, 2, 2, 1, 2, 9, 10, 3, 6, 27, size=11, sentinel=-2)'

        # Python always evaluates/assigns left to right
        pa11[0] = pa11[1] = pa11[2] = pa11[3] = None
        pa11[4] = pa11[5] = pa11[6] = pa11[7] = None
        pa11[8] = pa11[9] = pa11[10] = None
        assert repr(pa11) == 'PArray(30, 7, 14, 63, 70, -2, -2, -2, -2, -2, -2, size=11, sentinel=-2)'

    def test_exhaustMap(self) -> None:
        def le3(n: Any) -> int|None:
            if n <= 3:
                return n
            return None

        pa0 = PArray(*range(1, 6), sentinel=-1)
        assert pa0.sentinel() == -1
        pa1 = pa0.exhaustMap(lambda x: PArray(*range(x, x+2), sentinel=x+1))
        pa2 = pa0.exhaustMap(lambda x: PArray(*range(x-1, x+1), 42, sentinel=x*x))
        pa3 = pa0.exhaustMap(lambda x: PArray(*range(x+1, x+3)), sentinel=8)
        pa4 = pa0.exhaustMap(lambda x: PArray(*range(x), sentinel=-1), sentinel=10)
        pa5 = pa0.exhaustMap(lambda x: PArray(*range(x), sentinel=-1), size=8, sentinel=11)
        pa6 = pa0.exhaustMap(lambda x: PArray(*range(x), sentinel=-1), size=-8, sentinel=12)
        assert pa1 == PArray(1,2,3,4,5,2,3,4,5,6)
        assert pa2 == PArray(0,1,2,3,4,1,2,3,4,5,42,42,42,42,42)
        assert pa3 == PArray(2,3,4,5,6,3,4,5,6,7)
        assert pa4 == PArray(0,0,0,0,0,1,1,1,1,2,2,2,3,3,4)
        assert pa5 == PArray(0,0,0,0,0,1,1,1)
        assert pa6 == PArray(1,1,2,2,2,3,3,4)
        assert pa1._sentinel() == -1
        assert pa2._sentinel() == -1
        assert pa3._sentinel() == 8
        assert pa4._sentinel() == 10
        assert pa5._sentinel() == 11
        assert pa6._sentinel() == 12
        pa11 = pa1.map(le3)
        pa12 = pa2.map(le3)
        pa13 = pa3.map(le3)
        pa14 = pa4.map(le3)
        pa15 = pa5.map(le3)
        pa16 = pa6.map(le3)
        assert pa11 == PArray(1,2,3,-1,-1,2,3,-1,-1,-1)
        assert pa12 == PArray(0,1,2,3,-1,1,2,3,-1,-1,-1,-1,-1,-1,-1)
        assert pa13 == PArray(2,3,8,8,8,3,8,8,8,8)
        assert pa14 == PArray(0,0,0,0,0,1,1,1,1,2,2,2,3,3,10)
        assert pa15 == PArray(0,0,0,0,0,1,1,1)
        assert pa16 == PArray(1,1,2,2,2,3,3,12)
        assert pa11._sentinel() == -1
        assert pa12._sentinel() == -1
        assert pa13._sentinel() == 8
        assert pa14._sentinel() == 10
        assert pa15._sentinel() == 11
        assert pa16._sentinel() == 12

        def bar(x: int) -> PArray[int, int]:
            return PArray(*range(1, x+1), sentinel = 2*x)

        pa0 = PArray(1, 2, 3, sentinel=21)
        pa00 = pa0.exhaustMap(bar, size=8, mapsentinel=True)
        assert repr(pa00) == 'PArray(1, 1, 1, 2, 2, 3, 42, 42, size=8, sentinel=42)'
        assert eval(repr(pa00)) == PArray(1, 1, 1, 2, 2, 3, 42, 42)

        # Python always evaluates/assigns left to right
        pa00[0] = None
        pa00[4] = None
        assert pa00 == PArray(1, 1, 2, 42, 3, 42, 42, size=-8, sentinel=42)
        assert repr(pa00) == 'PArray(42, 1, 1, 2, 42, 3, 42, 42, size=8, sentinel=42)'
