import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date",
                 "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("all_data.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

# Sidebar
with st.sidebar:
    # MyName
    st.title("MUHAMMAD RAFI ILHAM")

    # My Photo
    st.image("e-commerce.jpeg")

# Main
main_df = all_df

# Header
st.markdown('<i class="fa fa-shopping-cart"></i> <h1 style="display:inline;">E-Commerce Dashboard Dicoding</h1>', unsafe_allow_html=True)

# Order Produk
st.subheader("Produk Terlaris dan tidak Terlaris")

total_items = main_df.groupby("product_category_name_english")[
    "order_item_id"].count().sum()
st.markdown(f"Total Produk: **{total_items}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 8))

colors = ["#3CB371", "#90EE90", "#90EE90", "#90EE90", "#90EE90"]

sns.barplot(x="order_item_id", y="product_category_name_english", data=main_df.groupby("product_category_name_english")[
            "order_item_id"].count().reset_index().sort_values(by="order_item_id", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Penjualan Paling Banyak", loc="center", fontsize=12)

sns.barplot(x="order_item_id", y="product_category_name_english", data=main_df.groupby("product_category_name_english")[
            "order_item_id"].count().reset_index().sort_values(by="order_item_id").head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Penjualan Paling Sedikit", loc="center", fontsize=12)

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Performa penjualan
st.subheader("Performa Penjualan tahun 2018")

monthly_orders_df = all_df.resample(rule='M', on='order_approved_at').agg({
    "order_id": "nunique",
})
monthly_orders_df.index = monthly_orders_df.index.strftime(
    '%B')  # Mengubah format order_approved_at menjadi Nama Bulan
monthly_orders_df = monthly_orders_df.reset_index()
monthly_orders_df.rename(columns={"order_id": "order_count"}, inplace=True)

monthly_orders_df = monthly_orders_df.sort_values(
    'order_count').drop_duplicates('order_approved_at', keep='last')

# Membuat mapping untuk bulan numerik
month_names = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
month_mapping = {month: i for i, month in enumerate(month_names, start=1)}

# Menambahkan kolom bulan numerik dan mengurutkan DataFrame berdasarkan bulan numerik
monthly_orders_df['month_numeric'] = monthly_orders_df['order_approved_at'].map(
    month_mapping)
monthly_orders_df = monthly_orders_df.sort_values(
    'month_numeric').drop('month_numeric', axis=1)

# Visualisasi
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    monthly_orders_df["order_approved_at"],
    monthly_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#068DA9"
)
ax.set_title("Jumlah pemesanan per bulan (2018)", loc="center", fontsize=20)
ax.set_xticklabels(monthly_orders_df["order_approved_at"], rotation=25)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Rating Customer
st.subheader("Rating Pelayanan E-Commerce oleh Customers")

total_rating = main_df['review_score'].count()
st.markdown(f"Total Rating: **{total_rating}**")

review_scores = all_df['review_score'].value_counts(
).sort_values(ascending=False)
popular_scores = review_scores.idxmax()

colors = ["#068DA9" if score ==
          popular_scores else "#D3D3D3" for score in review_scores.index]

# Visualisasi
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x=review_scores.index,
    y=review_scores.values,
    order=review_scores.index,
    palette=colors
)

plt.title("Rating Customer untuk Pelayanan E-Commerce", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Jumlah Customer")
plt.xticks(fontsize=12)

# Menampilkan plot di Streamlit
st.pyplot(fig)
