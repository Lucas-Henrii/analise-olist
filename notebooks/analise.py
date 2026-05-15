import pandas as pd

# Carregar
orders    = pd.read_csv('../dados/olist_orders_dataset.csv')
items     = pd.read_csv('../dados/olist_order_items_dataset.csv')
products  = pd.read_csv('../dados/olist_products_dataset.csv')
customers = pd.read_csv('../dados/olist_customers_dataset.csv')

# Limpeza
orders_clean = orders.dropna(subset=['order_delivered_customer_date']).copy()
orders_clean['order_purchase_timestamp'] = pd.to_datetime(orders_clean['order_purchase_timestamp'])
orders_clean['mes_ano'] = orders_clean['order_purchase_timestamp'].dt.to_period('M')

# Juntar tabelas
df = orders_clean.merge(items, on='order_id')
df = df.merge(customers, on='customer_id')
df = df.merge(products, on='product_id')

print(f"Dataset final: {df.shape[0]} linhas e {df.shape[1]} colunas")

# PERGUNTA 1 — Quais estados vendem mais?
print("\n=== TOP 10 ESTADOS POR VENDAS ===")
estados = df.groupby('customer_state')['price'].sum().sort_values(ascending=False).head(10)
print(estados)

# PERGUNTA 2 — Quais categorias têm maior ticket médio?
print("\n=== TOP 10 CATEGORIAS POR TICKET MÉDIO ===")
categorias = df.groupby('product_category_name')['price'].mean().sort_values(ascending=False).head(10)
print(categorias)

# PERGUNTA 3 — Evolução de vendas mês a mês
print("\n=== VENDAS POR MÊS ===")
mensal = df.groupby('mes_ano')['price'].sum()
print(mensal)

# Exportar para Excel
with pd.ExcelWriter('../relatorios/analise_olist.xlsx', engine='openpyxl') as writer:
    estados.to_frame().to_excel(writer, sheet_name='Vendas por Estado')
    categorias.to_frame().to_excel(writer, sheet_name='Ticket por Categoria')
    mensal.to_frame().to_excel(writer, sheet_name='Vendas Mensais')

print("\n✅ Relatório salvo em relatorios/analise_olist.xlsx")