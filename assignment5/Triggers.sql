-- 1. Trigger to automatically add a new payment row when an order is placed:

CREATE TRIGGER add_payment_on_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
  INSERT INTO payment (mode, details, order_id, customer_id, time_date)
  VALUES ('cash', 'unspecified', NEW.order_id, NEW.customer_id, NOW());
END;


-- 2. Trigger to prevent deletion of a category that is associated with any products:

CREATE TRIGGER prevent_category_deletion
BEFORE DELETE ON category
FOR EACH ROW
BEGIN
  DECLARE product_count INT;
  SELECT COUNT(*) INTO product_count FROM product WHERE product.category_id = OLD.category_id;
  IF product_count > 0 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Cannot delete a category that is associated with products';
  END IF;
END;

-- 3. Trigger to update the status of a delivery partner when a new order is assigned to them:

CREATE TRIGGER update_delivery_partner_status
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
  UPDATE delivery_partner
  SET status = 'Unavailable'
  WHERE delivery_partner.delivery_partner_id = NEW.delivery_partner_id;
END;

