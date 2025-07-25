SELECT
  ds.name AS group_key,
  COUNT(*) AS value
FROM
  frame f
JOIN
  media m ON f.media_id = m.uuid
JOIN
  dicom d ON m.dicom_id = d.uuid
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
