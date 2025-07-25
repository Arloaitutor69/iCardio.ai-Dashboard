
SELECT
  CASE
    WHEN r.decision IS NULL THEN 'Pending'
    ELSE 'Completed'
  END AS group_key,
  COUNT(*) AS value
FROM
  review r
WHERE
  r.is_deleted = FALSE
  AND (
    :start_date IS NULL OR r.updated_at >= :start_date
  )
  AND (
    :end_date IS NULL OR r.updated_at <= :end_date
  )
GROUP BY
  group_key
ORDER BY
  value DESC;
