"""Admin: testable classical simulation of relational learning and feedback.
Requires numpy, scipy. Run: python admin_relational_simulation.py
This is NOT a quantum simulation or a physical model of the ionosphere.
"""
import numpy as np
from scipy.signal import butter, sosfiltfilt, hilbert

class RelationalSimulator:
    def __init__(self, fs=128, band=(7.0, 9.0), theta=0.70, seed=42):
        self.fs, self.band, self.theta = fs, band, theta
        self.rng = np.random.default_rng(seed)
        self.sos = butter(3, band, btype='bandpass', fs=fs, output='sos')
        self.memory = {}  # long-term learned expected PLV by channel pair
        self.count = {}   # number of observed windows per pair
        self.ram = {}     # transient current PLV / prediction error
        self.feedback = 0.0  # bounded threshold adjustment, not an electrical voltage
        self.history = []

    def gyre(self, signals):
        filtered = sosfiltfilt(self.sos, signals, axis=1)
        phase = np.angle(hilbert(filtered, axis=1))
        n = phase.shape[0]
        plvs = {}
        for i in range(n):
            for j in range(i + 1, n):
                # Ignore edge transients after filtering.
                delta = phase[i, self.fs:-self.fs] - phase[j, self.fs:-self.fs]
                plvs[(i, j)] = float(abs(np.mean(np.exp(1j * delta))))
        return plvs

    def step(self, signals, label):
        all_plvs = self.gyre(signals)
        # RAM -> GYRE: feedback affects next window's selection threshold.
        effective_theta = float(np.clip(self.theta + self.feedback, 0.45, 0.90))
        selected = {pair: p for pair, p in all_plvs.items() if p >= effective_theta}
        outcomes = {}
        errors = []
        for pair, observed in all_plvs.items():
            prior = self.memory.get(pair)
            error = None if prior is None else observed - prior
            if error is not None:
                errors.append(abs(error))
            # Three-state decisions need history; first observation is always open.
            if prior is None or self.count.get(pair, 0) < 2:
                state = 2
            elif observed >= effective_theta and prior >= effective_theta and abs(error) <= 0.20:
                state = 1
            elif observed < effective_theta and prior < effective_theta:
                state = 0
            else:
                state = 2
            # Learn even weak relationships: absence/decay is also information.
            rate = 0.35 if state == 2 else 0.20
            self.memory[pair] = observed if prior is None else (1-rate)*prior + rate*observed
            self.count[pair] = self.count.get(pair, 0) + 1
            outcomes[pair] = {'plv': observed, 'predicted': prior, 'error': error, 'state': state}
        mean_error = float(np.mean(errors)) if errors else 0.0
        # A simple toy controller: large prediction errors widen selection on NEXT step.
        # Bounded, smoothed response avoids unstable runaway feedback.
        target = -0.12 if mean_error > 0.20 else 0.0
        self.feedback = float(np.clip(0.7*self.feedback + 0.3*target, -0.12, 0.0))
        self.ram = {'current_plv': all_plvs, 'mean_error': mean_error,
                    'next_feedback': self.feedback}
        record = {'label': label, 'theta': effective_theta, 'selected': selected,
                  'outcomes': outcomes, 'mean_error': mean_error,
                  'next_feedback': self.feedback}
        self.history.append(record)
        return record


def make_signals(rng, fs=128, duration=8, disrupt=False):
    t = np.arange(int(fs*duration)) / fs
    # Channels 0 and 1: same 8 Hz carrier with stable phase offset.
    # Channel 2: phase relationship is disrupted later in the experiment.
    # Channel 3: independent narrowband noise (no intentionally locked phase).
    base = 2*np.pi*8*t
    x0 = np.sin(base) + 0.20*rng.normal(size=len(t))
    x1 = np.sin(base + 0.7) + 0.20*rng.normal(size=len(t))
    if disrupt:
        # Phase random walk: loses consistent phase locking to 0/1.
        drift = np.cumsum(rng.normal(0, 0.18, size=len(t)))
        x2 = np.sin(base + drift) + 0.20*rng.normal(size=len(t))
    else:
        x2 = np.sin(base + 1.3) + 0.20*rng.normal(size=len(t))
    x3 = rng.normal(size=len(t))
    return np.stack([x0, x1, x2, x3])


def main():
    sim = RelationalSimulator()
    labels = {0: 'ODBACI', 1: 'PRIHVATI', 2: 'OTVORENO'}
    print('ADMIN — SIMULACIJA ODNOSA I POVRATNE KONTROLE')
    print('Fizicki model: NE. Klasican algoritamski test: DA.\n')
    for k in range(10):
        disrupt = k >= 5
        result = sim.step(make_signals(sim.rng, disrupt=disrupt),
                          'PROMENA' if disrupt else 'STABILNO')
        print(f"Korak {k+1:2d} | {result['label']:8s} | prag={result['theta']:.2f} | "
              f"izdvojeno={len(result['selected'])} | greska={result['mean_error']:.3f} | "
              f"RAM->gyre={result['next_feedback']:+.3f}")
        for pair in [(0, 1), (0, 2), (0, 3)]:
            r = result['outcomes'][pair]
            pred = 'nema' if r['predicted'] is None else f"{r['predicted']:.2f}"
            print(f"  {pair}: PLV={r['plv']:.2f} ocekivano={pred:>4s} {labels[r['state']]}")
    assert sim.history[2]['outcomes'][(0, 1)]['state'] == 1, 'Stable pair should be accepted'
    assert sim.history[-1]['outcomes'][(0, 1)]['plv'] > 0.90, 'Stable pair lost phase lock'
    assert sim.history[4]['outcomes'][(0, 2)]['plv'] > 0.90, 'Baseline pair not locked'
    assert any(r['mean_error'] > 0.20 for r in sim.history[5:]), 'Change not detected'
    assert any(r['next_feedback'] < 0 for r in sim.history[5:]), 'Feedback not activated'
    print('\nTESTOVI PROSLI: stabilna veza, promena odnosa i povratna kontrola.')

if __name__ == '__main__':
    main()
