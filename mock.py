import streamlit as st
import pandas as pd
import re

st.title("SSI Data Lookup")

ssi_file = st.file_uploader("Upload SSI Data File (Excel)", type=["xlsx"])

if ssi_file is not None:
    st.write("Data File uploaded")

    ssi_df = pd.read_excel(ssi_file)

    currency = st.text_input("Enter Currency (e.g., USD):")
    client_id = st.text_input("Enter Client ID (e.g., Client_1):")
    party_name = st.text_input("Enter Party Name (e.g., PTYA):")

    if st.button("Find SSI Ref IDs"):

        def generate_account_number(entity, currency):
            return f'{entity}-{currency}-001'

        client_account_number = generate_account_number(client_id, currency)
        party_account_number = generate_account_number(party_name, currency)

        def find_ssi_ref_id(entity, currency):
            pattern = re.compile(f'{entity}[-_ ]{currency}[-_]001', re.IGNORECASE)
            for account_no in ssi_df['account_no']:
                if pattern.search(account_no):
                    return ssi_df.loc[ssi_df['account_no'] == account_no, 'ssi_ref_id'].values[0]
            return None

        client_ssi_ref_id = find_ssi_ref_id(client_id, currency)

        party_ssi_ref_id = find_ssi_ref_id(party_name, currency)

        if client_ssi_ref_id is not None:
            st.write(f"SSI Ref ID for {client_id}, {currency}: {client_ssi_ref_id}")
        else:
            st.write(f"No SSI Ref ID found for {client_id}, {currency}")

        if party_ssi_ref_id is not None:
            st.write(f"SSI Ref ID for {party_name}, {currency}: {party_ssi_ref_id}")
        else:
            st.write(f"No SSI Ref ID found for {party_name}, {currency}")
