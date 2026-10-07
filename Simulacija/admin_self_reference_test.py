"""
ADMIN — BLIND TEST FUNKCIONALNE SAMOREFERENCIJE

Pitanje:

MOZE LI MASINA BOLJE DA PREDVIDJA BUDUCE STANJE
AKO U MODEL UKLJUCI I SOPSTVENO UNUTRASNJE STANJE?

Testiramo:

    MODEL A:
        Y(t+1) = f(X_t)

    MODEL B:
        Y(t+1) = f(X_t, M_t)

gde je:

    X_t = spoljasnji ulaz
    M_t = unutrasnje stanje sistema
    Y(t+1) = buduci ishod koji treba predvideti

KLJUCNA KONTROLA:

- A i B vide potpuno iste dogadjaje.
- A i B imaju isti tip algoritma.
- A i B imaju isti trening/test raspored.
- Jedina namerna razlika je:
      B sme da koristi M_t.
      A ne sme.

VAZNO:

Generator sveta zna pravi zakon.

Procesori ga NE znaju.

Procesorima se ne daje formula generatora.

Parametri modela uce se samo iz TRAIN dela.

FINAL TEST se ne koristi za ucenje.

Dodatno pravimo SHUFFLED SELF kontrolu:

    MODEL C = f(X_t, shuffled(M_t))

C dobija isti broj ulaza kao B, ali je veza izmedju unutrasnjeg
stanja i odgovarajuceg dogadjaja namerno unistena.

Ako:

    B < A
i
    B < C

onda prednost ne dolazi samo od dodatne promenljive,
vec od INFORMACIJE koju nosi odgovarajuce unutrasnje stanje.

Ovo NIJE test svesti.

Ovo je test minimalnog funkcionalnog koraka:

    stanje onoga koji predvidja
    postaje korisna promenljiva
    u njegovom modelu buducnosti.

Requires:
    numpy

Run:
    python3 admin_self_reference_test.py
"""

import csv
import numpy as np


# ============================================================
# 1. PARAMETRI EKSPERIMENTA
# ============================================================

SEED = 314159

N_STEPS = 6000

TRAIN_END = 4000

TEST_START = 4000
TEST_END = 6000


# ------------------------------------------------------------
# Unutrasnje stanje M
# ------------------------------------------------------------
#
# M nije nasumicna etiketa.
#
# Ono ima sopstvenu dinamiku:
#
#   prethodno stanje
#   + spoljasnje opterecenje
#   + mali unutrasnji sum
#
# Zatim se ogranicava u fizicki dozvoljen opseg.
#

STATE_MEMORY = 0.92
STATE_INPUT_COUPLING = 0.16
STATE_NOISE = 0.04


# ------------------------------------------------------------
# Koliko unutrasnje stanje stvarno utice na buduci ishod.
#
# Ovo zna samo generator.
# Modeli ovaj broj NE dobijaju.
# ------------------------------------------------------------

TRUE_SELF_EFFECT = 0.75


# ------------------------------------------------------------
# Sum buduceg ishoda
# ------------------------------------------------------------

OUTPUT_NOISE = 0.08


# ------------------------------------------------------------
# Regularizacija linearne regresije
# ------------------------------------------------------------

RIDGE = 1e-8


# ------------------------------------------------------------
# Unapred definisani kriterijumi
# ------------------------------------------------------------

# B mora imati najmanje 10% manji test MSE od A.

MIN_ADVANTAGE_OVER_EXTERNAL = 0.10


# B mora imati najmanje 10% manji test MSE od shuffled-self
# kontrole.

MIN_ADVANTAGE_OVER_SHUFFLED = 0.10


# Prednost B mora postojati i u MAE.

MIN_MAE_ADVANTAGE = 0.05


# Permutacioni test.
#
# Null hipoteza:
# veza izmedju M_t i odgovarajuceg dogadjaja nije vazna.
#
# Koristimo 1000 permutacija test skupa.

N_PERMUTATIONS = 1000

ALPHA = 0.01


CSV_FILE = "ADMIN_SELF_REFERENCE_RESULTS.csv"


# ============================================================
# 2. GENERATOR SPOLJASNJEG SVETA
# ============================================================

