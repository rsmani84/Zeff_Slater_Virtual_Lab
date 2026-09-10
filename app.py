import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Zeff Virtual Lab",
    page_icon="⚛️",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("⚛️ Virtual Chemistry Laboratory")

st.subheader(
    "Problems on Calculation of Effective Nuclear Charge (Zeff) "
    "Using Slater's Rules"
)

st.divider()

# --------------------------------------------------
# SIDEBAR MENU
# --------------------------------------------------

st.sidebar.title("🧪 Virtual Lab Menu")

menu = st.sidebar.radio(
    "Select an Activity",
    [
        "🏠 Home",
        "📚 Theory",
        "📖 Slater's Rules",
        "🧮 Zeff Calculator",
        "📝 Practice Problems"
    ]
)

# ==================================================
# HOME PAGE
# ==================================================

if menu == "🏠 Home":

    st.header("Welcome to the Virtual Laboratory")

    st.write("""
    This virtual laboratory helps students understand and solve problems
    related to the calculation of Effective Nuclear Charge (Zeff)
    using Slater's Rules.
    """)

    st.info("""
    ### Learning Objectives

    After completing this virtual lab, students will be able to:

    • Understand the concept of shielding effect.

    • Understand effective nuclear charge.

    • Apply Slater's Rules.

    • Calculate the shielding constant (S).

    • Calculate the effective nuclear charge (Zeff).
    """)

    st.latex(r"Z_{eff} = Z - S")

    st.success("Select an activity from the sidebar to begin!")

# ==================================================
# THEORY PAGE
# ==================================================

elif menu == "📚 Theory":

    st.header("📚 Effective Nuclear Charge")

    st.write("""
    In a multi-electron atom, electrons are attracted by the positively
    charged nucleus. However, inner electrons partially block or shield
    the nuclear attraction experienced by outer electrons.
    """)

    st.subheader("Shielding Effect")

    st.write("""
    The reduction in the attractive force between the nucleus and an outer
    electron due to the presence of inner electrons is called the
    shielding effect.
    """)

    st.subheader("Effective Nuclear Charge")

    st.write("""
    The actual positive charge experienced by an electron in a
    multi-electron atom is called the Effective Nuclear Charge.
    """)

    st.latex(r"Z_{eff} = Z - S")

    st.write("""
    Where:

    Z = Atomic number

    S = Shielding constant

    Zeff = Effective nuclear charge
    """)

# ==================================================
# SLATER'S RULES
# ==================================================

elif menu == "📖 Slater's Rules":

    st.header("📖 Slater's Rules")

    st.subheader("For ns and np Electrons")

    st.write("""
    Electrons are arranged into the following groups:
    """)

    st.code("""
(1s)
(2s, 2p)
(3s, 3p)
(3d)
(4s, 4p)
(4d)
(4f)
(5s, 5p)
    """)

    st.markdown("""
    ### Shielding Contributions

    **1. Other electrons in the same ns/np group**

    Contribution = **0.35 each**

    For 1s electrons = **0.30 each**

    **2. Electrons in the (n−1) shell**

    Contribution = **0.85 each**

    **3. Electrons in the (n−2) or lower shells**

    Contribution = **1.00 each**
    """)

    st.divider()

    st.subheader("For nd and nf Electrons")

    st.markdown("""
    **Other electrons in the same nd/nf group**

    Contribution = **0.35 each**

    **Electrons to the left**

    Contribution = **1.00 each**

    **Electrons to the right**

    Contribution = **0.00**
    """)

# ==================================================
# ZEFF CALCULATOR
# ==================================================

