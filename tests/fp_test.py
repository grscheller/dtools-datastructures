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

from grscheller.datastructures import *

class Test_FP:
    def test_reduce(self):
        ft1 = FTuple(1,2,3,4,5)
        fs1 = FStack(1,2,3,4,5)
        pa1 = PArray(1,2,3,4,5)
        qft, qfs, qpa = FIFOQueue(), LIFOQueue(), FIFOQueue()
        l1 = lambda x, y: x + y
        l2 = lambda x, y: x * y
        l3 = lambda x, y: x.push(y)

        assert ft1.reduce(l1) == 15
        assert ft1.reduce(l1, 10) == 25
        assert ft1.reduce(l2) == 120
        assert ft1.reduce(l2, 10) == 1200
#        assert ft1.reduce(l3, FIFOQueue()) == FIFOQueue(1,2,3,4,5)

        assert fs1.reduce(l1) == 15
        assert fs1.reduce(l1, 10) == 25
        assert fs1.reduce(l2) == 120
        assert fs1.reduce(l2, 10) == 1200
#        assert fs1.reduce(l3, LIFOQueue()) == LIFOQueue(1,2,3,4,5)

        assert pa1.reduce(l1) == 15
        assert pa1.reduce(l1, 10) == 25
        assert pa1.reduce(l2) == 120
        assert pa1.reduce(l2, 10) == 1200
#        assert pa1.reduce(l3, FIFOQueue()) == FIFOQueue(1,2,3,4,5)

        assert ft1.accummulate(l1) == FTuple(1,3,6,10,15)
        assert ft1.accummulate(l1, 10) == FTuple(10,11,13,16,20,25)
        assert ft1.accummulate(initial=20) == FTuple(20,21,23,26,30,35)
        assert ft1.accummulate(l2) == FTuple(1,2,6,24,120)
        assert ft1.accummulate(l2, 10) == FTuple(10,10,20,60,240,1200)

        assert fs1.accummulate(l1) == FStack(5,9,12,14,15)
        assert fs1.accummulate(l1, 10) == FStack(10,15,19,22,24,25)
        assert fs1.accummulate(initial=20) == FStack(20,25,29,32,34,35)
        assert fs1.accummulate(l2) == FStack(5,20,60,120,120)
        assert fs1.accummulate(l2, 10) == FStack(10,50,200,600,1200,1200)

        assert pa1.accummulate(l1) == PArray(1,3,6,10,15)
        assert pa1.accummulate(l1, 10) == PArray(10,11,13,16,20,25)
        assert pa1.accummulate(initial=20) == PArray(20,21,23,26,30,35)
        assert pa1.accummulate(l2) == PArray(1,2,6,24,120)
        assert pa1.accummulate(l2, 10) == PArray(10,10,20,60,240,1200)

    def test_ftuple_inherited(self):
        ft = FTuple(*range(3, 1001))
        l1 = lambda x: 2*x + 1
        l2 = lambda x: FTuple(*range(1, x+1)).accummulate()
        ft1 = ft.map(l1)
        ft2 = ft.flatMap(l2)
        ft3 = ft.mergeMap(l2)
        ft4 = ft.exhaustMap(l2)
        assert (ft1[0], ft1[1], ft1[-1]) == (7, 9, 2001)
        assert (ft2[0], ft2[1], ft2[2]) == (1, 3, 6)
        assert (ft2[3], ft2[4], ft2[5], ft2[6])  == (1, 3, 6, 10)
        assert (ft2[7], ft2[8], ft2[9], ft2[10], ft2[11])  == (1, 3, 6, 10, 15)
        assert ft2[-1] == ft2[500496] == 500500
        assert ft2[500497] is None
        assert (ft3[0], ft3[1]) == (1, 1)
        assert (ft3[2], ft3[3]) == (1, 1)
        assert (ft3[4], ft3[5]) == (1, 1)
        assert (ft3[996], ft3[997]) == (1, 1)
        assert (ft3[998], ft3[999]) == (3, 3)
        assert (ft3[1994], ft3[1995]) == (3, 3)
        assert (ft3[1996], ft3[1997]) == (6, 6)
        assert ft3[-1] == ft3[2993] == 6
        assert ft3[2994] is None
        assert (ft4[0], ft4[1], ft4[2]) == (1, 1, 1)
        assert (ft4[995], ft4[996], ft4[997]) == (1, 1, 1)
        assert (ft4[998], ft4[999], ft4[1000]) == (3, 3, 3)
        assert (ft4[1992], ft4[1993], ft4[1995]) == (3, 3, 3)
        assert (ft4[1996], ft4[1997], ft4[1998]) == (6, 6, 6)
        assert ft2[-1] == ft2[500496] == 500500
        assert ft2[500497] is None
