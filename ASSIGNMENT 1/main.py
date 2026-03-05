from fastapi import FastAPI,Query
app = FastAPI()
# ── Temporary data — acting as our database for now ──────────
products = [

    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },

    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },

    {'id': 3, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': False},

    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },

    {'id': 5, 'name': 'Laptop Stand',     'price':  199, 'category': 'Electronics',  'in_stock': True },

    {'id': 6, 'name': 'Mechanical Keyboard','price':  1299, 'category': 'Electronics',  'in_stock': True },

    {'id': 7, 'name': 'Webcam',  'price':  899, 'category': 'Electronics',  'in_stock': True },

]
# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
# ── Endpoint 1 — Return all products ──────────────────────────

@app.get('/products')

def get_all_products():

    return {'products': products, 
            'total': len(products)}

@app.get('/products/filter')
def filter_products(

    category:  str  = Query(None, description='Electronics or Stationery'),

    max_price: int  = Query(None, description='Maximum price'),

    in_stock:  bool = Query(None, description='True = in stock only')

):
    result = products          # start with all products
    if category:

        result = [p for p in result if p['category'] == category]
    if max_price:

        result = [p for p in result if p['price'] <= max_price]
    if in_stock is not None:

        result = [p for p in result if p['in_stock'] == in_stock]
    return {'filtered_products': result, 'count': len(result)}

# ── Endpoint 2 — Return one product by its ID ──────────────────

@app.get('/products/{product_id}')

def get_product(product_id: int):

    for product in products:

        if product['id'] == product_id:

            return {'product': product}

    return {'error': 'Product not found'}

#Q2_products by category

@app.get('/products/category/{category_name}')
def category_products(category_name: str):

    category_name = category_name.capitalize()  # Ensure first letter is uppercase

    filtered_result = [p for p in products if p['category'] == category_name]

    if not filtered_result:

        return {'error': 'No products found in this category'}

    return {"category": category_name,'products': filtered_result, 'count': len(filtered_result)}
#Q3 products which are instock
@app.get('/products/stock/{instock}')

def get_in_stock_products(instock: bool):

    in_stock = [p for p in products if p['in_stock'] == instock]

    return {'in_stock_products': in_stock, 'count': len(in_stock)}

#Q4 store summary

@app.get("/store/summary")
def get_store_summary():
    total_products = len(products)
    in_stock_products = len([p for p in products if p['in_stock'] == True])
    out_of_stock_products = len([p for p in products if p['in_stock'] == False])
    categories = list(set(p['category'] for p in products))
    return {
        "Store_name": "My E-commerce Store",
        "Total_products": total_products,
        "In_stock_products": in_stock_products,
        "Out_of_stock_products": out_of_stock_products,
        "Categories": categories
    }
#Q5 search products by keyword
@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    keyword = keyword.lower()

    matched_products = [p for p in products if keyword in p['name'].lower()]

    if not matched_products:

        return {'message': 'No products found matching your search'}

    return {'matched_products': matched_products, 'count': len(matched_products)}
  #Q6 Bonus question(deals)
@app.get("/products/deals/info")
def get_product_deals():

    best_deal = products[0]
    premium_pick = products[0]

    for product in products:
        if product["price"] < best_deal["price"]:
            best_deal = product

        if product["price"] > premium_pick["price"]:
            premium_pick = product

    return {
        "best_deal": best_deal,
        "premium_pick": premium_pick
    }
    
