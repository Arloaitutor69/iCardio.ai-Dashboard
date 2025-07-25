SELECT
  COUNT(*) AS total_all_time,
  COUNT(*) FILTER (
    WHERE created_at >= NOW() - INTERVAL '7 days'
  ) AS current_week
FROM study;
