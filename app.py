import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Zeff Virtual Lab",
    page_icon="⚛️",
    layout="wide"
)


# ============================================================
# ELECTRON CONFIGURATION FUNCTION
# ============================================================

def get_electron_configuration(Z):
    """
    Generate electron configuration using the Aufbau principle.
    This version supports elements from Z = 1 to Z = 36.
    """

    orbital_order = [
        ("1s", 2),
        ("2s", 2),
        ("2p", 6),
        ("3s", 2),
        ("3p", 6),
        ("4s", 2),
        ("3d", 10),
        ("4p", 6),
    ]

    configuration = {}
    remaining_electrons = Z

    for orbital, capacity in orbital_order:

        if remaining_electrons <= 0:
            break

        electrons = min(remaining_electrons, capacity)

        configuration[orbital] = electrons

        remaining_electrons -= electrons

    return configuration


# ============================================================
# FORMAT ELECTRON CONFIGURATION
# ============================================================

def format_configuration(configuration):

    superscripts = {
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹"
    }

    formatted = []

    for orbital, electrons in configuration.items():

        exponent = "".join(
            superscripts[digit]
            for digit in str(electrons)
        )

        formatted.append(f"{orbital}{exponent}")

    return " ".join(formatted)


# ============================================================
# CALCULATE ZEFF USING SLATER'S RULES
# ============================================================

def calculate_zeff(Z, configuration, selected_orbital):

    n = int(selected_orbital[0])
    orbital_type = selected_orbital[1]

    # ========================================================
    # CASE 1: ns / np ELECTRON
    # ========================================================

    if orbital_type in ["s", "p"]:

        # ----------------------------------------------------
        # ELECTRONS IN SAME (ns,np) GROUP
        # ----------------------------------------------------

        same_group = 0

        for orbital, electrons in configuration.items():

            orbital_n = int(orbital[0])
            current_type = orbital[1]

            if orbital_n == n and current_type in ["s", "p"]:
                same_group += electrons

        # Remove the electron being calculated
        same_group -= 1

        # ----------------------------------------------------
        # SPECIAL CASE: 1s
        # ----------------------------------------------------

        if n == 1:

            shielding = same_group * 0.30

            details = {
                "type": "1s",
                "same_group": same_group,
                "same_contribution": 0.30
            }

        # ----------------------------------------------------
        # GENERAL ns / np RULE
        # ----------------------------------------------------

        else:

            n_minus_1 = 0
            lower_shell = 0

            for orbital, electrons in configuration.items():

                orbital_n = int(orbital[0])

                # Electrons in (n-1) shell
                if orbital_n == n - 1:
                    n_minus_1 += electrons

                # Electrons in (n-2) or lower shell
                elif orbital_n <= n - 2:
                    lower_shell += electrons

            shielding = (
                same_group * 0.35
                + n_minus_1 * 0.85
                + lower_shell * 1.00
            )

            details = {
                "type": "sp",
                "same_group": same_group,
                "same_contribution": 0.35,
                "n_minus_1": n_minus_1,
                "lower_shell": lower_shell
            }

    # ========================================================
    # CASE 2: nd ELECTRON
    # ========================================================

    elif orbital_type == "d":

        # Other electrons in same d orbital group
        same_group = configuration[selected_orbital] - 1

        # Electrons to the left contribute 1.00
        left_electrons = 0

        # Standard Slater grouping order
        slater_order = [
            "1s",
            "2s",
            "2p",
            "3s",
            "3p",
            "3d",
            "4s",
            "4p",
            "4d",
            "5s",
            "5p"
        ]

        selected_index = slater_order.index(selected_orbital)

        for orbital, electrons in configuration.items():

            if slater_order.index(orbital) < selected_index:
                left_electrons += electrons

        shielding = (
            same_group * 0.35
            + left_electrons * 1.00
        )

        details = {
            "type": "d",
            "same_group": same_group,
            "left_electrons": left_electrons
        }

    zeff = Z - shielding

    return shielding, zeff, details


# ============================================================
# MAIN APPLICATION
# ============================================================

st.title("⚛️ Virtual Chemistry Laboratory")

st.subheader(
    "Calculation of Effective Nuclear Charge (Zeff) Using Slater's Rules"
)

st.divider()


# ============================================================
# INTRODUCTION
# ============================================================

with st.expander("📚 Learning Objective and Formula", expanded=True):

    st.write(
        "This virtual laboratory helps students calculate the "
        "Effective Nuclear Charge (Zeff) experienced by an electron "
        "using Slater's Rules."
    )

    st.latex(r"Z_{eff} = Z - S")

    st.write(
        "**Z** = Atomic Number  \n"
        "**S** = Shielding Constant  \n"
        "**Zeff** = Effective Nuclear Charge"
    )


# ============================================================
# USER INPUT
# ============================================================

st.header("🧪 Interactive Zeff Calculator")

st.write(
    "Step 1: Enter the Atomic Number (Z). "
    "The electron configuration will be generated automatically."
)

