import streamlit as st

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Zeff Virtual Lab",
    page_icon="⚛️",
    layout="wide"
)

# ==================================================
# ELECTRON CONFIGURATION FUNCTION
# ==================================================

def get_electron_configuration(Z):
    """
    Generate electron configuration using Aufbau principle.
    Supports atomic numbers 1–36.
    """

    orbitals = [
        ("1s", 2),
        ("2s", 2),
        ("2p", 6),
        ("3s", 2),
        ("3p", 6),
        ("4s", 2),
        ("3d", 10),
        ("4p", 6),
        ("5s", 2),
        ("4d", 10),
        ("5p", 6),
    ]

    remaining = Z
    configuration = {}

    for orbital, capacity in orbitals:

        electrons = min(remaining, capacity)

        if electrons > 0:
            configuration[orbital] = electrons

        remaining -= electrons

        if remaining <= 0:
            break

    return configuration


# ==================================================
# FORMAT ELECTRON CONFIGURATION
# ==================================================

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

    text = ""

    for orbital, electrons in configuration.items():

        superscript = "".join(
            superscripts[digit]
            for digit in str(electrons)
        )

        text += f"{orbital}{superscript} "

    return text


# ==================================================
# SLATER'S RULE CALCULATION
# ==================================================

def calculate_zeff(Z, configuration, selected_orbital):

    # Get principal quantum number
    n = int(selected_orbital[0])

    # Get orbital type (s, p, d, f)
    orbital_type = selected_orbital[1]

    # Number of electrons in selected orbital
    selected_electrons = configuration[selected_orbital]

    # ------------------------------------------------
    # ns / np ELECTRONS
    # ------------------------------------------------

    if orbital_type in ["s", "p"]:

        same_group = 0

        # Electrons in ns and np group
        for orbital, electrons in configuration.items():

            orbital_n = int(orbital[0])
            orbital_type_current = orbital[1]

            if (
                orbital_n == n
                and orbital_type_current in ["s", "p"]
            ):
                same_group += electrons

        # Exclude electron being calculated
        same_group -= 1

        # Special case for 1s
        if n == 1:

            shielding = same_group * 0.30

            details = {
                "same_group": same_group,
                "same_contribution": 0.30,
                "n_minus_1": 0,
                "lower": 0
            }

        else:

            n_minus_1 = 0
            lower_shell = 0

            for orbital, electrons in configuration.items():

                orbital_n = int(orbital[0])

                # (n-1) shell
                if orbital_n == n - 1:
                    n_minus_1 += electrons

                # (n-2) or lower
                elif orbital_n <= n - 2:
                    lower_shell += electrons

            shielding = (
                same_group * 0.35
                + n_minus_1 * 0.85
                + lower_shell * 1.00
            )

            details = {
                "same_group": same_group,
                "same_contribution": 0.35,
                "n_minus_1": n_minus_1,
                "lower": lower_shell
            }

    # ------------------------------------------------
    # nd / nf ELECTRONS
    # ------------------------------------------------

    else:

        same_group = selected_electrons - 1

        left_electrons = 0

        # Aufbau order
        orbital_order = list(configuration.keys())

        selected_index = orbital_order.index(selected_orbital)

        for orbital in orbital_order[:selected_index]:
            left_electrons += configuration[orbital]

        shielding = (
            same_group * 0.35
            + left_electrons * 1.00
        )

        details = {
            "same_group": same_group,
            "same_contribution": 0.35,
            "left": left_electrons
        }

    zeff = Z - shielding

    return shielding, zeff, details


# ==================================================
# TITLE
# ==================================================

st.title("⚛️ Virtual Chemistry Laboratory")

st.subheader(
    "Calculation of Effective Nuclear Charge (Zeff) "
    "Using Slater's Rules"
)

st.divider()


# ==================================================
# USER INPUT
# ==================================================

st.header("🧪 Zeff Interactive Calculator")

st.write(
    "Enter the Atomic Number and select the orbital "
    "for which you want to calculate Zeff."
)

Z = st.number_input(
    "Enter Atomic Number (Z)",
    min_value=1,
    max_value=36,
    value=11,
    step=1
)

# Generate electron configuration

