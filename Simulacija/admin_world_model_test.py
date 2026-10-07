"""
ADMIN — BLIND TEST IZGRADNJE I ADAPTACIJE MODELA

Cilj:
Testirati funkcionalni ciklus:

ISKUSTVO
    ->
OBRAZAC / MODEL
    ->
PREDVIDJANJE
    ->
NEOCEKIVANA PROMENA PRENOSA
    ->
PREDICTION ERROR / SURPRISE
    ->
PROMENA MODELA
    ->
BOLJE BUDUCE PREDVIDJANJE

Eksperiment koristi TRI procesora:

A) LEARNING
   Uci pre i posle promene magistrale.

B) NEVER_LEARN
   Nikada ne uci.

C) FREEZE_AT_CHANGE
   Uci identicno kao A do trenutka promene.
   Od tog trenutka njegov model je zamrznut.

A i C zato imaju ISTU istoriju i ISTI model neposredno
pre promene.

Posle promene jedina namerna razlika je:

    A sme da menja model.
    C ne sme.

Dodatno cuvamo COUNTERFACTUAL signal:

    - sta bi magistrala prenela da nije promenjena
    - sta je prenela nakon promene

Counterfactual se koristi SAMO ZA NAKNADNU EVALUACIJU.
Procesori A, B i C ga nikada ne vide.

VAZNO:

1. Predvidjanje se pravi PRE nego sto stigne observation[t].
2. Model se menja TEK NAKON merenja greske.
3. Procesor ne zna formule generatora sveta.
4. Procesor ne zna kada ce se magistrala promeniti.
5. Procesor ne dobija counterfactual.
6. Kriterijumi testa su definisani unapred.
7. Skripta sme da vrati NE.

Ovo je klasican algoritamski eksperiment.
Nije dokaz fizicke gyre, magistrale ili prirodnog racunara.

Requires:
    numpy

Run:
    python3 admin_world_model_test.py
"""

import csv
import numpy as np


# ============================================================
# 1. FIKSIRANI PARAMETRI EKSPERIMENTA
# ============================================================

SEED = 42

N_STEPS = 900
N_SIGNALS = 12

CHANGE_STEP = 480
CHANGED_CHANNEL = 3

# ------------------------------------------------------------
# Promena magistrale
# ------------------------------------------------------------
#
# Ovo nije nasumicni sum.
#
# Magistrala prelazi iz jednog deterministickog rezima prenosa
# u drugi.
#
# Zato test ne zavisi od pretpostavke:
#
#     "novi signal mora biti losiji"
#
# vec proverava:
#
#     "da li se promenio odnos izmedju naucenog modela
#      i onoga sto sada stize?"
#

NEW_GAIN = 0.55
NEW_OFFSET = 0.28
NEW_DELAY = 2


# ------------------------------------------------------------
# Model
# ------------------------------------------------------------

LEARNING_RATE = 0.08
TREND_WEIGHT = 0.35


# ------------------------------------------------------------
# Prozori za evaluaciju
# ------------------------------------------------------------

BASELINE_START = 400
BASELINE_END = 480

# Prvih 10 koraka nakon promene.
# Ovo NIJE jedini test "surprise".
EARLY_CHANGE_START = 480
EARLY_CHANGE_END = 490

EARLY_ADAPT_START = 490
EARLY_ADAPT_END = 540

LATE_ADAPT_START = 540
LATE_ADAPT_END = 650

FINAL_TEST_START = 700
FINAL_TEST_END = 900


# ------------------------------------------------------------
# Pragovi unapred definisanih testova
# ------------------------------------------------------------
#
# Ne menjati ih nakon gledanja rezultata samo da bi test prosao.
#

# A i C moraju biti numericki identicni pre promene.
IDENTICAL_TOLERANCE = 1e-12

# Novi rezim magistrale mora stvarno promeniti signal.
MIN_COUNTERFACTUAL_EFFECT = 1e-6

