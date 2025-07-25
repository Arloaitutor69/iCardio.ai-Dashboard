SELECT
  COUNT(DISTINCT frame_id) AS total_all_time,
  COUNT(DISTINCT frame_id) FILTER (
    WHERE created_at >= NOW() - INTERVAL '7 days'
  ) AS current_week
FROM segmentation_label;
