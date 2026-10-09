ALTER TABLE users ADD COLUMN has_pending_payments BOOLEAN NOT NULL DEFAULT false;

UPDATE users u SET has_pending_payments = EXISTS (
    SELECT 1 FROM rentals r 
    WHERE r.user_id = u.id
    AND r.status = 'Active'
);