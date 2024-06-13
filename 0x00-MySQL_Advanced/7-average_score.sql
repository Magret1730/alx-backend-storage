-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes
-- and store the average score for a student. NB: An average score can be a decimal

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
	IN user_id INT
)
BEGIN
	-- Declare a variable to hold the computed average score
	DECLARE avg_score DECIMAL(10, 2);

	-- Compute the average score for the specified user_id
	SELECT AVG(score)
	INTO avg_score
	FROM corrections
	WHERE user_id = user_id;
	
	-- update the users table with the computed average score
	UPDATE users
	SET average_score = avg_score
	WHERE id = user_id;
END //

DELIMITER ;