configuration = get_electron_configuration(Z)

formatted_config = format_configuration(configuration)

st.subheader("Step 1: Electron Configuration")

st.info(formatted_config)


# ==================================================
# ORBITAL SELECTION
# ==================================================

available_orbitals = list(configuration.keys())

selected_orbital = st.selectbox(
    "Step 2: Select the Electron Orbital",
    available_orbitals
)


# ==================================================
# CALCULATE BUTTON
# ==================================================

if st.button("⚡ Calculate Zeff"):

    shielding, zeff, details = calculate_zeff(
        Z,
        configuration,
        selected_orbital
    )

    st.divider()

    st.header("📊 Calculation Results")

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


    # ==================================================
    # STEP-BY-STEP SOLUTION
    # ==================================================

    st.divider()

    st.header("📝 Step-by-Step Calculation")

    st.write("### Step 1: Atomic Number")

    st.write(f"**Z = {Z}**")


    st.write("### Step 2: Electron Configuration")

    st.code(formatted_config)


    st.write("### Step 3: Selected Orbital")

    st.write(
        f"You selected the **{selected_orbital}** orbital."
    )


    orbital_type = selected_orbital[1]

    # --------------------------------------------------
    # ns / np
    # --------------------------------------------------

    if orbital_type in ["s", "p"]:

        st.write(
            "### Step 4: Apply Slater's Rules for ns/np Electrons"
        )

        if selected_orbital == "1s":

            st.write(
                f"Other electrons in the same group = "
                f"**{details['same_group']}**"
            )

            st.write(
                f"Contribution = "
                f"{details['same_group']} × 0.30"
            )

            st.write(
                f"Shielding Constant, S = **{shielding:.2f}**"
            )

        else:

            st.write(
                f"Other electrons in the same (ns,np) group = "
                f"**{details['same_group']}**"
            )

            st.write(
                f"Contribution = "
                f"{details['same_group']} × 0.35"
            )

            st.write(
                f"Electrons in (n−1) shell = "
                f"**{details['n_minus_1']}**"
            )

            st.write(
                f"Contribution = "
                f"{details['n_minus_1']} × 0.85"
            )

            st.write(
                f"Electrons in (n−2) or lower shells = "
                f"**{details['lower']}**"
            )

            st.write(
                f"Contribution = "
                f"{details['lower']} × 1.00"
            )

            st.write("### Step 5: Calculate Shielding Constant")

            st.latex(
                rf"""
                S =
                ({details['same_group']} \times 0.35)
                +
                ({details['n_minus_1']} \times 0.85)
                +
                ({details['lower']} \times 1.00)
                """
            )

            st.latex(
                rf"S = {shielding:.2f}"
            )


    # --------------------------------------------------
    # nd / nf
    # --------------------------------------------------

    else:

        st.write(
            "### Step 4: Apply Slater's Rules for nd/nf Electrons"
        )

        st.write(
            f"Other electrons in the same group = "
            f"**{details['same_group']}**"
        )

        st.write(
            f"Contribution = "
            f"{details['same_group']} × 0.35"
        )

        st.write(
            f"Electrons to the left = "
            f"**{details['left']}**"
        )

        st.write(
            f"Contribution = "
            f"{details['left']} × 1.00"
        )

        st.write("### Step 5: Calculate Shielding Constant")

        st.latex(
            rf"""
            S =
            ({details['same_group']} \times 0.35)
            +
            ({details['left']} \times 1.00)
            """
        )

        st.latex(
            rf"S = {shielding:.2f}"
        )


    # ==================================================
    # FINAL ZEFF
    # ==================================================

    st.write(
        "### Step 6: Calculate Effective Nuclear Charge"
    )

    st.latex(
        rf"Z_{{eff}} = Z - S"
    )

    st.latex(
        rf"Z_{{eff}} = {Z} - {shielding:.2f}"
    )

    st.latex(
        rf"\boxed{{Z_{{eff}} = {zeff:.2f}}}"
    )

    st.success(
        f"Final Answer: Zeff for {selected_orbital} = {zeff:.2f}"
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "⚛️ Virtual Chemistry Laboratory | "
    "Effective Nuclear Charge Calculation Using Slater's Rules"
)
```
