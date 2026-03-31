import csv
import json
from pathlib import Path

CSV_PATH = Path('products.csv')
JSON_PATH = Path('products.json')
OUTPUT_DIR = Path('.')

def slugify(name):
    return name.lower().replace(' ', '-').replace('.', '').replace('(', '').replace(')', '')

def generate_product_page(product, all_products, is_thai=False):
    """Generate a single product page with anti-flicker and correct script order"""
    
    lang_prefix = '/th' if is_thai else ''
    name = product.get('name_th', product['name']) if is_thai else product['name']
    description = product.get('description_th', product['description']) if is_thai else product['description']
    
    # Get 4 random recommended products
    import random
    others = [p for p in all_products if p['id'] != product['id']]
    random.shuffle(others)
    recommendations = others[:4]
    
    html = f'''<!DOCTYPE html>
<html lang="{ 'th' if is_thai else 'en' }">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | Daje Games</title>
    <meta name="description" content="{description[:150]}">
    
    <!-- Anti-flicker: hides page until injector builds correct navbar -->
    <style id="jh-anti-flicker">body {{ opacity: 0; }}</style>
    
    <!-- INJECTORS (config must load before core) -->
    <script src="https://assets.janishammer.com/js/injector-config.js"></script>
    <script src="https://assets.janishammer.com/js/injector-core.js"></script>
    
    <style>
        /* your existing product page styles here */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Quicksand', sans-serif; background: #fafafa; }}
        .product-container {{ max-width: 1200px; margin: 2rem auto; padding: 1rem; }}
        .product-detail {{ display: flex; flex-wrap: wrap; gap: 2rem; background: white; border-radius: 24px; padding: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }}
        .product-image {{ flex: 1; min-width: 280px; }}
        .product-image img {{ width: 100%; border-radius: 16px; }}
        .product-info {{ flex: 1; }}
        .product-name {{ font-size: 2rem; color: #FFB6C1; margin-bottom: 1rem; }}
        .product-price {{ font-size: 2rem; color: #D4AF37; font-weight: bold; margin: 1rem 0; }}
        .product-description {{ color: #666; line-height: 1.6; margin: 1rem 0; }}
        .add-to-cart {{ background: linear-gradient(135deg, #FFB6C1, #FF99AA); color: #333; border: none; padding: 1rem 2rem; border-radius: 40px; font-weight: bold; cursor: pointer; margin-top: 1rem; }}
        .back-link {{ display: inline-block; margin-top: 1rem; color: #FFB6C1; text-decoration: none; }}
        .recommendations {{ margin-top: 3rem; }}
        .rec-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem; }}
        .rec-card {{ background: white; border-radius: 16px; padding: 1rem; text-align: center; cursor: pointer; transition: transform 0.2s; }}
        .rec-card:hover {{ transform: translateY(-4px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .rec-card img {{ width: 100%; height: 120px; object-fit: contain; }}
        .rec-name {{ font-weight: 600; margin-top: 0.5rem; }}
        .rec-price {{ color: #D4AF37; }}
        @media (max-width: 768px) {{ .product-detail {{ flex-direction: column; }} }}
    </style>
</head>
<body>
    <div class="product-container">
        <div class="product-detail">
            <div class="product-image">
                <img src="{product['main_image']}" alt="{name}">
            </div>
            <div class="product-info">
                <h1 class="product-name">{name}</h1>
                <div class="product-price">฿{product['price']:,}</div>
                <div class="product-description">{description}</div>
                <button class="add-to-cart" onclick="addToCart({{ id: '{product['id']}', name: '{name}', price: {product['price']}, image: '{product['main_image']}' }})">
                    <i class="fas fa-shopping-cart"></i> Add to Cart
                </button>
                <a href="{lang_prefix}/" class="back-link">← Back to Shop</a>
            </div>
        </div>
        
        <div class="recommendations">
            <h3>You May Also Like</h3>
            <div class="rec-grid">
                {''.join([f'''
                <div class="rec-card" onclick="location.href='{lang_prefix}/{slugify(r['name'])}.html'">
                    <img src="{r['main_image']}" alt="{r['name']}">
                    <div class="rec-name">{r['name']}</div>
                    <div class="rec-price">฿{r['price']:,}</div>
                </div>
                ''' for r in recommendations])}
            </div>
        </div>
    </div>
    
    <div class="cart-floating" id="cartFloating">
        <i class="fas fa-shopping-bag"></i>
        <span class="cart-count" id="cartCount">0</span>
    </div>
    
    <div id="cartModal" class="cart-modal">
        <div class="cart-content">
            <div class="cart-header">
                <h2><i class="fas fa-shopping-bag"></i> Your Cart</h2>
                <span class="cart-close" onclick="closeCart()">&times;</span>
            </div>
            <div class="cart-items" id="cartItems">
                <div style="text-align: center; padding: 2rem;">Your cart is empty</div>
            </div>
            <div class="cart-summary">
                <div class="cart-total">
                    <span>Total</span>
                    <span id="cartTotal">฿0</span>
                </div>
                <button class="btn-quotation" onclick="requestQuotation()">
                    <i class="fas fa-file-invoice"></i> Get Quotation
                </button>
            </div>
        </div>
    </div>
    
    <div id="toast" class="toast"></div>
    
    <script>
        // Cart functions (same as your main index)
        let cart = JSON.parse(localStorage.getItem('dajeCart')) || [];
        
        function updateCartUI() {{
            const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);
            document.getElementById('cartCount').innerText = cartCount;
            localStorage.setItem('dajeCart', JSON.stringify(cart));
            renderCartItems();
        }}
        
        function renderCartItems() {{
            const container = document.getElementById('cartItems');
            const totalSpan = document.getElementById('cartTotal');
            if (!container) return;
            
            if (cart.length === 0) {{
                container.innerHTML = '<div style="text-align: center; padding: 2rem;">Your cart is empty</div>';
                if (totalSpan) totalSpan.innerText = '0';
                return;
            }}
            
            let total = 0;
            container.innerHTML = cart.map((item, idx) => {{
                total += item.price * item.quantity;
                return `
                    <div class="cart-item">
                        <img src="${{item.image}}" class="cart-item-image">
                        <div class="cart-item-details">
                            <div class="cart-item-name">${{item.name}}</div>
                            <div class="cart-item-price">฿${{item.price.toLocaleString()}}</div>
                        </div>
                        <div class="cart-item-actions">
                            <button class="cart-qty-btn" onclick="updateCartItem(${{idx}}, -1)">-</button>
                            <span>${{item.quantity}}</span>
                            <button class="cart-qty-btn" onclick="updateCartItem(${{idx}}, 1)">+</button>
                            <i class="fas fa-trash-alt" onclick="removeCartItem(${{idx}})" style="color: #F44336; cursor: pointer;"></i>
                        </div>
                    </div>
                `;
            }}).join('');
            if (totalSpan) totalSpan.innerText = `฿${{total.toLocaleString()}}`;
        }}
        
        function updateCartItem(index, change) {{
            const newQty = cart[index].quantity + change;
            if (newQty <= 0) cart.splice(index, 1);
            else cart[index].quantity = newQty;
            updateCartUI();
        }}
        
        function removeCartItem(index) {{
            cart.splice(index, 1);
            updateCartUI();
        }}
        
        function addToCart(product) {{
            const existing = cart.find(i => i.id === product.id);
            if (existing) existing.quantity++;
            else cart.push({{...product, quantity: 1}});
            updateCartUI();
            showToast(`Added ${{product.name}} to cart`);
        }}
        
        function showToast(msg) {{
            const toast = document.getElementById('toast');
            if (toast) {{
                toast.textContent = msg;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2000);
            }}
        }}
        
        function openCart() {{
            document.getElementById('cartModal').classList.add('active');
            renderCartItems();
        }}
        
        function closeCart() {{
            document.getElementById('cartModal').classList.remove('active');
        }}
        
        function requestQuotation() {{
            if (cart.length === 0) {{
                showToast('Please add items to your cart first');
                return;
            }}
            let items = cart.map(i => `${{i.name}} x ${{i.quantity}} = ฿${{(i.price * i.quantity).toLocaleString()}}`).join('\\n');
            let total = cart.reduce((s, i) => s + i.price * i.quantity, 0);
            let subject = encodeURIComponent('Quotation Request - Daje Games');
            let body = encodeURIComponent(`Hello Daje Games Team,\\n\\nI would like a quotation for:\\n\\n${{items}}\\n\\nTotal: ฿${{total.toLocaleString()}}\\n\\nPlease contact me.\\n\\nBest regards`);
            window.location.href = `mailto:info@daje.janishammer.com?subject=${{subject}}&body=${{body}}`;
            showToast('Opening email client...');
        }}
        
        document.getElementById('cartFloating').addEventListener('click', openCart);
        updateCartUI();
    </script>
</body>
</html>'''
    
    return html