def generate_external_world(rng):
    """
    X_t je spoljasnji svet.

    Kombinujemo vise ritmova i sum da ne bismo imali
    trivijalan konstantan ulaz.
    """

    t = np.arange(N_STEPS, dtype=float)

    phase1 = rng.uniform(0.0, 2.0 * np.pi)
    phase2 = rng.uniform(0.0, 2.0 * np.pi)

    x = (
        0.70 * np.sin(
            2.0 * np.pi * t / 73.0 + phase1
        )
        +
        0.35 * np.sin(
            2.0 * np.pi * t / 191.0 + phase2
        )
        +
        rng.normal(
            0.0,
            0.20,
            N_STEPS
        )
    )

    return x


# ============================================================
# 3. GENERATOR UNUTRASNJEG STANJA
# ============================================================

def generate_internal_state(x, rng):
    """
    Generise M_t.

    M ima memoriju.

    Na njega deluje spoljasnji svet,
    ali M nije isto sto i X.

    Zbog memorije i unutrasnjeg suma dva slicna X mogu
    zateci sistem u razlicitom unutrasnjem stanju.
    """

    m = np.zeros(
        N_STEPS,
        dtype=float
    )

    m[0] = rng.normal(
        0.0,
        0.25
    )

    for t in range(1, N_STEPS):

        m[t] = (
            STATE_MEMORY * m[t - 1]
            +
            STATE_INPUT_COUPLING * x[t - 1]
            +
            rng.normal(
                0.0,
                STATE_NOISE
            )
        )

        m[t] = np.clip(
            m[t],
            -2.0,
            2.0
        )

    return m


# ============================================================
# 4. GENERATOR BUDUCEG ISHODA
# ============================================================

def generate_future_outcome(x, m, rng):
    """
    Skriveni zakon generatora:

        Y(t+1) zavisi od:
            X_t
            M_t

    Modeli NE dobijaju ovu formulu.

    Vazna osobina:

    efekat X zavisi i od unutrasnjeg stanja.

    Zato isti ili slican X ne mora proizvesti isti Y
    kada je M drugaciji.
    """

    y = np.zeros(
        N_STEPS,
        dtype=float
    )

    for t in range(N_STEPS - 1):

        external_part = (
            0.65 * x[t]
            +
            0.18 * x[t] ** 2
        )

        internal_part = (
            TRUE_SELF_EFFECT * m[t]
        )

        interaction = (
            0.30 * x[t] * m[t]
        )

        y[t + 1] = (
            external_part
            +
            internal_part
            +
            interaction
            +
            rng.normal(
                0.0,
                OUTPUT_NOISE
            )
        )

    return y


# ============================================================
# 5. FEATURE MATRICE
# ============================================================

def external_features(x):
    """
    MODEL A vidi samo X.

    Dajemo mu dovoljno fleksibilnosti da nauci nelinearnost X,
    kako B ne bi pobedio samo zato sto A ima preslab model.
    """

    return np.column_stack([
        np.ones(len(x)),
        x,
        x ** 2,
        x ** 3
    ])


def self_features(x, m):
    """
    MODEL B vidi X i odgovarajuce unutrasnje stanje M.

    Ukljucujemo i interaction X*M.
    """

    return np.column_stack([
        np.ones(len(x)),
        x,
        x ** 2,
        x ** 3,
        m,
        m ** 2,
        x * m
    ])


# ============================================================
# 6. RIDGE REGRESIJA
# ============================================================

def fit_ridge(X, y):
    """
    Zatvorena forma.

    Intercept ne regularizujemo.
    """

    identity = np.eye(
        X.shape[1]
    )

    identity[0, 0] = 0.0

    beta = np.linalg.solve(
        X.T @ X
        + RIDGE * identity,
        X.T @ y
    )

    return beta


def predict(X, beta):
    return X @ beta


# ============================================================
# 7. METRIKE
# ============================================================

def mse(actual, predicted):
    return float(
        np.mean(
            (actual - predicted) ** 2
        )
    )


def mae(actual, predicted):
    return float(
        np.mean(
            np.abs(
                actual - predicted
            )
        )
    )


def percent_improvement(
    better,
    worse
):
    if worse <= 0.0:
        return np.nan

    return (
        (worse - better)
        / worse
        * 100.0
    )


# ============================================================
# 8. GLAVNI EKSPERIMENT
# ============================================================

