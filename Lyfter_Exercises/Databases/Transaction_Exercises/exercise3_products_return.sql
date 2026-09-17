SET search_path TO transactions_exercises;

DO $$
DECLARE
	v_bill_number INTEGER:= 1011;
	v_bill_id INTEGER;
	v_bill_status VARCHAR(10);
	v_bill_lines RECORD;
BEGIN
	SELECT id, status INTO v_bill_id, v_bill_status FROM bills WHERE bill_number = v_bill_number;
	
	-- Validate if the bill exists
	IF NOT FOUND THEN
		RAISE EXCEPTION 'The bill % does not exist in the database.', v_bill_number;
	END IF;

	-- Validate if the bill is already Returned
	IF v_bill_status = 'Returned' THEN
		RAISE EXCEPTION 'The bill % has already been returned.', v_bill_number;
	END IF;
		
	-- Set status invoices as Returned
	UPDATE billS SET status = 'Returned' 
	WHERE id = v_bill_id;

	-- Gel the bill lines
	FOR v_bill_lines IN
		SELECT product_id, quantity FROM bill_lines WHERE bill_id = v_bill_id
	LOOP
		-- Update the stock of every product
		UPDATE products SET stock_available = stock_available + v_bill_lines.quantity
		WHERE id = v_bill_lines.product_id;
	END LOOP;
	
	RAISE NOTICE 'Bill % returned successfully.', v_bill_number;
EXCEPTION 
	WHEN OTHERS THEN
		RAISE EXCEPTION 'Bill % return failed: %', v_bill_number ,SQLERRM;
END $$;



