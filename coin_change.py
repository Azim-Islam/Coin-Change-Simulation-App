import streamlit as st
import pandas as pd
def _get_change_making_matrix(set_of_coins, r: int):
    m = [[0 for _ in range(r + 1)] for _ in range(len(set_of_coins) + 1)]
    for i in range(1, r + 1):
        m[0][i] = float('inf')  # By default there is no way of making change
    return m

def change_making(coins, n: int):
    """This function assumes that all coins are available infinitely.
    n is the number to obtain with the fewest coins.
    coins is a list or tuple with the available denominations.
    """
    m = _get_change_making_matrix(coins, n)
    for c in range(1, len(coins) + 1):
        for r in range(1, n + 1):
            # Just use the coin coins[c - 1].
            if coins[c - 1] == r:
                m[c][r] = 1
            # coins[c - 1] cannot be included.
            # Use the previous solution for making r,
            # excluding coins[c - 1].
            elif coins[c - 1] > r:
                m[c][r] = m[c - 1][r]
            # coins[c - 1] can be used.
            # Decide which one of the following solutions is the best:
            # 1. Using the previous solution for making r (without using coins[c - 1]).
            # 2. Using the previous solution for making r - coins[c - 1] (without
            #      using coins[c - 1]) plus this 1 extra coin.
            else:
                m[c][r] = min(m[c - 1][r], 1 + m[c][r - coins[c - 1]])
    return m

def print_2d_array(array):
    for i in range(len(array)):
        for j in range(len(array[0])):
            print(array[i][j], end="   ")
        print("\n")

st.set_page_config(
     page_title="Coin Change Solver",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
)

with st.form("coin_change_table"):
    coins = st.text_input("Enter The Coins Available (Space Seperated eg, '1 2 4 6 10')")
    amount = st.text_input("Enter The Amount To Create")
    submit = st.form_submit_button("Submit")   
    if submit:
        coins = list(map(int, coins.split()))
        amount = int(amount)
        array = change_making(coins, amount)
        
        df = pd.DataFrame(
            array,
            columns=(f"Amount = {i}" for i in range(0, amount+1)),
            index=(["Coins = 0"] + [f"Coins = {c}" for c in coins])
        )
        st.success("Table Successfully Generated")
        
with st.expander("Generated Table"):
    if submit:
        st.table(df.style.format('{:7,.1f}'))