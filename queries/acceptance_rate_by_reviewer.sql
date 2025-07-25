SELECT
  u.first_name || ' ' || u.last_name AS group_key,
  r.decision AS sub_group,
  COUNT(*) AS value
FROM
  review r
JOIN
  "user" u ON r.user_id = u.uuid
WHERE
  r.is_deleted = FALSE
  AND r.decision IS NOT NULL
  AND (
    :cutoff_time IS NULL
    OR r.updated_at >= :cutoff_time
  )
GROUP BY
  group_key, sub_group
ORDER BY
  group_key;
