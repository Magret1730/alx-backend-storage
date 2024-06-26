--  SQL script that lists all bands with Glam rock as their main style, ranked by their longevity


SELECT band_name as band_name,
	IFNULL(split - formed, YEAR('2022-01-01') - formed)  AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
