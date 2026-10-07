"""Small dependency-light diagnostics for GammaCAdam claims.

This reproduces the mathematical scalar updates; it does not run the PyTorch
implementation because PyTorch is unavailable in this workspace.
"""
import math


def moment_trace(grads, beta1=0.9, beta2=0.999, eps=1e-8):
    m = v = 0.0
    trace = []
    for t, g in enumerate(grads, 1):
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * g * g
        mh = m / (1 - beta1**t)
        vh = v / (1 - beta2**t)
        trace.append((mh, vh, mh * mh / (vh + eps)))
    return trace


def gamma_lr_decay(s, eta0=1e-3, decay0=.01, target=.5,
                   k_eta=1.5, k_decay=2.):
    eta = eta0 / math.sqrt(1 + k_eta * max(s - target, 0))
    decay = decay0 * math.exp(k_decay * (s - target))
    return eta, decay, 1 - eta * decay


def run():
    zero_then_spike = moment_trace([0.] * 10000 + [1.])[-1]
    alternating = moment_trace([(-1.)**t for t in range(10000)])[-1]
    steady = moment_trace([1.] * 10000)[-1]
    print('10k zero gradients, then spike: mhat,vhat,S=', zero_then_spike)
    print('10k alternating gradients: mhat,vhat,S=', alternating)
    print('10k steady gradients: mhat,vhat,S=', steady)
    print('first nonzero step S=', moment_trace([1.])[0][-1])
    for label, s in [('steady', steady[-1]), ('alternating', alternating[-1]),
                     ('spike', zero_then_spike[-1])]:
        eta, decay, gamma = gamma_lr_decay(s)
        print(label, 'eta,decay,gamma=', (eta, decay, gamma))
    # Same gradient and weight can coexist with any positive quadratic
    # curvature by moving its center: L_h(w)=h/2*(w-a_h)^2, a_h=1-1/h.
    for h in [1., 10., 1000., 1000000.]:
        w = 1.
        center = 1 - 1 / h
        grad = h * (w - center)
        proxy = abs(grad) / (abs(w) + 1e-8)
        print('curvature example h,center,grad,proxy=',
              (h, center, grad, proxy))
    # Generalized first-step effective rate and the GD bound are independent
    # of the measured S at fixed first-step gradient.
    eta1, _, _ = gamma_lr_decay(moment_trace([1.])[0][-1])
    for h in [100., 10000.]:
        print('GD heuristic h, eta1, 2/h, eta1<2/h=',
              (h, eta1, 2/h, eta1 < 2/h))


if __name__ == '__main__':
    run()
