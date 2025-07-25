SELECT
  sc.value AS group_key,
  COUNT(DISTINCT sl.frame_id) AS value
FROM
  segmentation_label sl
JOIN
  segmentation_class sc ON sl.segmentation_class_id = sc.uuid
WHERE
  sc.value IS NOT NULL
GROUP BY
  sc.value
ORDER BY
  value DESC;