# Adaptacija mora dati najmanje 10% bolju gresku
# od zamrznutog identicnog modela na promenjenom kanalu.
MIN_ADAPTIVE_ADVANTAGE = 0.10

# Nauceni model pre promene mora biti najmanje 5% bolji
# od sistema koji nikada nije ucio.
MIN_LEARNING_ADVANTAGE = 0.05

# Kasna adaptacija mora imati najmanje 10% manju gresku
# od zamrznutog modela.
MIN_LATE_ADVANTAGE = 0.10


CSV_FILE = "ADMIN_WORLD_MODEL_RESULTS.csv"


# ============================================================
# 2. GENERATOR SKRIVENOG SVETA
# ============================================================

def generate_world(seed=SEED):
    """
    Generise sinteticki svet.

    Generator zna njegove skrivene zakone.

    ADMIN procesori ih NE znaju.

    Procesori dobijaju samo niz brojeva koji stize kroz
    magistrale.
    """

    rng = np.random.default_rng(seed)

    world = np.zeros(
        (N_STEPS, N_SIGNALS),
        dtype=float
    )

    phases = rng.uniform(
        0.0,
        2.0 * np.pi,
        N_SIGNALS
    )

    for t in range(N_STEPS):

        # ----------------------------------------------------
        # 0 — periodicni odnos
        # ----------------------------------------------------

        world[t, 0] = (
            0.50
            + 0.22
            * np.sin(
                2 * np.pi * t / 55.0
                + phases[0]
            )
            + rng.normal(0, 0.025)
        )

        # ----------------------------------------------------
        # 1 — drugi periodicni odnos
        # ----------------------------------------------------

        world[t, 1] = (
            0.48
            + 0.18
            * np.sin(
                2 * np.pi * t / 83.0
                + phases[1]
            )
            + rng.normal(0, 0.025)
        )

        # ----------------------------------------------------
        # 2 — kombinacija dva ritma
        # ----------------------------------------------------

        world[t, 2] = (
            0.52
            + 0.12
            * np.sin(
                2 * np.pi * t / 41.0
                + phases[2]
            )
            + 0.07
            * np.sin(
                2 * np.pi * t / 113.0
            )
            + rng.normal(0, 0.025)
        )

        # ----------------------------------------------------
        # 3 — signal cija ce MAGISTRALA promeniti prenos
        # ----------------------------------------------------

        world[t, 3] = (
            0.50
            + 0.20
            * np.sin(
                2 * np.pi * t / 67.0
                + phases[3]
            )
            + rng.normal(0, 0.020)
        )

        # ----------------------------------------------------
        # 4 — drift + oscilacija
        # ----------------------------------------------------

        world[t, 4] = (
            0.35
            + 0.00035 * t
            + 0.08
            * np.sin(
                2 * np.pi * t / 120.0
                + phases[4]
            )
            + rng.normal(0, 0.020)
        )

        # ----------------------------------------------------
        # 5 — odnos povezan sa drugim signalima
        # ----------------------------------------------------

        world[t, 5] = (
            0.30
            + 0.35 * world[t, 0]
            + 0.20 * world[t, 1]
            + rng.normal(0, 0.018)
        )

        # ----------------------------------------------------
        # 6 — sporiji ritam
        # ----------------------------------------------------

        world[t, 6] = (
            0.55
            + 0.14
            * np.sin(
                2 * np.pi * t / 145.0
                + phases[6]
            )
            + rng.normal(0, 0.020)
        )

        # ----------------------------------------------------
        # 7 — slozeniji predvidljiv odnos
        # ----------------------------------------------------

        world[t, 7] = (
            0.50
            + 0.10
            * np.sin(
                2 * np.pi * t / 31.0
            )
            + 0.08
            * np.sin(
                2 * np.pi * t / 79.0
                + phases[7]
            )
            + rng.normal(0, 0.025)
        )

        # ----------------------------------------------------
        # 8 — autoregresivni odnos
        # ----------------------------------------------------

        if t == 0:

            world[t, 8] = (
                0.50
                + rng.normal(0, 0.03)
            )

        else:

            world[t, 8] = (
                0.88 * world[t - 1, 8]
                + 0.12 * 0.50
                + rng.normal(0, 0.025)
            )

        # ----------------------------------------------------
        # 9 — jos jedan strukturisan odnos
        # ----------------------------------------------------

        world[t, 9] = (
            0.45
            + 0.16
            * np.cos(
                2 * np.pi * t / 97.0
                + phases[9]
            )
            + rng.normal(0, 0.022)
        )

        # ----------------------------------------------------
        # 10 i 11 — slabo predvidljivi odnosi
        # ----------------------------------------------------

        world[t, 10] = (
            0.50
            + rng.normal(0, 0.12)
        )

        world[t, 11] = (
            0.50
            + rng.normal(0, 0.15)
        )

    return world


