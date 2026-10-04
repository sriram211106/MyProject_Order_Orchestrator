def split_order_by_supplier(order_items):
    """Group order items by supplier_id.

    Args:
        order_items: A list of dictionaries containing ``sku``, ``quantity``,
            and ``supplier_id``.

    Returns:
        A dictionary mapping each supplier_id to the list of items for that
        supplier.

    Example:
        >>> items = [
        ...     {"sku": "A1", "quantity": 2, "supplier_id": "supplier-1"},
        ...     {"sku": "B2", "quantity": 1, "supplier_id": "supplier-2"},
        ...     {"sku": "C3", "quantity": 4, "supplier_id": "supplier-1"},
        ... ]
        >>> split_order_by_supplier(items)
        {'supplier-1': [{'sku': 'A1', 'quantity': 2, 'supplier_id': 'supplier-1'}, {'sku': 'C3', 'quantity': 4, 'supplier_id': 'supplier-1'}], 'supplier-2': [{'sku': 'B2', 'quantity': 1, 'supplier_id': 'supplier-2'}]}
    """
    grouped = {}
    for item in order_items:
        supplier_id = item["supplier_id"]
        grouped.setdefault(supplier_id, []).append(item)
    return grouped


# Example usage
items = [
    {"sku": "A1", "quantity": 2, "supplier_id": "supplier-1"},
    {"sku": "B2", "quantity": 1, "supplier_id": "supplier-2"},
    {"sku": "C3", "quantity": 4, "supplier_id": "supplier-1"},
]

items_by_supplier = split_order_by_supplier(items)
print(items_by_supplier)