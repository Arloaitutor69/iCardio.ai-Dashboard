-- dicoms_breakdown.sql
SELECT
  ds.name AS datasource,
  d.manufacturer,
  d.manufacturer_model_name AS model,
  d.type,
  CASE WHEN f.uuid IS NOT NULL THEN TRUE ELSE FALSE END AS has_media,
  d.flagged,
  DATE_TRUNC('day', d.created_at) AS date,
  COUNT(*) AS count
FROM dicom d
LEFT JOIN study s ON d.study_id = s.uuid
LEFT JOIN datasource ds ON s.datasource_id = ds.uuid
LEFT JOIN frame f ON d.uuid = f.media_id
WHERE
  (:datasource IS NULL OR ds.name = ANY(:datasource)) AND
  (:manufacturer IS NULL OR d.manufacturer = ANY(:manufacturer)) AND
  (:model IS NULL OR d.manufacturer_model_name = ANY(:model)) AND
  (:type IS NULL OR d.type = ANY(:type)) AND
  (:has_media IS NULL OR (:has_media = TRUE AND f.uuid IS NOT NULL) OR (:has_media = FALSE AND f.uuid IS NULL)) AND
  (:flagged IS NULL OR d.flagged = :flagged)
GROUP BY ds.name, d.manufacturer, d.manufacturer_model_name, d.type, has_media, d.flagged, DATE_TRUNC('day', d.created_at)
ORDER BY count DESC;