# ============================================================
# 3. MAGISTRALE
# ============================================================

def build_magistrale(world):
    """
    Vraca dva niza:

    normal:
        sta bi stiglo da se magistrala nikada nije promenila

    changed:
        ono sto stvarno dajemo procesorima u eksperimentu

    Procesori vide SAMO changed.

    normal posle CHANGE_STEP postoji samo kao counterfactual
    kontrola za evaluaciju.
    """

    normal = world.copy()
    changed = world.copy()

    for t in range(CHANGE_STEP, N_STEPS):

        source_t = max(
            0,
            t - NEW_DELAY
        )

        changed[t, CHANGED_CHANNEL] = (
            NEW_GAIN
            * world[source_t, CHANGED_CHANNEL]
            + NEW_OFFSET
        )

    return normal, changed


# ============================================================
# 4. MODEL
# ============================================================

class WorldModel:

    def __init__(
        self,
        name,
        can_learn=True
    ):

        self.name = name
        self.can_learn = can_learn

        self.level = np.full(
            N_SIGNALS,
            0.5,
            dtype=float
        )

        self.trend = np.zeros(
            N_SIGNALS,
            dtype=float
        )

        self.last_observation = None

        self.initialized = False


    def predict(self):
        """
        Predikcija nastaje ISKLJUCIVO iz prethodnog stanja.

        Tek nakon ove funkcije sme da stigne observation[t].
        """

        return (
            self.level
            + TREND_WEIGHT * self.trend
        ).copy()


    def observe(
        self,
        observation,
        learning_allowed=True
    ):
        """
        Model vidi podatak tek NAKON sto je predikcija vec
        napravljena i greska izmerena.
        """

        if not self.can_learn:
            return

        if not learning_allowed:
            return

        if not self.initialized:

            self.level = observation.copy()

            self.last_observation = (
                observation.copy()
            )

            self.initialized = True

            return

        difference = (
            observation
            - self.level
        )

        self.level = (
            self.level
            + LEARNING_RATE * difference
        )

        if self.last_observation is not None:

            instantaneous_trend = (
                observation
                - self.last_observation
            )

            self.trend = (
                (1.0 - LEARNING_RATE)
                * self.trend
                + LEARNING_RATE
                * instantaneous_trend
            )

        self.last_observation = (
            observation.copy()
        )


# ============================================================
# 5. POMOCNE FUNKCIJE
# ============================================================

def squared_error(predicted, actual):

    return (
        predicted - actual
    ) ** 2


def mse(predicted, actual):

    return float(
        np.mean(
            squared_error(
                predicted,
                actual
            )
        )
    )


def mean_slice(
    values,
    start,
    end
):

    return float(
        np.mean(
            np.asarray(
                values,
                dtype=float
            )[start:end]
        )
    )


def percent_better(
    better,
    worse
):

    if worse <= 0:
        return np.nan

    return (
        (worse - better)
        / worse
        * 100.0
    )