Z = st.number_input(
    "Enter Atomic Number (Z)",
    min_value=1,
    max_value=36,
    value=11,
    step=1
)


# ============================================================
# GENERATE ELECTRON CONFIGURATION
# ============================================================

configuration = get_electron_configuration(Z)

formatted_configuration = format_configuration(configuration)

st.subheader("Step 2: Electron Configuration")

st.info(formatted_configuration)


# ============================================================
# SELECT ORBITAL
# ============================================================

st.subheader("Step 3: Select the Orbital")

available_orbitals = list(configuration.keys())

selected_orbital = st.selectbox(
    "Select the electron orbital for Zeff calculation",
    available_orbitals
)


# ============================================================
# CALCULATE BUTTON
# ============================================================

if st.button("⚡ Calculate Zeff", type="primary"):

    shielding, zeff, details = calculate_zeff(
        Z,
        configuration,
        selected_orbital
    )

    st.divider()

    st.header("📊 Results")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Shielding Constant (S)",
            f"{shielding:.2f}"
        )

    with col2:

        st.metric(
            "Effective Nuclear Charge (Zeff)",
            f"{zeff:.2f}"
        )


    # ========================================================
    # STEP-BY-STEP CALCULATION
    # ========================================================

    st.divider()

    st.header("📝 Step-by-Step Solution")

    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    st.subheader("Step 1: Atomic Number")

    st.write(f"Atomic Number, Z = **{Z}**")


    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    st.subheader("Step 2: Electron Configuration")

    st.code(formatted_configuration)


    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    st.subheader("Step 3: Selected Orbital")

    st.write(
        f"The selected orbital is **{selected_orbital}**."
    )


    # --------------------------------------------------------
    # ns / np ELECTRONS
    # --------------------------------------------------------

    if details["type"] == "1s":

        st.subheader("Step 4: Apply Slater's Rule")

        st.write(
            "For a 1s electron, the other electron in the 1s group "
            "contributes 0.30 to the shielding constant."
        )

        st.write(
            f"Other electrons in the same group = "
            f"**{details['same_group']}**"
        )

        st.latex(
            rf"S = {details['same_group']} \times 0.30"
        )

        st.latex(
            rf"S = {shielding:.2f}"
        )


    elif details["type"] == "sp":

        st.subheader(
            "Step 4: Apply Slater's Rules for ns/np Electrons"
        )

        st.write(
            f"Other electrons in the same (ns,np) group = "
            f"**{details['same_group']}**"
        )

        st.write(
            f"Contribution = {details['same_group']} × 0.35"
        )

        st.write(
            f"Electrons in the (n−1) shell = "
            f"**{details['n_minus_1']}**"
        )

        st.write(
            f"Contribution = {details['n_minus_1']} × 0.85"
        )

        st.write(
            f"Electrons in the (n−2) or lower shells = "
            f"**{details['lower_shell']}**"
        )

        st.write(
            f"Contribution = {details['lower_shell']} × 1.00"
        )

        st.subheader("Step 5: Calculate Shielding Constant")

        st.latex(
            rf"""
            S =
            ({details['same_group']} \times 0.35)
            +
            ({details['n_minus_1']} \times 0.85)
            +
            ({details['lower_shell']} \times 1.00)
            """
        )

        st.latex(
            rf"S = {shielding:.2f}"
        )


    # --------------------------------------------------------
    # nd ELECTRONS
    # --------------------------------------------------------

    elif details["type"] == "d":

        st.subheader(
            "Step 4: Apply Slater's Rules for nd Electrons"
        )

        st.write(
            f"Other electrons in the same d group = "
            f"**{details['same_group']}**"
        )

        st.write(
            f"Contribution = {details['same_group']} × 0.35"
        )

        st.write(
            f"Electrons to the left of the nd group = "
            f"**{details['left_electrons']}**"
        )

        st.write(
            f"Contribution = {details['left_electrons']} × 1.00"
        )

        st.subheader("Step 5: Calculate Shielding Constant")

        st.latex(
            rf"""
            S =
            ({details['same_group']} \times 0.35)
            +
            ({details['left_electrons']} \times 1.00)
            """
        )

        st.latex(
            rf"S = {shielding:.2f}"
        )


    # ========================================================
    # FINAL ZEFF CALCULATION
    # ========================================================

    st.subheader("Step 6: Calculate Effective Nuclear Charge")

    st.latex(r"Z_{eff} = Z - S")

    st.latex(
        rf"Z_{{eff}} = {Z} - {shielding:.2f}"
    )

    st.latex(
        rf"Z_{{eff}} = {zeff:.2f}"
    )

    st.success(
        f"🎉 Final Answer: Zeff for the {selected_orbital} electron = {zeff:.2f}"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "⚛️ Virtual Chemistry Laboratory | "
    "Calculation of Effective Nuclear Charge (Zeff) Using Slater's Rules"
)
