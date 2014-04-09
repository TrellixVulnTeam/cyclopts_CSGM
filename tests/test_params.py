from cyclopts.params import Incrementer, ReactorRequestSampler
from nose.tools import assert_equal, assert_almost_equal, assert_true, assert_false

def test_incr():
    i = Incrementer()
    assert_equal(i.next(), 0)
    i = Incrementer(5)
    assert_equal(i.next(), 5)
    assert_equal(i.next(), 6)

def test_default_rxtr_req():
    s = ReactorRequestSampler()
    assert_equal(1, s.n_commods.sample())
    assert_equal(1, s.n_request.sample())
    assert_equal(1, s.assem_per_req.sample())
    assert_equal(0, s.req_multi_frac.sample())
    assert_equal(1, s.req_multi_commods.sample())
    assert_false(s.exclusive.sample())
    assert_equal(0, s.n_req_constr.sample())
    assert_equal(1, s.n_supply.sample())
    assert_equal(0, s.sup_multi_frac.sample())
    assert_equal(1, s.sup_multi_commods.sample())
    assert_equal(1, s.n_sup_constr.sample())
    assert_equal(1, s.sup_constr_val.sample())
    assert_true(s.connection.sample())
    constr_avg = 0
    pref_avg = 0
    n = 1000
    for i in range(n):
        constr = s.constr_coeff.sample()
        constr_avg += constr
        assert_true(constr > 0)
        assert_true(constr <= 1)
        pref = s.pref_coeff.sample()
        pref_avg += pref
        assert_true(pref > 0)
        assert_true(pref <= 1)
    assert_almost_equal(0.5, constr_avg / n, places=1)
    assert_almost_equal(0.5, pref_avg / n, places=1)