# ============================================================
# 6. GLAVNI EKSPERIMENT
# ============================================================

def main():

    print("=" * 78)
    print(
        "ADMIN — BLIND TEST: "
        "ISKUSTVO -> MODEL -> GRESKA -> ADAPTACIJA"
    )
    print("=" * 78)

    print()

    print(
        "Procesori ne znaju pravila generatora sveta."
    )

    print(
        "Procesori ne znaju kada ce magistrala promeniti rezim."
    )

    print(
        "Counterfactual postoji samo za evaluaciju "
        "i nikada se ne daje procesorima."
    )

    print()

    print(
        "A = LEARNING          "
        "uci pre i posle promene"
    )

    print(
        "B = NEVER_LEARN       "
        "nikada ne uci"
    )

    print(
        "C = FREEZE_AT_CHANGE  "
        "uci do promene, zatim se zamrzava"
    )

    print()

    print(
        f"Promena magistrale: "
        f"korak {CHANGE_STEP}, "
        f"kanal {CHANGED_CHANNEL}"
    )

    print()


    # ========================================================
    # SVET
    # ========================================================

    world = generate_world()

    counterfactual, observed = (
        build_magistrale(world)
    )


    # ========================================================
    # MODELI
    # ========================================================

    A = WorldModel(
        "LEARNING",
        can_learn=True
    )

    B = WorldModel(
        "NEVER_LEARN",
        can_learn=False
    )

    C = WorldModel(
        "FREEZE_AT_CHANGE",
        can_learn=True
    )


    # ========================================================
    # ISTORIJA
    # ========================================================

    error_A = []
    error_B = []
    error_C = []

    channel_error_A = []
    channel_error_B = []
    channel_error_C = []

    counterfactual_effect = []

    # Posebna mera:
    #
    # koliko je prediction error veci/manji zbog promene
    # magistrale u odnosu na ono sto bi ISTI model imao da
    # magistrala nije promenjena.
    #
    # Ovo se racuna samo naknadno.
    surprise_due_to_change_A = []
    surprise_due_to_change_C = []

    rows = []


    # ========================================================
    # SIMULACIJA
    # ========================================================

    for t in range(N_STEPS):

        actual = observed[t]

        cf = counterfactual[t]


        # ----------------------------------------------------
        # 1. PREDVIDJANJE
        # ----------------------------------------------------
        #
        # Nijedan model jos nije video actual[t].
        #

        pred_A = A.predict()
        pred_B = B.predict()
        pred_C = C.predict()


        # ----------------------------------------------------
        # 2. GRESKA PRE UCENJA
        # ----------------------------------------------------

        eA = mse(
            pred_A,
            actual
        )

        eB = mse(
            pred_B,
            actual
        )

        eC = mse(
            pred_C,
            actual
        )

        error_A.append(eA)
        error_B.append(eB)
        error_C.append(eC)


        # ----------------------------------------------------
        # Promenjeni kanal
        # ----------------------------------------------------

        ch = CHANGED_CHANNEL

        ceA = float(
            (
                pred_A[ch]
                - actual[ch]
            ) ** 2
        )

        ceB = float(
            (
                pred_B[ch]
                - actual[ch]
            ) ** 2
        )

        ceC = float(
            (
                pred_C[ch]
                - actual[ch]
            ) ** 2
        )

        channel_error_A.append(ceA)
        channel_error_B.append(ceB)
        channel_error_C.append(ceC)


        # ----------------------------------------------------
        # 3. COUNTERFACTUAL EFEKAT MAGISTRALE
        # ----------------------------------------------------
        #
        # Koliko se ono sto STVARNO stize razlikuje od onoga
        # sto bi stiglo bez promene magistrale.
        #
        # Model ovo NE vidi.
        #

        cf_effect = float(
            (
                actual[ch]
                - cf[ch]
            ) ** 2
        )

        counterfactual_effect.append(
            cf_effect
        )


        # ----------------------------------------------------
        # 4. SURPRISE KOJI JE IZAZVALA SAMA PROMENA
        # ----------------------------------------------------
        #
        # Ista predikcija se poredi sa:
        #
        #   a) stvarnim novim prenosom
        #   b) counterfactual starim prenosom
        #
        # Razlika govori koliko je sama promena magistrale
        # promenila prediction error.
        #
        # Ovo je evaluator.
        # ADMIN ne dobija ovaj podatak.
        #

        cf_error_A = float(
            (
                pred_A[ch]
                - cf[ch]
            ) ** 2
        )

        cf_error_C = float(
            (
                pred_C[ch]
                - cf[ch]
            ) ** 2
        )

        surprise_A = (
            ceA - cf_error_A
        )

        surprise_C = (
            ceC - cf_error_C
        )

        surprise_due_to_change_A.append(
            surprise_A
        )

        surprise_due_to_change_C.append(
            surprise_C
        )


        # ----------------------------------------------------
        # Faza
        # ----------------------------------------------------

        if t < CHANGE_STEP:

            phase = "PRE_CHANGE"

        elif (
            EARLY_CHANGE_START
            <= t
            < EARLY_CHANGE_END
        ):

            phase = "IMMEDIATE_CHANGE"

        elif (
            EARLY_ADAPT_START
            <= t
            < EARLY_ADAPT_END
        ):

            phase = "EARLY_ADAPTATION"

        elif (
            LATE_ADAPT_START
            <= t
            < LATE_ADAPT_END
        ):

            phase = "LATE_ADAPTATION"

        elif (
            FINAL_TEST_START
            <= t
            < FINAL_TEST_END
        ):

            phase = "FINAL_TEST"

        else:

            phase = "TRANSITION"


        # ----------------------------------------------------
        # Sacuvaj rezultat PRE UCENJA
        # ----------------------------------------------------

        rows.append({

            "step":
                t,

            "phase":
                phase,

            "actual_changed_channel":
                actual[ch],

            "counterfactual_channel":
                cf[ch],

            "counterfactual_effect":
                cf_effect,

            "prediction_A":
                pred_A[ch],

            "prediction_B":
                pred_B[ch],

            "prediction_C":
                pred_C[ch],

            "world_mse_A":
                eA,

            "world_mse_B":
                eB,

            "world_mse_C":
                eC,

            "channel_mse_A":
                ceA,

            "channel_mse_B":
                ceB,

            "channel_mse_C":
                ceC,

            "counterfactual_prediction_error_A":
                cf_error_A,

            "counterfactual_prediction_error_C":
                cf_error_C,

            "surprise_due_to_change_A":
                surprise_A,

            "surprise_due_to_change_C":
                surprise_C,
        })


        # ----------------------------------------------------
        # 5. TEK SADA UCENJE
        # ----------------------------------------------------

        A.observe(
            actual,
            learning_allowed=True
        )

        B.observe(
            actual,
            learning_allowed=False
        )

        C.observe(
            actual,
            learning_allowed=(
                t < CHANGE_STEP
            )
        )


    # ========================================================
    # 7. ANALIZA
    # ========================================================

    baseline_A = mean_slice(
        error_A,
        BASELINE_START,
        BASELINE_END
    )

    baseline_B = mean_slice(
        error_B,
        BASELINE_START,
        BASELINE_END
    )

    baseline_C = mean_slice(
        error_C,
        BASELINE_START,
        BASELINE_END
    )


    baseline_ch_A = mean_slice(
        channel_error_A,
        BASELINE_START,
        BASELINE_END
    )

    baseline_ch_C = mean_slice(
        channel_error_C,
        BASELINE_START,
        BASELINE_END
    )


    immediate_ch_A = mean_slice(
        channel_error_A,
        EARLY_CHANGE_START,
        EARLY_CHANGE_END
    )

    immediate_ch_C = mean_slice(
        channel_error_C,
        EARLY_CHANGE_START,
        EARLY_CHANGE_END
    )


    early_ch_A = mean_slice(
        channel_error_A,
        EARLY_ADAPT_START,
        EARLY_ADAPT_END
    )

    early_ch_C = mean_slice(
        channel_error_C,
        EARLY_ADAPT_START,
        EARLY_ADAPT_END
    )


    late_ch_A = mean_slice(
        channel_error_A,
        LATE_ADAPT_START,
        LATE_ADAPT_END
    )

    late_ch_C = mean_slice(
        channel_error_C,
        LATE_ADAPT_START,
        LATE_ADAPT_END
    )


    final_A = mean_slice(
        error_A,
        FINAL_TEST_START,
        FINAL_TEST_END
    )

    final_B = mean_slice(
        error_B,
        FINAL_TEST_START,
        FINAL_TEST_END
    )

    final_C = mean_slice(
        error_C,
        FINAL_TEST_START,
        FINAL_TEST_END
    )


    final_ch_A = mean_slice(
        channel_error_A,
        FINAL_TEST_START,
        FINAL_TEST_END
    )

    final_ch_C = mean_slice(
        channel_error_C,
        FINAL_TEST_START,
        FINAL_TEST_END
    )


    cf_effect_after_change = mean_slice(
        counterfactual_effect,
        CHANGE_STEP,
        FINAL_TEST_END
    )


    immediate_surprise_A = mean_slice(
        surprise_due_to_change_A,
        EARLY_CHANGE_START,
        EARLY_CHANGE_END
    )


    immediate_surprise_C = mean_slice(
        surprise_due_to_change_C,
        EARLY_CHANGE_START,
        EARLY_CHANGE_END
    )


    # ========================================================
    # 8. PRIKAZ
    # ========================================================

    print("=" * 78)
    print("REZULTATI")
    print("=" * 78)

    print()

    print(
        f"PRE PROMENE — ceo svet"
    )

    print(
        f"  A learning       = "
        f"{baseline_A:.6f}"
    )

    print(
        f"  B never learn    = "
        f"{baseline_B:.6f}"
    )

    print(
        f"  C freeze later   = "
        f"{baseline_C:.6f}"
    )

    print()

    print(
        "PRE PROMENE — kanal magistrale"
    )

    print(
        f"  A = {baseline_ch_A:.6f}"
    )

    print(
        f"  C = {baseline_ch_C:.6f}"
    )

    print()

    print(
        "NEPOSREDNO POSLE PROMENE — kanal"
    )

    print(
        f"  A = {immediate_ch_A:.6f}"
    )

    print(
        f"  C = {immediate_ch_C:.6f}"
    )

    print()

    print(
        "RANA ADAPTACIJA — kanal"
    )

    print(
        f"  A = {early_ch_A:.6f}"
    )

    print(
        f"  C = {early_ch_C:.6f}"
    )

    print()

    print(
        "KASNA ADAPTACIJA — kanal"
    )

    print(
        f"  A = {late_ch_A:.6f}"
    )

    print(
        f"  C = {late_ch_C:.6f}"
    )

    print()

    print(
        "KASNI TEST — kanal"
    )

    print(
        f"  A = {final_ch_A:.6f}"
    )

    print(
        f"  C = {final_ch_C:.6f}"
    )

    print()

    print(
        "KASNI TEST — ceo svet"
    )

    print(
        f"  A = {final_A:.6f}"
    )

    print(
        f"  B = {final_B:.6f}"
    )

    print(
        f"  C = {final_C:.6f}"
    )

    print()

    print(
        "COUNTERFACTUAL PROVERA"
    )

    print(
        "  prosecna fizicka promena prenosa "
        f"= {cf_effect_after_change:.6f}"
    )

    print(
        "  surprise zbog promene, "
        f"A prvih 10 koraka = "
        f"{immediate_surprise_A:+.6f}"
    )

    print(
        "  surprise zbog promene, "
        f"C prvih 10 koraka = "
        f"{immediate_surprise_C:+.6f}"
    )


    # ========================================================
    # 9. TESTOVI
    # ========================================================

    print()

    print("=" * 78)
    print("UNAPRED DEFINISANI TESTOVI")
    print("=" * 78)

    print()


    # --------------------------------------------------------
    # TEST 1
    #
    # A i C moraju imati istu istoriju pre promene.
    # --------------------------------------------------------

    test1 = (
        abs(
            baseline_A
            - baseline_C
        )
        <= IDENTICAL_TOLERANCE
    )


    # --------------------------------------------------------
    # TEST 2
    #
    # Magistrala se zaista mora promeniti.
    #
    # Ovo ne zahteva da prediction MSE mora obavezno porasti.
    # Samo proverava da eksperimentalna intervencija postoji.
    # --------------------------------------------------------

    test2 = (
        cf_effect_after_change
        > MIN_COUNTERFACTUAL_EFFECT
    )


    # --------------------------------------------------------
    # TEST 3
    #
    # Pre promene nauceni model mora imati prediktivnu vrednost
    # u odnosu na model koji nikada ne uci.
    # --------------------------------------------------------

    pre_learning_advantage = (
        percent_better(
            baseline_A,
            baseline_B
        )
    )

    test3 = (
        pre_learning_advantage
        >= MIN_LEARNING_ADVANTAGE * 100.0
    )


    # --------------------------------------------------------
    # TEST 4
    #
    # Nakon promene, A i C krecu iz iste naucene istorije.
    #
    # Kasnije A mora biti bolji jer sme da promeni model.
    # --------------------------------------------------------

    adaptive_advantage = (
        percent_better(
            final_ch_A,
            final_ch_C
        )
    )

    test4 = (
        adaptive_advantage
        >= MIN_ADAPTIVE_ADVANTAGE * 100.0
    )


    # --------------------------------------------------------
    # TEST 5
    #
    # Isti zahtev proveravamo u ranijoj/kasnoj fazi adaptacije.
    # --------------------------------------------------------

    late_advantage = (
        percent_better(
            late_ch_A,
            late_ch_C
        )
    )

    test5 = (
        late_advantage
        >= MIN_LATE_ADVANTAGE * 100.0
    )


    # --------------------------------------------------------
    # TEST 6
    #
    # A mora biti bolji i od sistema koji nikada nije ucio
    # na kasnom out-of-sample prozoru.
    # --------------------------------------------------------

    final_world_advantage = (
        percent_better(
            final_A,
            final_B
        )
    )

    test6 = (
        final_world_advantage
        >= MIN_LEARNING_ADVANTAGE * 100.0
    )


    # --------------------------------------------------------
    # TEST 7 — SURPRISE
    #
    # Ovde NE zahtevamo:
    #
    #     novi MSE > stari MSE
    #
    # jer promena moze slucajno da ucini signal lakse
    # predvidljivim.
    #
    # Umesto toga proveravamo da li promena magistrale menja
    # prediction error u odnosu na counterfactual stari rezim.
    #
    # Apsolutna razlika mora biti nenulta.
    # --------------------------------------------------------

    test7 = (
        abs(
            immediate_surprise_C
        )
        > MIN_COUNTERFACTUAL_EFFECT
    )


    # ========================================================
    # 10. STAMPA TESTOVA
    # ========================================================

    print(
        "TEST 1 — A i C imaju identican model "
        "pre promene: "
        f"{'DA' if test1 else 'NE'}"
    )

    print(
        "TEST 2 — intervencija je zaista promenila "
        "prenos magistrale: "
        f"{'DA' if test2 else 'NE'}"
    )

    print(
        "TEST 3 — iskustvo poboljsava predvidjanje "
        "pre promene: "
        f"{'DA' if test3 else 'NE'}"
    )

    print(
        "TEST 4 — adaptivni model nadmasuje "
        "identican zamrznuti model posle promene: "
        f"{'DA' if test4 else 'NE'}"
    )

    print(
        "TEST 5 — prednost adaptacije postoji "
        "vec u kasnoj fazi adaptacije: "
        f"{'DA' if test5 else 'NE'}"
    )

    print(
        "TEST 6 — nauceni model nadmasuje "
        "never-learn kontrolu na kasnom testu: "
        f"{'DA' if test6 else 'NE'}"
    )

    print(
        "TEST 7 — promena magistrale menja "
        "prediction error u odnosu na "
        "counterfactual stari rezim: "
        f"{'DA' if test7 else 'NE'}"
    )


    # ========================================================
    # 11. VELICINA EFEKTA
    # ========================================================

    print()

    print("=" * 78)
    print("VELICINA EFEKTA")
    print("=" * 78)

    print()

    print(
        "Prednost ucenja pre promene "
        "u odnosu na NEVER_LEARN:"
    )

    print(
        f"  {pre_learning_advantage:+.2f}%"
    )

    print()

    print(
        "Prednost adaptivnog modela nad "
        "zamrznutim modelom na kasnom testu "
        "promenjene magistrale:"
    )

    print(
        f"  {adaptive_advantage:+.2f}%"
    )

    print()

    print(
        "Prednost tokom kasne adaptacije:"
    )

    print(
        f"  {late_advantage:+.2f}%"
    )

    print()

    print(
        "Prednost naucenog modela nad "
        "NEVER_LEARN na kasnom testu celog sveta:"
    )

    print(
        f"  {final_world_advantage:+.2f}%"
    )


    # ========================================================
    # 12. CSV
    # ========================================================

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

        writer.writerows(rows)


    # ========================================================
    # 13. KONACNA OCENA
    # ========================================================

    tests = [
        test1,
        test2,
        test3,
        test4,
        test5,
        test6,
        test7
    ]

    passed = sum(tests)


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
            "U ovom sintetickom eksperimentu:"
        )

        print()

        print(
            "1. iskustvo je proizvelo model sa "
            "prediktivnom vrednoscu;"
        )

        print(
            "2. magistrala je promenila rezim prenosa;"
        )

        print(
            "3. promena je promenila odnos izmedju "
            "predikcije i pristiglog signala;"
        )

        print(
            "4. sistem kome je dozvoljeno dalje "
            "ucenje promenio je model;"
        )

        print(
            "5. isti prethodno nauceni model koji je "
            "zamrznut nije ostvario istu buducu tacnost."
        )

        print()

        print(
            "Funkcionalni ciklus:"
        )

        print()

        print(
            "ISKUSTVO -> MODEL -> PREDVIDJANJE -> "
            "PROMENA -> GRESKA -> PROMENA MODELA"
        )

        print()

        print(
            "je algoritamski ostvariv u ovom "
            "kontrolisanom sintetickom eksperimentu."
        )

    else:

        print(
            "REZULTAT: EKSPERIMENT NIJE PROSAO "
            "SVE UNAPRED DEFINISANE TESTOVE."
        )

        print()

        print(
            "Ne menjati pragove ili pravila samo da "
            "bi rezultat postao pozitivan."
        )

        print(
            "Potrebno je utvrditi koji funkcionalni "
            "korak nije demonstriran."
        )


    print()

    print(
        "NAPOMENA:"
    )

    print(
        "Ovaj rezultat moze pokazati samo "
        "algoritamsku mogucnost predlozenog principa."
    )

    print(
        "Ne dokazuje da prirodna gyre, magistrale, "
        "RAM ili centralni procesor fizicki rade "
        "na ovaj nacin."
    )

    print()

    print(
        f"Detaljni rezultati: {CSV_FILE}"
    )


if __name__ == "__main__":
    main()