def main():
    products = []
    
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append({
                'id': row['id'],
                'name': row['name'],
                'name_th': row.get('name_th', row['name']),
                'price': int(row['price']),
                'main_image': row['main_image'],
                'description': row['description'],
                'description_th': row.get('description_th', row['description']),
                'stock_status': row['stock_status'],
                'collection': row.get('collection', '')
            })
    
    # Save JSON
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f'✅ Generated {JSON_PATH} with {len(products)} products')
    
    # Generate product pages
    for product in products:
        # English version
        slug = slugify(product['name'])
        en_path = OUTPUT_DIR / f'{slug}.html'
        with open(en_path, 'w', encoding='utf-8') as f:
            f.write(generate_product_page(product, products, is_thai=False))
        print(f'  ✅ Generated {en_path}')
        
        # Thai version
        th_slug = slugify(product.get('name_th', product['name']))
        th_dir = OUTPUT_DIR / 'th'
        th_dir.mkdir(exist_ok=True)
        th_path = th_dir / f'{th_slug}.html'
        with open(th_path, 'w', encoding='utf-8') as f:
            f.write(generate_product_page(product, products, is_thai=True))
        print(f'  ✅ Generated {th_path}')
    
    print(f'🎉 Done! Generated {len(products) * 2} product pages')

if __name__ == '__main__':
    main()
