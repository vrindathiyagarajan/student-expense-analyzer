import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
student_data = pd.read_csv("student_spending.csv")
st.title("🎓 Student Expense Analyzer")
st.subheader("Track where your money goes!")
name = st.text_input("Enter your name :")
budget = st.number_input("Enter your monthly budget :", min_value = 0.0)
if "expenses" not in st.session_state:
    st.session_state.expenses = []
if name and budget :
    st.write(f"Hi {name} ! Your budget for this month is {budget :.0f} rupees")
st.subheader("Add your expenses ")
categories = ["Food","Transport","College Supplies","Subscriptions","Going out","Shopping","Other"]
category = st.selectbox("Select Category:",categories)
amount = st.number_input("Enter amount :",min_value = 0.0)
description = st.text_input("Description (optional):")
if st.button("Add Expense"):
    st.session_state.expenses.append({"category":category,"amount":amount,"description":description})
    save_df=pd.DataFrame(st.session_state.expenses)
    save_df.to_csv("my_expenses.csv",index=False)
    st.success(f"Added ₹{amount} for {category}!")


if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    
    total_spent = df["amount"].sum()
    remaining = budget - total_spent
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Budget", f"₹{budget :.0f}")
    col2.metric("Total Spent", f"₹{total_spent :.0f}")

    if remaining < 0:
        col3.metric("Status", "Over Budget!", delta=f"-₹{abs(remaining)}")
        st.error(f"⚠️ Warning! You are ₹{abs(remaining)} above your monthly budget!")
    else:
        col3.metric("Remaining", f"₹{remaining}")
        st.subheader("Expense Breakdown")
        st.dataframe(df)
    
    category_totals = df.groupby("category")["amount"].sum()
    st.bar_chart(category_totals)
    st.subheader("💰 Spending Breakdown")
    for cat, amount in category_totals.items():
        percentage = (amount / total_spent) * 100
        st.write(f"{cat}: ₹{amount} — {round(percentage, 1)}% of your total spending")
    top_category = category_totals.idxmax()
    top_amount = category_totals.max()
    st.warning(f"🚨 You're spending the most on {top_category} — ₹{top_amount}")
    avg_food = student_data["food"].mean()
    avg_transport = student_data["transportation"].mean()
    avg_supplies = student_data["books_supplies"].mean()

    user_food = category_totals.get("Food",0)
    user_transport = category_totals.get("Transport",0)
    user_supplies = category_totals.get("College Supplies",0)

    comparison_data = {
    "Category": ["Food", "Transport", "Supplies"],
    "You": [user_food, user_transport, user_supplies],
    "Average Student": [avg_food, avg_transport, avg_supplies]
}

    comparison_df = pd.DataFrame(comparison_data)
    comparison_df = comparison_df.set_index("Category")

    fig, ax = plt.subplots()
    comparison_df.plot(kind="bar", ax=ax)
    ax.set_ylabel("Amount (₹)")
    ax.set_title("You vs Average Student")
    st.pyplot(fig)

    st.subheader("How You Compare To Other Students")

    if user_food > avg_food:
        st.write(f"🍔 Food: You spend ₹{user_food}, average student spends ₹{round(avg_food,2)}")
        st.info("💡 Tip: Try cooking at home, meal prepping on weekends, or limiting eating out to once a week.")
    else:
        st.write(f"🍔 Food: You spend ₹{user_food}, average student spends ₹{round(avg_food,2)}")
        st.success("✅ Great job keeping food costs under control!")

    if user_transport > avg_transport:
        st.write(f"🚌 Transport: You spend ₹{user_transport}, average student spends ₹{round(avg_transport,2)}")
        st.info("💡 Tip: Consider using public transport, carpooling with friends, or a monthly bus/metro pass.")
    else:
        st.write(f"🚌 Transport: You spend ₹{user_transport}, average student spends ₹{round(avg_transport,2)}")
        st.success("✅ Your transport spending is well managed!")

    if user_supplies > avg_supplies:
        st.write(f"📚 Supplies: You spend ₹{user_supplies}, average student spends ₹{round(avg_supplies,2)}")
        st.info("💡 Tip: Look for second-hand textbooks, digital versions, or share resources with classmates.")
    else:
        st.write(f"📚 Supplies: You spend ₹{user_supplies}, average student spends ₹{round(avg_supplies,2)}")
        st.success("✅ Your supplies spending looks reasonable!")