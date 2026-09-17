SET search_path TO transactions_exercises;

DO $$
DECLARE
	v_user_email TEXT:= 'oscar@mail.com';
	v_user_id INTEGER;
	v_list_of_products RECORD;
	v_bill_number INTEGER;
	v_bill_id INTEGER;
BEGIN
	-- Validate if the user exists
	SELECT id INTO v_user_id 
	FROM users 
	WHERE email = v_user_email AND is_active;

	IF NOT FOUND THEN
		RAISE EXCEPTION 'There is not an active user with email: %.', v_user_email;
	END IF;

	-- Generate the new bill_number and initialize v_bill_number
	SELECT COALESCE(MAX(bill_number), 0) + 1 INTO v_bill_number FROM bills;

	-- Create the bill
	INSERT INTO bills (bill_number, user_id) VALUES
	(v_bill_number, v_user_id)
	RETURNING id INTO v_bill_id;
	
	-- Build the list of products to purchase
	FOR v_list_of_products IN
		SELECT p.id AS product_id, lp.product_name, lp.quantity, p.price 
		FROM (VALUES
		('Rice 1kg', 20),
		('Whole Milk 1L', 2),
		('Chicken Breast kg', 12),
		('Coffee 500g', 5),
		('Black Beans 1kg', 15),
		('Brown Sugar 2kg', 8)
		) AS lp(product_name, quantity)
		LEFT JOIN products p ON LOWER(p.name) = LOWER(lp.product_name)
	LOOP
		-- Validate if the product exist
		IF v_list_of_products.product_id IS NULL THEN
			RAISE EXCEPTION 'The product "%" does not exist.', v_list_of_products.product_name;
		END IF;

		-- Reduce the product stock only if there is enough 
		UPDATE products SET stock_available = stock_available - v_list_of_products.quantity
		WHERE id = v_list_of_products.product_id AND stock_available >= v_list_of_products.quantity;

		IF NOT FOUND THEN
			RAISE EXCEPTION 'There is not enough stock for product "%" review the line first', v_list_of_products.product_name;
		END IF;

		-- Create the bill line
		INSERT INTO bill_lines (bill_id, product_id, quantity, unit_price) VALUES
		(v_bill_id, v_list_of_products.product_id, v_list_of_products.quantity, v_list_of_products.price);
	
	END LOOP;
	RAISE NOTICE 'The purchase was created successfully with the invoice number: %', v_bill_number;

EXCEPTION 
	WHEN OTHERS THEN
		RAISE EXCEPTION 'Purchase failed: %', SQLERRM
		USING ERRCODE = SQLSTATE;
END $$;

-- The "ROLLBACK;" is not necessary here because any unhandled error inside the DO block rolls back all automatically.

