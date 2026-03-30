import streamlit as st

# Function to reduce number to single digit
def digit_root(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

st.title("🔢 Digit Root Calculator")

start = st.number_input("Enter Start Number", value=1)
end = st.number_input("Enter End Number", value=100)

filter_value = st.selectbox("Filter by Digit Root", ["All"] + list(range(1,10)))

if st.button("Calculate"):
    results = []
    
    for num in range(int(start), int(end) + 1):
        dr = digit_root(num)
        
        if filter_value == "All" or dr == filter_value:
            results.append((num, dr))
    
    st.write("### Results")
    
    for r in results:
        st.write(f"{r[0]} → {r[1]}")
    
    st.success(f"Total Results: {len(results)}")