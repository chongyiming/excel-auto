import streamlit as st
import pandas as pd
from io import StringIO

rt_pasted_text = st.text_area("Request Timeout (Get all accounts)")
con_strings = []
if rt_pasted_text:
    try:
        rt_df = pd.read_csv(StringIO(rt_pasted_text), sep="\t", header=None)

        for line in rt_df[3].astype(str):  # Ensure it's string
            prefix = line.split(':')[0]
            con_strings.append(prefix)

        if con_strings:
            final_string = "|".join(con_strings) + "|"
            st.write(final_string[0:-1])
    except:
        pass

# import streamlit as st
# import pandas as pd
# from io import StringIO
# from collections import defaultdict

# rt_pasted_text = st.text_area("Request Timeout (Get all accounts)")

# result_dict = defaultdict(list)
# if rt_pasted_text:
#     try:
#         rt_df = pd.read_csv(StringIO(rt_pasted_text), sep="\t", header=None)

#         # Loop through each row
#         for i in range(len(rt_df)):
#             key = str(rt_df.iloc[i, 0])
#             full_string = str(rt_df.iloc[i, 3])
#             value = full_string.split(':')[0]  # Get part before the colon
#             result_dict[key].append(value[1:-1])

#         # Display result
#         print(result_dict)  # Optional: convert back to regular dict
#     except:
#         pass