elif menu == "🧮 Zeff Calculator":

    st.header("🧮 Zeff Calculator")

    st.write("""
    Enter the required values and calculate the
    Effective Nuclear Charge.
    """)

    col1, col2 = st.columns(2)

    with col1:

        Z = st.number_input(
            "Atomic Number (Z)",
            min_value=1,
            max_value=100,
            value=11
        )

        same_group = st.number_input(
            "Number of other electrons in the same group",
            min_value=0,
            value=0
        )

    with col2:

        n_minus_1 = st.number_input(
            "Number of electrons in (n−1) shell",
            min_value=0,
            value=8
        )

        lower_shell = st.number_input(
            "Number of electrons in (n−2) or lower shells",
            min_value=0,
            value=2
        )

    electron_type = st.selectbox(
        "Select Electron Type",
        [
            "ns / np electron",
            "nd / nf electron"
        ]
    )

    if st.button("⚡ Calculate Zeff"):

        if electron_type == "ns / np electron":

            S = (
                same_group * 0.35
                + n_minus_1 * 0.85
                + lower_shell * 1.00
            )

        else:

            S = (
                same_group * 0.35
                + n_minus_1 * 1.00
                + lower_shell * 1.00
            )

        Zeff = Z - S

        st.divider()

        st.success("Calculation Completed Successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Shielding Constant (S)",
                f"{S:.2f}"
            )

        with col2:
            st.metric(
                "Effective Nuclear Charge (Zeff)",
                f"{Zeff:.2f}"
            )

        st.subheader("Step-by-Step Calculation")

        st.write(f"### Step 1: Atomic Number")

        st.write(f"Z = **{Z}**")

        st.write("### Step 2: Calculate Shielding Constant")

        if electron_type == "ns / np electron":

            st.write(
                f"S = ({same_group} × 0.35) + "
                f"({n_minus_1} × 0.85) + "
                f"({lower_shell} × 1.00)"
            )

        else:

            st.write(
                f"S = ({same_group} × 0.35) + "
                f"({n_minus_1} × 1.00) + "
                f"({lower_shell} × 1.00)"
            )

        st.write(f"### Step 3: Shielding Constant")

        st.write(f"S = **{S:.2f}**")

        st.write("### Step 4: Calculate Effective Nuclear Charge")

        st.latex(
            rf"Z_{{eff}} = {Z} - {S:.2f}"
        )

        st.latex(
            rf"Z_{{eff}} = {Zeff:.2f}"
        )

# ==================================================
# PRACTICE PROBLEMS
# ==================================================

elif menu == "📝 Practice Problems":

    st.header("📝 Practice Problems")

    problems = {

        "Problem 1: Sodium (Na)": {
            "question": """
            Calculate the Effective Nuclear Charge (Zeff)
            experienced by the 3s electron of Sodium (Na).
            """,
            "answer": """
            Sodium: Z = 11

            Electron configuration:

            1s² 2s² 2p⁶ 3s¹

            Shielding:

            (2 × 1.00) + (8 × 0.85)

            S = 2 + 6.8

            S = 8.8

            Zeff = Z − S

            Zeff = 11 − 8.8

            Zeff = 2.2
            """
        },

        "Problem 2: Oxygen (O)": {
            "question": """
            Calculate Zeff experienced by a 2p electron
            in Oxygen.
            """,

            "answer": """
            Oxygen: Z = 8

            Electron configuration:

            1s² 2s² 2p⁴

            Apply Slater's Rules carefully.
            """
        },

        "Problem 3: Chlorine (Cl)": {
            "question": """
            Calculate Zeff experienced by a 3p electron
            in Chlorine.
            """,

            "answer": """
            Chlorine: Z = 17

            Electron configuration:

            1s² 2s² 2p⁶ 3s² 3p⁵

            Use Slater's Rules to calculate S
            and then Zeff.
            """
        }
    }

    selected_problem = st.selectbox(
        "Select a Problem",
        list(problems.keys())
    )

    st.subheader("Question")

    st.write(
        problems[selected_problem]["question"]
    )

    if st.button("💡 Show Solution"):

        st.success(
            problems[selected_problem]["answer"]
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Virtual Chemistry Laboratory | Zeff Calculation Using Slater's Rules"
)