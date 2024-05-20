import pickle
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os
import signal
import pytest
import threading
import platform
import hypothesis.strategies as st
from hypothesis import given, assume, settings, example

from .ellipticcurve import CurveFp, PointJacobi, INFINITY
from .ecdsa import (
    generator_256,
    curve_256,
    generator_224,
    generator_brainpoolp160r1,
    curve_brainpoolp160r1,
    generator_112r2,
    curve_112r2,
)
from .numbertheory import inverse_mod
from .util import randrange


NO_OLD_SETTINGS = {}
NO_OLD_SETTINGS["deadline"] = 5000


SLOW_SETTINGS = {}
if "--fast" in sys.argv:  # pragma: no cover
    SLOW_SETTINGS["max_examples"] = 2
else:
    SLOW_SETTINGS["max_examples"] = 10


class TestJacobi(unittest.TestCase):
    def test___init__(self):
        curve = object()
        x = 2
        y = 3
        z = 1
        order = 4
        pj = PointJacobi(curve, x, y, z, order)

        self.assertEqual(pj.order(), order)
        self.assertIs(pj.curve(), curve)
        self.assertEqual(pj.x(), x)
        self.assertEqual(pj.y(), y)

    def test_add_with_different_curves(self):
        p_a = PointJacobi.from_affine(generator_256)
        p_b = PointJacobi.from_affine(generator_224)

        with self.assertRaises(ValueError):  # pragma: no branch
            p_a + p_b

    def test_compare_different_curves(self):
        self.assertNotEqual(generator_256, generator_224)

    def test_equality_with_non_point(self):
        pj = PointJacobi.from_affine(generator_256)

        self.assertNotEqual(pj, "value")

    def test_conversion(self):
        pj = PointJacobi.from_affine(generator_256)
        pw = pj.to_affine()

        self.assertEqual(generator_256, pw)

    def test_single_double(self):
        pj = PointJacobi.from_affine(generator_256)
        pw = generator_256.double()

        pj = pj.double()

        self.assertEqual(pj.x(), pw.x())
        self.assertEqual(pj.y(), pw.y())

    def test_double_with_zero_point(self):
        pj = PointJacobi(curve_256, 0, 0, 1)

        pj = pj.double()

        self.assertIs(pj, INFINITY)

    def test_double_with_zero_equivalent_point(self):
        pj = PointJacobi(curve_256, 0, curve_256.p(), 1)

        pj = pj.double()

        self.assertIs(pj, INFINITY)

    def test_double_with_zero_equivalent_point_non_1_z(self):
        pj = PointJacobi(curve_256, 0, curve_256.p(), 2)

        pj = pj.double()

        self.assertIs(pj, INFINITY)

    def test_compare_with_affine_point(self):
        pj = PointJacobi.from_affine(generator_256)
        pa = pj.to_affine()

        self.assertEqual(pj, pa)
        self.assertEqual(pa, pj)

    def test_to_affine_with_zero_point(self):
        pj = PointJacobi(curve_256, 0, 0, 1)

        pa = pj.to_affine()

        self.assertIs(pa, INFINITY)

    def test_add_with_affine_point(self):
        pj = PointJacobi.from_affine(generator_256)
        pa = pj.to_affine()

        s = pj + pa

        self.assertEqual(s, pj.double())

    def test_radd_with_affine_point(self):
        pj = PointJacobi.from_affine(generator_256)
        pa = pj.to_affine()

        s = pa + pj

        self.assertEqual(s, pj.double())

    def test_add_with_infinity(self):
        pj = PointJacobi.from_affine(generator_256)

        s = pj + INFINITY

        self.assertEqual(s, pj)

    def test_add_zero_point_to_affine(self):
        pa = PointJacobi.from_affine(generator_256).to_affine()
        pj = PointJacobi(curve_256, 0, 0, 1)

        s = pj + pa

        self.assertIs(s, pa)

    def test_multiply_by_zero(self):
        pj = PointJacobi.from_affine(generator_256)

        pj = pj * 0

        self.assertIs(pj, INFINITY)

    def test_zero_point_multiply_by_one(self):
        pj = PointJacobi(curve_256, 0, 0, 1)

        pj = pj * 1

        self.assertIs(pj, INFINITY)

    def test_multiply_by_one(self):
        pj = PointJacobi.from_affine(generator_256)
        pw = generator_256 * 1

        pj = pj * 1

        self.assertEqual(pj.x(), pw.x())
        self.assertEqual(pj.y(), pw.y())

    def test_multiply_by_two(self):
        pj = PointJacobi.from_affine(generator_256)
        pw = generator_256 * 2

        pj = pj * 2

        self.assertEqual(pj.x(), pw.x())
        self.assertEqual(pj.y(), pw.y())

    def test_rmul_by_two(self):
        pj = PointJacobi.from_affine(generator_256)
        pw = generator_256 * 2

        pj = 2 * pj

        self.assertEqual(pj, pw)

    def test_compare_non_zero_with_infinity(self):
        pj = PointJacobi.from_affine(generator_256)

        self.assertNotEqual(pj, INFINITY)

    def test_compare_zero_point_with_infinity(self):
        pj = PointJacobi(curve_256, 0, 0, 1)

        self.assertEqual(pj, INFINITY)

    def test_compare_double_with_multiply(self):
        pj = PointJacobi.from_affine(generator_256)
        dbl = pj.double()
        mlpl = pj * 2

        self.assertEqual(dbl, mlpl)

    @settings(**SLOW_SETTINGS)
    @given(
        st.integers(
            min_value=0, max_value=int(generator_brainpoolp160r1.order() - 1)
        )
    )
    def test_multiplications(self, mul):
        pj = PointJacobi.from_affine(generator_brainpoolp160r1)
        pw = pj.to_affine() * mul

        pj = pj * mul

        self.assertEqual((pj.x(), pj.y()), (pw.x(), pw.y()))
        self.assertEqual(pj, pw)

    @settings(**SLOW_SETTINGS)
    @given(
        st.integers(
            min_value=0, max_value=int(generator_brainpoolp160r1.order() - 1)
        )
    )
    @example(0)
    @example(int(generator_brainpoolp160r1.order()))
    def test_precompute(self, mul):
        precomp = generator_brainpoolp160r1
        self.assertTrue(precomp._PointJacobi__precompute)
        pj = PointJacobi.from_affine(generator_brainpoolp160r1)

        a = precomp * mul
        b = pj * mul

        self.assertEqual(a, b)

    @settings(**SLOW_SETTINGS)
    @given(
        st.integers(
            min_value=1, max_value=int(generator_brainpoolp160r1.order() - 1)
        ),
        st.integers(
            min_value=1, max_value=int(generator_brainpoolp160r1.order() - 1)
        ),
    )
    @example(3, 3)
    def test_add_scaled_points(self, a_mul, b_mul):
        j_g = PointJacobi.from_affine(generator_brainpoolp160r1)
        a = PointJacobi.from_affine(j_g * a_mul)
        b = PointJacobi.from_affine(j_g * b_mul)

        c = a + b

        self.assertEqual(c, j_g * (a_mul + b_mul))

    @settings(**SLOW_SETTINGS)
    @given(
        st.integers(
            min_value=1, max_value=int(generator_brainpoolp160r1.order() - 1)
        ),
        st.integers(
            min_value=1, max_value=int(generator_brainpoolp160r1.order() - 1)
        ),
        st.integers(min_value=1, max_value=int(curve_brainpoolp160r1.p() - 1)),
    )
    def test_add_one_scaled_point(self, a_mul, b_mul, new_z):
        j_g = PointJacobi.from_affine(generator_brainpoolp160r1)
        a = PointJacobi.from_affine(j_g * a_mul)
        b = PointJacobi.from_affine(j_g * b_mul)

        p = curve_brainpoolp160r1.p()

        assume(inverse_mod(new_z, p))

        new_zz = new_z * new_z % p

        b = PointJacobi(
            curve_brainpoolp160r1,
            b.x() * new_zz % p,
            b.y() * new_zz * new_z % p,
            new_z,
        )

        c = a + b

        self.assertEqual(c, j_g * (a_mul + b_mul))

    @pytest.mark.slow
    @settings(**SLOW_SETTINGS)
    @given(
        st.integers(
            min_value=1, max_value=int(generator_brainpoolp160r1.order() - 1)
        ),
        st.integers(
            min_value=1, max_value=int(generator_brainpoolp160r1.order() - 1)
        ),
        st.integers(min_value=1, max_value=int(curve_brainpoolp160r1.p() - 1)),
    )
    @example(1, 1, 1)
    @example(3, 3, 3)
    @example(2, int(generator_brainpoolp160r1.order() - 2), 1)
    @example(2, int(generator_brainpoolp160r1.order() - 2), 3)
    def test_add_same_scale_points(self, a_mul, b_mul, new_z):
        j_g = PointJacobi.from_affine(generator_brainpoolp160r1)
        a = PointJacobi.from_affine(j_g * a_mul)
        b = PointJacobi.from_affine(j_g * b_mul)

        p = curve_brainpoolp160r1.p()

        assume(inverse_mod(new_z, p))

        new_zz = new_z * new_z % p

        a = PointJacobi(
            curve_brainpoolp160r1,
            a.x() * new_zz % p,
            a.y() * new_zz * new_z % p,
            new_z,
        )
        b = PointJacobi(
            curve_brainpoolp160r1,
            b.x() * new_zz % p,
            b.y() * new_zz * new_z % p,
            new_z,
        )

        c = a + b

        self.assertEqual(c, j_g * (a_mul + b_mul))

    def test_add_same_scale_points_static(self):
        j_g = generator_brainpoolp160r1
        p = curve_brainpoolp160r1.p()
        a = j_g * 11
        a.scale()
        z1 = 13
        x = PointJacobi(
            curve_brainpoolp160r1,
            a.x() * z1**2 % p,
            a.y() * z1**3 % p,
            z1,
        )
        y = PointJacobi(
            curve_brainpoolp160r1,
            a.x() * z1**2 % p,
            a.y() * z1**3 % p,
            z1,
        )

        c = a + a

        self.assertEqual(c, x + y)

    @pytest.mark.slow
    @settings(**SLOW_SETTINGS)
    @given(
        st.integers(
            min_value=1, max_value=int(generator_brainpoolp160r1.order() - 1)
        ),
        st.integers(
            min_value=1, max_value=int(generator_brainpoolp160r1.order() - 1)
        ),
        st.lists(
            st.integers(
                min_value=1, max_value=int(curve_brainpoolp160r1.p() - 1)
            ),
            min_size=2,
            max_size=2,
            unique=True,
        ),
    )
    @example(2, 2, [2, 1])
    @example(2, 2, [2, 3])
    @example(2, int(generator_brainpoolp160r1.order() - 2), [2, 3])
    @example(2, int(generator_brainpoolp160r1.order() - 2), [2, 1])
    def test_add_different_scale_points(self, a_mul, b_mul, new_z):
        j_g = PointJacobi.from_affine(generator_brainpoolp160r1)
        a = PointJacobi.from_affine(j_g * a_mul)
        b = PointJacobi.from_affine(j_g * b_mul)

        p = curve_brainpoolp160r1.p()

        assume(inverse_mod(new_z[0], p))
        assume(inverse_mod(new_z[1], p))

        new_zz0 = new_z[0] * new_z[0] % p
        new_zz1 = new_z[1] * new_z[1] % p

        a = PointJacobi(
            curve_brainpoolp160r1,
            a.x() * new_zz0 % p,
            a.y() * new_zz0 * new_z[0] % p,
            new_z[0],
        )
        b = PointJacobi(
            curve_brainpoolp160r1,
            b.x() * new_zz1 % p,
            b.y() * new_zz1 * new_z[1] % p,
            new_z[1],
        )

        c = a + b

        self.assertEqual(c, j_g * (a_mul + b_mul))

    def test_add_different_scale_points_static(self):
        j_g = generator_brainpoolp160r1
        p = curve_brainpoolp160r1.p()
        a = j_g * 11
        a.scale()
        z1 = 13
        x = PointJacobi(
            curve_brainpoolp160r1,
            a.x() * z1**2 % p,
            a.y() * z1**3 % p,
            z1,
        )
        z2 = 29
        y = PointJacobi(
            curve_brainpoolp160r1,
            a.x() * z2**2 % p,
            a.y() * z2**3 % p,
            z2,
        )

        c = a + a

        self.assertEqual(c, x + y)

    def test_add_different_points_same_scale_static(self):
        j_g = generator_brainpoolp160r1
        p = curve_brainpoolp160r1.p()
        a = j_g * 11
        a.scale()
        b = j_g * 12
        z = 13
        x = PointJacobi(
            curve_brainpoolp160r1,
            a.x() * z**2 % p,
            a.y() * z**3 % p,
            z,
        )
        y = PointJacobi(
            curve_brainpoolp160r1,
            b.x() * z**2 % p,
            b.y() * z**3 % p,
            z,
        )

        c = a + b

        self.assertEqual(c, x + y)

    def test_add_same_point_different_scale_second_z_1_static(self):
        j_g = generator_112r2
        p = curve_112r2.p()
        z = 11
        a = j_g * z
        a.scale()

        x = PointJacobi(
            curve_112r2,
            a.x() * z**2 % p,
            a.y() * z**3 % p,
            z,
        )
        y = PointJacobi(
            curve_112r2,
            a.x(),
            a.y(),
            1,
        )

        c = a + a

        self.assertEqual(c, x + y)

    def test_add_to_infinity_static(self):
        j_g = generator_112r2

        z = 11
        a = j_g * z
        a.scale()

        b = -a

        x = PointJacobi(
            curve_112r2,
            a.x(),
            a.y(),
            1,
        )
        y = PointJacobi(
            curve_112r2,
            b.x(),
            b.y(),
            1,
        )

        self.assertEqual(INFINITY, x + y)

    def test_add_point_3_times(self):
        j_g = PointJacobi.from_affine(generator_256)

        self.assertEqual(j_g * 3, j_g + j_g + j_g)

    def test_mul_without_order(self):
        j_g = PointJacobi(curve_256, generator_256.x(), generator_256.y(), 1)

        self.assertEqual(j_g * generator_256.order(), INFINITY)

    def test_mul_add_inf(self):
        j_g = PointJacobi.from_affine(generator_256)

        self.assertEqual(j_g, j_g.mul_add(1, INFINITY, 1))

    def test_mul_add_same(self):
        j_g = PointJacobi.from_affine(generator_256)

        self.assertEqual(j_g * 2, j_g.mul_add(1, j_g, 1))

    def test_mul_add_precompute(self):
        j_g = PointJacobi.from_affine(generator_brainpoolp160r1, True)
        b = PointJacobi.from_affine(j_g * 255, True)

        self.assertEqual(j_g * 256, j_g + b)
        self.assertEqual(j_g * (5 + 255 * 7), j_g * 5 + b * 7)
        self.assertEqual(j_g * (5 + 255 * 7), j_g.mul_add(5, b, 7))

    def test_mul_add_precompute_large(self):
        j_g = PointJacobi.from_affine(generator_brainpoolp160r1, True)
        b = PointJacobi.from_affine(j_g * 255, True)

        self.assertEqual(j_g * 256, j_g + b)
        self.assertEqual(
            j_g * (0xFF00 + 255 * 0xF0F0), j_g * 0xFF00 + b * 0xF0F0
        )
        self.assertEqual(
            j_g * (0xFF00 + 255 * 0xF0F0), j_g.mul_add(0xFF00, b, 0xF0F0)
        )

    def test_mul_add_to_mul(self):
        j_g = PointJacobi.from_affine(generator_256)

        a = j_g * 3
        b = j_g.mul_add(2, j_g, 1)

        self.assertEqual(a, b)

    def test_mul_add_differnt(self):
        j_g = PointJacobi.from_affine(generator_256)

        w_a = j_g * 2

        self.assertEqual(j_g.mul_add(1, w_a, 1), j_g * 3)

    def test_mul_add_slightly_different(self):
        j_g = PointJacobi.from_affine(generator_256)

        w_a = j_g * 2
        w_b = j_g * 3

        self.assertEqual(w_a.mul_add(1, w_b, 3), w_a * 1 + w_b * 3)

    def test_mul_add(self):
        j_g = PointJacobi.from_affine(generator_256)

        w_a = generator_256 * 255
        w_b = generator_256 * (0xA8 * 0xF0)
        j_b = j_g * 0xA8

        ret = j_g.mul_add(255, j_b, 0xF0)

        self.assertEqual(ret.to_affine(), w_a + w_b)

    def test_mul_add_large(self):
        j_g = PointJacobi.from_affine(generator_256)
        b = PointJacobi.from_affine(j_g * 255)

        self.assertEqual(j_g * 256, j_g + b)
        self.assertEqual(
            j_g * (0xFF00 + 255 * 0xF0F0), j_g * 0xFF00 + b * 0xF0F0
        )
        self.assertEqual(
            j_g * (0xFF00 + 255 * 0xF0F0), j_g.mul_add(0xFF00, b, 0xF0F0)
        )

    def test_mul_add_with_infinity_as_result(self):
        j_g = PointJacobi.from_affine(generator_256)

        order = generator_256.order()

        b = PointJacobi.from_affine(generator_256 * 256)

        self.assertEqual(j_g.mul_add(order % 256, b, order // 256), INFINITY)

    def test_mul_add_without_order(self):
        j_g = PointJacobi(curve_256, generator_256.x(), generator_256.y(), 1)

        order = generator_256.order()

        w_b = generator_256 * 34
        w_b.scale()

        b = PointJacobi(curve_256, w_b.x(), w_b.y(), 1)

        self.assertEqual(j_g.mul_add(order % 34, b, order // 34), INFINITY)

    def test_mul_add_with_doubled_negation_of_itself(self):
        j_g = PointJacobi.from_affine(generator_256 * 17)

        dbl_neg = 2 * (-j_g)

        self.assertEqual(j_g.mul_add(4, dbl_neg, 2), INFINITY)

    def test_equality(self):
        pj1 = PointJacobi(curve=CurveFp(23, 1, 1, 1), x=2, y=3, z=1, order=1)
        pj2 = PointJacobi(curve=CurveFp(23, 1, 1, 1), x=2, y=3, z=1, order=1)
        self.assertEqual(pj1, pj2)

    def test_equality_with_invalid_object(self):
        j_g = PointJacobi.from_affine(generator_256)

        self.assertNotEqual(j_g, 12)

    def test_equality_with_wrong_curves(self):
        p_a = PointJacobi.from_affine(generator_256)
        p_b = PointJacobi.from_affine(generator_224)

        self.assertNotEqual(p_a, p_b)

    def test_add_with_point_at_infinity(self):
        pj1 = PointJacobi(curve=CurveFp(23, 1, 1, 1), x=2, y=3, z=1, order=1)
        x, y, z = pj1._add(2, 3, 1, 5, 5, 0, 23)

        self.assertEqual((x, y, z), (2, 3, 1))

    def test_pickle(self):
        pj = PointJacobi(curve=CurveFp(23, 1, 1, 1), x=2, y=3, z=1, order=1)
        self.assertEqual(pickle.loads(pickle.dumps(pj)), pj)

    @pytest.mark.slow
    @settings(**NO_OLD_SETTINGS)
    @pytest.mark.skipif(
        platform.python_implementation() == "PyPy",
        reason="threading on PyPy breaks coverage",
    )
    @given(st.integers(min_value=1, max_value=10))
    def test_multithreading(self, thread_num):  # pragma: no cover
        # ensure that generator's precomputation table is filled
        generator_112r2 * 2

        # create a fresh point that doesn't have a filled precomputation table
        gen = generator_112r2
        gen = PointJacobi(gen.curve(), gen.x(), gen.y(), 1, gen.order(), True)

        self.assertEqual(gen._PointJacobi__precompute, [])

        def runner(generator):
            order = generator.order()
            for _ in range(10):
                generator * randrange(order)

        threads = []
        for _ in range(thread_num):
            threads.append(threading.Thread(target=runner, args=(gen,)))

        for t in threads:
            t.start()

        runner(gen)

        for t in threads:
            t.join()

        self.assertEqual(
            gen._PointJacobi__precompute,
            generator_112r2._PointJacobi__precompute,
        )

    @pytest.mark.slow
    @pytest.mark.skipif(
        platform.system() == "Windows"
        or platform.python_implementation() == "PyPy",
        reason="there are no signals on Windows, and threading breaks coverage"
        " on PyPy",
    )
    def test_multithreading_with_interrupts(self):  # pragma: no cover
        thread_num = 10
        # ensure that generator's precomputation table is filled
        generator_112r2 * 2

        # create a fresh point that doesn't have a filled precomputation table
        gen = generator_112r2
        gen = PointJacobi(gen.curve(), gen.x(), gen.y(), 1, gen.order(), True)

        self.assertEqual(gen._PointJacobi__precompute, [])

        def runner(generator):
            order = generator.order()
            for _ in range(50):
                generator * randrange(order)

        def interrupter(barrier_start, barrier_end, lock_exit):
            # wait until MainThread can handle KeyboardInterrupt
            barrier_start.release()
            barrier_end.acquire()
            os.kill(os.getpid(), signal.SIGINT)
            lock_exit.release()

        threads = []
        for _ in range(thread_num):
            threads.append(threading.Thread(target=runner, args=(gen,)))

        barrier_start = threading.Lock()
        barrier_start.acquire()
        barrier_end = threading.Lock()
        barrier_end.acquire()
        lock_exit = threading.Lock()
        lock_exit.acquire()

        threads.append(
            threading.Thread(
                target=interrupter,
                args=(barrier_start, barrier_end, lock_exit),
            )
        )

        for t in threads:
            t.start()

        with self.assertRaises(KeyboardInterrupt):
            # signal to interrupter that we can now handle the signal
            barrier_start.acquire()
            barrier_end.release()
            runner(gen)
            # use the lock to ensure we never go past the scope of
            # assertRaises before the os.kill is called
            lock_exit.acquire()

        for t in threads:
            t.join()

        self.assertEqual(
            gen._PointJacobi__precompute,
            generator_112r2._PointJacobi__precompute,
        )
