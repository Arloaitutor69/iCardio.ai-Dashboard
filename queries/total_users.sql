SELECT
  COUNT(DISTINCT uuid) AS total_all_time,
  COUNT(DISTINCT uuid) FILTER (
    WHERE created_at >= NOW() - INTERVAL '7 days'
  ) AS current_week
FROM "user";
