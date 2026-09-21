SET search_path TO transactions_exercises;

DO $$
DECLARE
	v_bill_id	  INTEGER;
	v_bill_number INTEGER;
	v_user_email  TEXT := 'oscar@mail.com';
	v_user_id 	  INTEGER;
	v_bill_line RECORD;
BEGIN
	-- Search for the user
	SELECT id INTO v_user_id FROM users WHERE email = v_user_email AND is_active;
	
	-- Validate if the user exists
	IF NOT FOUND THEN
		RAISE EXCEPTION 'There is not an active user with the email: %', v_user_email;
	END IF;

	-- Search for the next bill_number
	SELECT COALESCE(MAX(bill_number), 0) + 1 INTO v_bill_number FROM bills;
	
	-- Create the bill
	INSERT INTO bills(bill_number, user_id, status) VALUES(v_bill_number, v_user_id, 'Sent')
	RETURNING id INTO v_bill_id;

	-- Loop for bill lines
	FOR v_bill_line IN
		-- Generate the results for the lines
		SELECT
		ld.product_name,
		ld.quantity,
		p.id AS product_id,
		p.price AS unit_price,
		p.stock_available
		FROM (VALUES
		('Coffee 500g', 1.00),
		('Chicken Breast kg', 0.50),
		('Apples per kg', 4.00)
		) AS ld(product_name, quantity)
		LEFT JOIN products p ON p.name = ld.product_name
	LOOP
		IF v_bill_line.product_id IS NULL THEN
			RAISE EXCEPTION 'An entered product does not exist in the database.';
		END IF;
		
		-- Validate if there's available stock for every product
		IF v_bill_line.stock_available < v_bill_line.quantity THEN
			RAISE EXCEPTION 'The product: "%" does not have sufficient stock, it is currently: "%", and you entered: "%"', 
			v_bill_line.product_name , v_bill_line.stock_available, v_bill_line.quantity;
		END IF;	

		-- Create every line in bill_lines table
		INSERT INTO bill_lines (bill_id, product_id, quantity, unit_price) 
		VALUES(v_bill_id, v_bill_line.product_id, v_bill_line.quantity, v_bill_line.unit_price);

		-- Update the stock of the product
		UPDATE products SET stock_available = stock_available - v_bill_line.quantity
		WHERE id = v_bill_line.product_id;
		
	END LOOP;
	RAISE NOTICE 'Bill number: % created successfully.', v_bill_number;
EXCEPTION
	WHEN OTHERS THEN
		RAISE EXCEPTION 'Bill creation failed: %', SQLERRM;
END $$;



