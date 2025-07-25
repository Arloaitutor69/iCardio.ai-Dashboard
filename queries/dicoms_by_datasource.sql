SELECT
  ds.name AS group_key,
  COUNT(*) AS value
FROM
  dicom d
JOIN
  study s ON d.study_id = s.uuid
JOIN
  datasource ds ON s.datasource_id = ds.uuid
WHERE
  ds.name IS NOT NULL
GROUP BY
  ds.name
ORDER BY
  value DESC;
