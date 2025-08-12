import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="📊 FCST Replacer (Multi-Filter)", layout="centered")
st.title("🔁 Replace FCST Based on LOC + ITEM + CHANNEL + FDATE (with Multi-Filter)")

st.markdown("""
This tool replaces only the `FCST` in the **first file**, based on exact match of:

**`LOC + ITEM + CHANNEL + FDATE`** from the **second file**  

You can **multi-select** LOC(s) and FDATE(s) to control exactly which rows get updated.
""")

# File uploaders
file1 = st.file_uploader("📂 Upload File 1 (Base)", type=["csv", "txt"])
file2 = st.file_uploader("📂 Upload File 2 (Source)", type=["csv", "txt"])

if file1 and file2:
    try:
        # Read File 1 (pipe-delimited single column)
        file1_lines = file1.read().decode("utf-8").splitlines()
        header = file1_lines[0].strip()
        col_names = header.split("|")

        data1 = [line.split("|") for line in file1_lines[1:]]
        df1 = pd.DataFrame(data1, columns=col_names)

        # Read File 2 normally
        df2 = pd.read_csv(file2, delimiter='|', dtype=str, keep_default_na=False)

        # Ensure both have necessary columns
        required_cols = ['LOC', 'ITEM', 'CHANNEL', 'FDATE', 'FCST']
        for col in required_cols:
            if col not in df1.columns or col not in df2.columns:
                st.error(f"❌ Missing column: {col}")
                st.stop()

        # Multi-select filters
        available_fdates = sorted(df2['FDATE'].unique())
        available_locs = sorted(df2['LOC'].unique())

        selected_fdates = st.multiselect("📅 Select FDATE(s) to update", available_fdates, default=available_fdates)
        selected_locs = st.multiselect("🏢 Select LOC(s) to update", available_locs, default=available_locs)

        # Create match key
        df1['KEY'] = df1['LOC'].str.strip() + df1['ITEM'].str.strip() + df1['CHANNEL'].str.strip() + df1['FDATE'].str.strip()
        df2['KEY'] = df2['LOC'].str.strip() + df2['ITEM'].str.strip() + df2['CHANNEL'].str.strip() + df2['FDATE'].str.strip()

        # Apply multi-select filters to df2
        df2_filtered = df2[df2['FDATE'].isin(selected_fdates) & df2['LOC'].isin(selected_locs)]

        # Map for FCST updates
        fcst_map = df2_filtered.set_index('KEY')['FCST'].to_dict()

        # Replace FCST only for filtered matches
        df1['FCST'] = df1.apply(lambda row: fcst_map.get(row['KEY'], row['FCST']), axis=1)

        # Drop helper column
        df1.drop(columns=['KEY'], inplace=True)

        # Rebuild output file
        output_lines = ['|'.join(col_names)]
        for _, row in df1.iterrows():
            output_lines.append('|'.join(row.astype(str)))

        result_data = '\n'.join(output_lines)

        # Download + Preview
        st.success("✅ FCST values updated based on selected LOC(s) & FDATE(s).")
        st.download_button("📥 Download Updated CSV", result_data, file_name="fcst_updated.csv", mime="text/csv")

        st.text("🔍 Preview:")
        st.code('\n'.join(output_lines[:5]), language='text')

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("⬆️ Upload both files to proceed.")
