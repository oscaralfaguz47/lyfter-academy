from models.category import Category
from data.data_context import get_data_from_csv


def create_category(category_name):
    existing_categories = get_data_from_csv(Category.FILE_NAME, Category)

    for category in existing_categories:
        if category.category_name.strip().lower() == category_name.strip().lower():
            raise ValueError(f"The category '{category_name}' already exists")
        
    new_category = Category(category_name)
    new_category.create_category()

def get_all_categories():
    categories = get_data_from_csv(Category.FILE_NAME, Category)
    rows = [[c.id_category, c.category_name] for c in categories] 
    return rows