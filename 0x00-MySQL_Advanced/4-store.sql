-- SQL script that creates a trigger that decreases the quantity of an item after adding a new order.
DROP TRIGGER IF EXISTS decrease_quantity_item_after_adding_new_order;

DELIMITER //

CREATE TRIGGER decrease_quantity_item_after_adding_new_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
	UPDATE items
	SET quantity = quantity - NEW.number
	WHERE name = New.item_name;
END //

DELIMITER ;
