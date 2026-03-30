import csv
import json
from pathlib import Path

CSV_PATH = Path('products.csv')
JSON_PATH = Path('products.json')

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
    
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    print(f'✅ Generated {JSON_PATH} with {len(products)} products')

if __name__ == '__main__':
    main()
