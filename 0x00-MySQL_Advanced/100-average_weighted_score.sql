-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
	IN user_id INT
)
BEGIN
	-- Declare a variable to hold the computed average score
	DECLARE total_weighted_score DECIMAL(10, 2);
	DECLARE total_weight INT;

	-- Compute the average score for the specified user_id
	-- Compute the total weighted score and the total weight
    	SELECT SUM(c.score * p.weight), SUM(p.weight)
    	INTO total_weighted_score, total_weight
    	FROM corrections c
    	JOIN projects p ON c.project_id = p.id
    	WHERE c.user_id = user_id;

    	-- Update the users table with the computed average weighted score
    	UPDATE users
    	SET average_score = total_weighted_score / total_weight
    	WHERE id = user_id;
END //

DELIMITER ;
