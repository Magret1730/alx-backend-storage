-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Cursor to loop through each user
    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Declare variables to hold the computed total weighted score and total weight
        DECLARE total_weighted_score DECIMAL(10, 2);
        DECLARE total_weight INT;

        -- Compute the total weighted score and the total weight for the current user
        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO total_weighted_score, total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Update the users table with the computed average weighted score
        UPDATE users
        SET average_score = IFNULL(total_weighted_score / total_weight, 0)
        WHERE id = user_id;

    END LOOP;

    CLOSE cur;
END //

DELIMITER ;
