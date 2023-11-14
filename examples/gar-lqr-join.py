"""
Define two successive LQ problems and "fuse" them together by maximizing over the common Lagrange multiplier.
"""
from proxddp import gar
from eigenpy import LDLT

import numpy as np
import matplotlib.pyplot as plt


np.random.seed(42)
nx = nu = 1

x0 = np.random.randn(nx)
xf = np.ones(nx)

xbar = np.zeros(nx)

A = 1.2 * np.eye(nx)
B = np.eye(nx, nu)
f = np.zeros(nx)
Q = np.eye(nx, nx) * 0.01
Qf = np.eye(nx) * 1.0
E = -np.eye(nx)


def knot_get_default(nx, nu, nc):
    knot = gar.LQRKnot(nx, nu, nc)
    knot.Q[:] = Q
    knot.q[:] = -Q @ xbar
    knot.R[:] = np.eye(nu) * 0.1
    knot.A[:] = A
    knot.B[:] = B
    knot.E[:] = E
    return knot


T_all = 10
t0 = T_all // 2
knots = []
for t in range(t0):
    knots.append(knot_get_default(nx, nu, 0))


mu = 1e-10

prob1 = gar.LQRProblem(knots, nx)
prob1.G0 = -np.eye(nx)
prob1.g0 = x0
prob1.addParameterization(nx)
knots1 = prob1.stages
knots1[-1].Gammath = -mu * np.eye(nx)
knots1[-1].Gammax = A.T
knots1[-1].Gammau = B.T
knots1[-1].gamma = f

solver1 = gar.ProximalRiccatiSolver(prob1)
solver1.backward(mu, mu)


prob2 = gar.LQRProblem(knots, 0)
prob2.stages.append(knot_get_default(nx, 0, 0))
prob2.addParameterization(nx)
knots2 = prob2.stages
knots2[0].Gammax = E.T
knots2[-1].Q[:] = Qf
knots2[-1].q[:] = -Qf @ xf

assert prob1.horizon + prob2.horizon + 1 == T_all, "Got {}, expected {}".format(
    prob1.horizon + prob2.horizon, T_all
)

solver2 = gar.ProximalRiccatiSolver(prob2)
solver2.backward(mu, mu)

sol1 = gar.lqrInitializeSolution(prob1)
sol2 = gar.lqrInitializeSolution(prob2)

# Here, theta is a Lagrange multiplier

H = solver1.thHess + solver2.thHess
g = solver1.thGrad + solver2.thGrad
print("Hth:", H)
print("gth:", g)

thopt = LDLT(H).solve(-g)
thopt = thopt[0]
print("thopt = costate[t0]:", thopt)

solver1.forward(**sol1, theta=thopt)
solver2.forward(**sol2, theta=thopt)
xs1 = sol1["xs"]
us1 = sol1["us"]
ls1 = sol1["lbdas"]

xs2 = sol2["xs"]
us2 = sol2["us"]
ls2 = sol2["lbdas"]

prob3 = prob1.copy()
for kn in knots2:
    prob3.stages.append(kn)
prob3.addParameterization(0)
solver3 = gar.ProximalRiccatiSolver(prob3)
solver3.backward(mu, mu)
sol3 = gar.lqrInitializeSolution(prob3)
solver3.forward(**sol3)

xs3 = sol3["xs"]
us3 = sol3["us"]


# compute error
def computeError():
    kn: gar.LQRKnot = knots1[t0 - 1]
    knp = knots1[-2]
    x_ = xs1[t0 - 1]
    u_ = us1[t0 - 1]
    lp_ = ls1[t0 - 1]
    dynerr_ = kn.A @ x_ + kn.B @ u_ + kn.f + kn.E @ xs2[0]
    gu = kn.r + kn.S.T @ x_ + kn.R @ u_ + kn.B.T @ thopt
    gx = kn.q + kn.Q @ x_ + kn.S @ u_ + kn.A.T @ thopt
    gx += knp.E.T @ lp_
    # first leg
    vm0 = solver1.datas[0].vm
    _L0 = vm0.Lmat
    _err = vm0.Pmat @ xs2[0] + vm0.pvec + _L0 @ thopt
    _err0 = vm0.Pmat @ solver1.kkt0.ff(0, 0) + vm0.pvec
    print("knots1::initerr", _err)
    print("knots1::initerr_0", _err0)
    print("Dyn err:", dynerr_)
    print("gu:", gu)
    print("gx:", gx)
    # second leg
    knn: gar.LQRKnot = knots2[0]
    gxn = knn.q + knn.Q @ xs2[0] + knn.S @ us2[0] + knn.A.T @ ls2[1]
    gxn += kn.E.T @ thopt
    print("gxn:", gxn)
    vm0: gar.value_data = solver2.datas[0].vm
    _L0 = vm0.Lmat
    _err = vm0.Pmat @ xs2[0] + vm0.pvec + _L0 @ thopt
    print("knots2::L0", _L0)
    print("knots2::initerr", _err)


computeError()


print("T_total:", T_all)
print("sum horizons:", prob1.horizon + prob2.horizon)

ts1 = np.arange(0, t0)
ts2 = np.arange(t0, T_all + 1)
times = np.concatenate([ts1, ts2])

assert ts1.size == len(xs1)
assert ts2.size == len(xs2)

plt.figure()
plt.subplot(2, 1, 1)
ax = plt.gca()
ax.xaxis.set_major_locator(plt.MultipleLocator(1))
plt.title("States $x_t$")
plt.plot(times, xs3, marker=".", label="true", lw=4.0, alpha=0.4, c="g")
plt.plot(ts1, xs1, marker=".", label="1st leg")
plt.plot(ts2, xs2, marker=".", label="2nd leg")

plt.subplot(2, 1, 2)
plt.title("Controls $u_t$")
plt.plot(times[:T_all], us3, marker=".", label="true", lw=4.0, alpha=0.4, c="g")
plt.plot(ts1, us1, marker=".", label="1st leg")
plt.plot(ts2[:-1], us2, marker=".", label="2nd leg")

plt.legend()

plt.tight_layout()
plt.show()
