-- Update financial transaction table to include shipment_id
ALTER TABLE financial_transaction ADD COLUMN IF NOT EXISTS shipment_id INTEGER REFERENCES shipment(id);

-- Update expenses_general table to include shipment_id (already done)
-- ALTER TABLE expenses_general ADD COLUMN IF NOT EXISTS shipment_id INTEGER REFERENCES shipment(id);

-- Update expenses_documents table to include shipment_id (already done)  
-- ALTER TABLE expenses_documents ADD COLUMN IF NOT EXISTS shipment_id INTEGER REFERENCES shipment(id);

-- Update shipment table to include linked_expenses (already done)
-- ALTER TABLE shipment ADD COLUMN IF NOT EXISTS linked_expenses REAL DEFAULT 0.0;