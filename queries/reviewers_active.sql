SELECT
  u.first_name || ' ' || u.last_name AS group_key,
  COUNT(r.uuid) AS value,
  MAX(r.updated_at) AS last_review_time
FROM
  review r
JOIN
  "user" u ON r.user_id = u.uuid
WHERE
  r.is_deleted = FALSE
  AND (
    :cutoff_time IS NULL 
    OR r.updated_at >= :cutoff_time
  )
GROUP BY
  group_key
ORDER BY
  last_review_time DESC;
