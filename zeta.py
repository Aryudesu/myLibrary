import mpmath as mp


def setup_precision(dps=100):
    mp.mp.dps = dps
setup_precision(120)

PI = mp.pi

def theta(t):
    z = mp.mpf('0.25') + 0.5j * t
    return mp.arg(mp.gamma(z)) - 0.5*t*mp.log(mp.pi)

def Z(t):
    s = mp.mpf('0.5') + 1j*t
    return mp.re(mp.e**(1j*theta(t)) * mp.zeta(s))

def avg_spacing(t):
    t = mp.mpf(t)
    return (2*PI) / mp.log(t/(2*PI))

def scan_brackets_adaptive(f, tmin, tmax, alpha=0.3):
    t = mp.mpf(tmin)
    f_prev = f(t)
    brackets = []
    while t < tmax:
        h = alpha * avg_spacing(max(t, 10))
        t_next = min(t + h, tmax)
        f_next = f(t_next)
        if f_prev * f_next <= 0:
            brackets.append((t, f_prev, t_next, f_next))
        t, f_prev = t_next, f_next
    return brackets

def refine_root(f, a, b, fa=None, fb=None, tol=mp.mpf('1e-90')):
    if fa is None: fa = f(a)
    if fb is None: fb = f(b)
    left, right = mp.mpf(a), mp.mpf(b)
    fl, fr = fa, fb
    for _ in range(400):
        mid = (left + right)/2
        fm = f(mid)
        if abs(fm) < tol or (right-left)/2 < tol:
            x0, f0 = left, fl
            x1, f1 = right, fr
            for __ in range(5):
                if f1 == f0: break
                x2 = x1 - f1*(x1-x0)/(f1-f0)
                if not (left <= x2 <= right): break
                f2 = f(x2)
                x0, f0, x1, f1 = x1, f1, x2, f2
            return x1 if left <= x1 <= right else mid
        if fl*fm <= 0:
            right, fr = mid, fm
        else:
            left, fl = mid, fm
    return (left+right)/2

def zeros_in_range(tmin, tmax, dps=120, alpha=0.3, tol_exp=-100):
    setup_precision(dps)
    br = scan_brackets_adaptive(Z, tmin, tmax, alpha=alpha)
    zeros = []
    for (a,fa,b,fb) in br:
        if fa*fb > 0:
            continue
        z = refine_root(Z, a, b, fa, fb, tol=mp.mpf(10)**tol_exp)
        zeros.append(z)
    cleaned = []
    for z in sorted(zeros):
        if not cleaned or abs(z - cleaned[-1]) > mp.mpf('1e-20'):
            cleaned.append(z)
    return cleaned

zeros = zeros_in_range(0, 100)
for z in zeros:
    print(z)
