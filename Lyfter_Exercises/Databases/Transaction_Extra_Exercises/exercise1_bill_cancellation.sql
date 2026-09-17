SET search_path TO transactions_exercises;

DO $$
DECLARE
	v_bill_number INTEGER:= 1006;
	v_bill_status VARCHAR(10);
	v_bill_id INTEGER;
	v_bill_line RECORD;
BEGIN
	-- Verify invoice exists
	SELECT id, status INTO v_bill_id, v_bill_status FROM bills 
	WHERE bill_number = v_bill_number
	FOR UPDATE; -- Block the bill to avoid other users making updates on it.

	IF NOT FOUND THEN
		RAISE EXCEPTION 'The bill % does not exist.', v_bill_number;
	END IF;
	
	-- Verify invoice is status "Pending"
	IF v_bill_status <> 'Pending' THEN
		RAISE EXCEPTION 'The bill % has status %, it must have status Pending', v_bill_number, v_bill_status;
	END IF;

	-- Verify there are not delivered products in the invoice
	IF EXISTS (SELECT 1 FROM bill_lines WHERE bill_id = v_bill_id AND delivered) THEN
		RAISE EXCEPTION 'The bill % has delivered products and cannot be cancelled, review the bill lines first.', v_bill_number;
	END IF;

	-- Change bill status to "Cancelled"
	UPDATE bills SET status = 'Cancelled' WHERE id = v_bill_id;

	-- Get the existing bill_lines
	FOR v_bill_line IN 
		SELECT product_id, quantity, delivered FROM bill_lines
		WHERE bill_id = v_bill_id
		ORDER BY product_id
		FOR UPDATE -- Block the bill_lines to avoid other users making changes on them.
	LOOP
		IF NOT v_bill_line.delivered THEN
			-- Update the product stock
			UPDATE products 
			SET stock_available = stock_available + v_bill_line.quantity 
			WHERE id = v_bill_line.product_id;
		END IF;	
	END LOOP;
	
	RAISE NOTICE 'Bill % cancelled successfully.', v_bill_number;
EXCEPTION 
	WHEN OTHERS THEN
		RAISE 'Bill % cancellation failed: %', v_bill_number, SQLERRM
		USING ERRCODE = SQLSTATE;
END $$;

-- The "ROLLBACK;" is not necessary here because any unhandled error inside the DO block rolls back all automatically.