def main():

    print("=" * 78)
    print(
        "ADMIN — BLIND TEST FUNKCIONALNE SAMOREFERENCIJE"
    )
    print("=" * 78)

    print()

    print(
        "Pitanje:"
    )

    print(
        "Da li informacija o sopstvenom unutrasnjem stanju "
        "poboljsava predvidjanje buduceg ishoda?"
    )

    print()

    print(
        "A = EXTERNAL ONLY     : koristi samo X_t"
    )

    print(
        "B = SELF STATE        : koristi X_t + M_t"
    )

    print(
        "C = SHUFFLED SELF     : koristi X_t + pogresno upareno M_t"
    )

    print()

    print(
        f"TRAIN: 0-{TRAIN_END - 1}"
    )

    print(
        f"BLIND TEST: {TEST_START}-{TEST_END - 1}"
    )

    print()


    # ========================================================
    # 9. GENERISI PODATKE
    # ========================================================

    rng = np.random.default_rng(
        SEED
    )

    x = generate_external_world(
        rng
    )

    m = generate_internal_state(
        x,
        rng
    )

    y = generate_future_outcome(
        x,
        m,
        rng
    )


    # --------------------------------------------------------
    # Predvidjamo Y[t+1] iz stanja u trenutku t.
    #
    # Zato poslednji t nema buduci target.
    # --------------------------------------------------------

    x_now = x[:-1]
    m_now = m[:-1]

    target = y[1:]


    # ========================================================
    # 10. TRAIN / TEST
    # ========================================================

    train_idx = np.arange(
        0,
        TRAIN_END
    )

    test_idx = np.arange(
        TEST_START,
        TEST_END - 1
    )


    x_train = x_now[train_idx]
    m_train = m_now[train_idx]
    y_train = target[train_idx]

    x_test = x_now[test_idx]
    m_test = m_now[test_idx]
    y_test = target[test_idx]


    # ========================================================
    # 11. SHUFFLED SELF KONTROLA
    # ========================================================
    #
    # Koristimo posebnu RNG granu.
    #
    # Mesamo M samo unutar TRAIN dela.
    #
    # Time C dobija dodatnu promenljivu iste raspodele,
    # ali ona vise nije pravilno povezana sa dogadjajem.
    # ========================================================

    shuffle_rng = np.random.default_rng(
        SEED + 1000
    )

    m_train_shuffled = (
        m_train.copy()
    )

    shuffle_rng.shuffle(
        m_train_shuffled
    )


    # ========================================================
    # 12. MATRICE
    # ========================================================

    XA_train = external_features(
        x_train
    )

    XA_test = external_features(
        x_test
    )


    XB_train = self_features(
        x_train,
        m_train
    )

    XB_test = self_features(
        x_test,
        m_test
    )


    XC_train = self_features(
        x_train,
        m_train_shuffled
    )


    # C na testu dobija M, ali njegov nauceni odnos prema M
    # potice iz pogresnog train uparivanja.
    #
    # To je kontrola za pitanje:
    #
    # "Da li je dovoljno samo dodati jos kolona?"
    #

    XC_test = self_features(
        x_test,
        m_test
    )


    # ========================================================
    # 13. UCENJE
    # ========================================================

    beta_A = fit_ridge(
        XA_train,
        y_train
    )

    beta_B = fit_ridge(
        XB_train,
        y_train
    )

    beta_C = fit_ridge(
        XC_train,
        y_train
    )


    # ========================================================
    # 14. BLIND PREDICTIONS
    # ========================================================

    pred_A = predict(
        XA_test,
        beta_A
    )

    pred_B = predict(
        XB_test,
        beta_B
    )

    pred_C = predict(
        XC_test,
        beta_C
    )


    # ========================================================
    # 15. METRIKE
    # ========================================================

    mse_A = mse(
        y_test,
        pred_A
    )

    mse_B = mse(
        y_test,
        pred_B
    )

    mse_C = mse(
        y_test,
        pred_C
    )


    mae_A = mae(
        y_test,
        pred_A
    )

    mae_B = mae(
        y_test,
        pred_B
    )

    mae_C = mae(
        y_test,
        pred_C
    )


    advantage_A = percent_improvement(
        mse_B,
        mse_A
    )

    advantage_C = percent_improvement(
        mse_B,
        mse_C
    )

    mae_advantage_A = percent_improvement(
        mae_B,
        mae_A
    )


    # ========================================================
    # 16. PERMUTACIONI TEST
    # ========================================================
    #
    # Ovo je dodatna nezavisna provera.
    #
    # Model B ostaje zamrznut.
    #
    # Na TEST skupu mesamo M izmedju dogadjaja.
    #
    # X ostaje isti.
    # Y ostaje isti.
    #
    # Ako odgovarajuce M stvarno nosi informaciju,
    # unistavanje njegovog uparivanja treba da poveca gresku.
    #
    # NISTA se ponovo ne trenira.
    # ========================================================

    permutation_rng = np.random.default_rng(
        SEED + 2000
    )

    permuted_mse = np.zeros(
        N_PERMUTATIONS,
        dtype=float
    )

    for i in range(
        N_PERMUTATIONS
    ):

        permuted_m = (
            m_test.copy()
        )

        permutation_rng.shuffle(
            permuted_m
        )

        X_perm = self_features(
            x_test,
            permuted_m
        )

        pred_perm = predict(
            X_perm,
            beta_B
        )

        permuted_mse[i] = mse(
            y_test,
            pred_perm
        )


    # Koliko permutacija je jednako dobra ili bolja
    # od pravilno uparenog M?

    p_value = (
        1
        + np.sum(
            permuted_mse
            <= mse_B
        )
    ) / (
        N_PERMUTATIONS + 1
    )


    median_permuted_mse = float(
        np.median(
            permuted_mse
        )
    )


    # ========================================================
    # 17. REZULTATI
    # ========================================================

    print("=" * 78)
    print("BLIND TEST REZULTATI")
    print("=" * 78)

    print()

    print(
        "MSE — manji broj je bolji"
    )

    print(
        f"  A external only = {mse_A:.8f}"
    )

    print(
        f"  B self state    = {mse_B:.8f}"
    )

    print(
        f"  C shuffled self = {mse_C:.8f}"
    )

    print()

    print(
        "MAE — manji broj je bolji"
    )

    print(
        f"  A external only = {mae_A:.8f}"
    )

    print(
        f"  B self state    = {mae_B:.8f}"
    )

    print(
        f"  C shuffled self = {mae_C:.8f}"
    )

    print()

    print(
        "Prednost B nad A po MSE:"
    )

    print(
        f"  {advantage_A:+.2f}%"
    )

    print()

    print(
        "Prednost B nad C po MSE:"
    )

    print(
        f"  {advantage_C:+.2f}%"
    )

    print()

    print(
        "Prednost B nad A po MAE:"
    )

    print(
        f"  {mae_advantage_A:+.2f}%"
    )

    print()

    print(
        "PERMUTACIONA KONTROLA"
    )

    print(
        f"  pravi M MSE      = {mse_B:.8f}"
    )

    print(
        f"  median shuffled  = "
        f"{median_permuted_mse:.8f}"
    )

    print(
        f"  p-value          = {p_value:.6f}"
    )

    print()


    # ========================================================
    # 18. UNAPRED DEFINISANI TESTOVI
    # ========================================================

    print("=" * 78)
    print("UNAPRED DEFINISANI TESTOVI")
    print("=" * 78)

    print()


    # --------------------------------------------------------
    # TEST 1
    #
    # Dodavanje pravog M mora poboljsati MSE najmanje 10%.
    # --------------------------------------------------------

    test1 = (
        advantage_A
        >=
        MIN_ADVANTAGE_OVER_EXTERNAL
        * 100.0
    )


    # --------------------------------------------------------
    # TEST 2
    #
    # Pravilno M mora biti bolje od shuffled-M modela.
    # --------------------------------------------------------

    test2 = (
        advantage_C
        >=
        MIN_ADVANTAGE_OVER_SHUFFLED
        * 100.0
    )


    # --------------------------------------------------------
    # TEST 3
    #
    # Efekat mora postojati i po drugoj metrici.
    # --------------------------------------------------------

    test3 = (
        mae_advantage_A
        >=
        MIN_MAE_ADVANTAGE
        * 100.0
    )


    # --------------------------------------------------------
    # TEST 4
    #
    # Permutaciona kontrola mora odbaciti slucajno uparivanje.
    # --------------------------------------------------------

    test4 = (
        p_value
        < ALPHA
    )


    # --------------------------------------------------------
    # TEST 5
    #
    # Apsolutna provera:
    # pravi M mora biti bolji od medijane permutovanih M.
    # --------------------------------------------------------

    test5 = (
        mse_B
        <
        median_permuted_mse
    )


    print(
        "TEST 1 — model sa unutrasnjim stanjem "
        "nadmasuje external-only model:"
        f" {'DA' if test1 else 'NE'}"
    )

    print(
        "TEST 2 — pravi M nadmasuje shuffled-self "
        "kontrolu:"
        f" {'DA' if test2 else 'NE'}"
    )

    print(
        "TEST 3 — prednost postoji i po MAE:"
        f" {'DA' if test3 else 'NE'}"
    )

    print(
        "TEST 4 — permutacioni test odbacuje "
        "slucajno uparivanje M:"
        f" {'DA' if test4 else 'NE'}"
    )

    print(
        "TEST 5 — pravi M je bolji od medijane "
        "permutovanih stanja:"
        f" {'DA' if test5 else 'NE'}"
    )


    # ========================================================
    # 19. CSV
    # ========================================================

    rows = []

    for i in range(
        len(test_idx)
    ):

        rows.append({

            "t":
                int(
                    test_idx[i]
                ),

            "X_t":
                float(
                    x_test[i]
                ),

            "M_t":
                float(
                    m_test[i]
                ),

            "Y_next":
                float(
                    y_test[i]
                ),

            "prediction_external_only":
                float(
                    pred_A[i]
                ),

            "prediction_self_state":
                float(
                    pred_B[i]
                ),

            "prediction_shuffled_self":
                float(
                    pred_C[i]
                ),

            "sq_error_external_only":
                float(
                    (
                        y_test[i]
                        - pred_A[i]
                    ) ** 2
                ),

            "sq_error_self_state":
                float(
                    (
                        y_test[i]
                        - pred_B[i]
                    ) ** 2
                ),

            "sq_error_shuffled_self":
                float(
                    (
                        y_test[i]
                        - pred_C[i]
                    ) ** 2
                ),
        })


    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=list(
                rows[0].keys()
            )
        )

        writer.writeheader()

        writer.writerows(
            rows
        )


    # ========================================================
    # 20. KONACNA OCENA
    # ========================================================

    tests = [
        test1,
        test2,
        test3,
        test4,
        test5
    ]

    passed = sum(
        tests
    )


    print()

    print("=" * 78)
    print("KONACNA OCENA")
    print("=" * 78)

    print()

    print(
        f"Proslo testova: "
        f"{passed}/{len(tests)}"
    )

    print()


    if all(tests):

        print(
            "REZULTAT: SVI UNAPRED DEFINISANI "
            "TESTOVI SU PROSLI."
        )

        print()

        print(
            "U ovom sintetickom eksperimentu "
            "informacija o unutrasnjem stanju "
            "sistema nosila je dodatnu prediktivnu "
            "vrednost koju spoljasnji ulaz sam nije imao."
        )

        print()

        print(
            "Prednost nije objasnjena samo dodavanjem "
            "jos jedne promenljive, jer je nestala kada "
            "je veza izmedju M_t i odgovarajuceg "
            "dogadjaja unistena mesanjem."
        )

        print()

        print(
            "Minimalni funkcionalni princip:"
        )

        print()

        print(
            "SPOLJASNJE STANJE + SOPSTVENO STANJE "
            "-> BOLJE PREDVIDJANJE"
        )

        print()

        print(
            "je demonstriran u ovom kontrolisanom "
            "sintetickom testu."
        )

    else:

        print(
            "REZULTAT: EKSPERIMENT NIJE PROSAO "
            "SVE UNAPRED DEFINISANE TESTOVE."
        )

        print()

        print(
            "Ne menjati pragove, generator ili kriterijume "
            "samo da bi rezultat postao pozitivan."
        )

        print(
            "Potrebno je utvrditi koji funkcionalni "
            "korak nije demonstriran."
        )


    print()

    print(
        "OGRANICENJE:"
    )

    print(
        "Ovaj eksperiment NE pokazuje svest, "
        "subjektivno iskustvo niti tvrdnju "
        "'JA POSTOJIM'."
    )

    print(
        "Pokazuje samo da predstavljanje sopstvenog "
        "unutrasnjeg stanja moze biti funkcionalno "
        "korisno za predvidjanje."
    )

    print()

    print(
        f"Detaljni rezultati: {CSV_FILE}"
    )


if __name__ == "__main__":
    main()