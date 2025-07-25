WITH
  perspective_studies AS (
    SELECT DISTINCT s.uuid AS study_id
    FROM Study s
    JOIN Dicom d ON d.study_id = s.uuid
    JOIN view_label vl ON vl.dicom_id = d.uuid
    WHERE vl.is_deleted = FALSE
  ),
  segmentation_studies AS (
    SELECT DISTINCT s.uuid AS study_id
    FROM Study s
    JOIN Dicom d ON d.study_id = s.uuid
    JOIN media m ON m.dicom_id = d.uuid
    JOIN frame f ON f.media_id = m.uuid
    JOIN segmentation_label sl ON sl.frame_id = f.uuid
    WHERE sl.is_deleted = FALSE
  ),
  reviewed_studies AS (
    SELECT DISTINCT CAST(r.object_id AS uuid) AS study_id
    FROM Review r
    WHERE r.object_type = 'study'
      AND r.is_deleted = FALSE
      AND r.object_id IS NOT NULL
  ),
  fully_labeled AS (
    SELECT s.uuid
    FROM Study s
    WHERE s.uuid IN (SELECT study_id FROM perspective_studies)
      AND s.uuid IN (SELECT study_id FROM segmentation_studies)
      AND s.uuid IN (SELECT study_id FROM reviewed_studies)
  )

SELECT 
  COUNT(DISTINCT f.uuid) AS fully_labeled_count,
  COUNT(DISTINCT s.uuid) AS total_studies,
  ROUND(
    COUNT(DISTINCT f.uuid) * 100.0 / NULLIF(COUNT(DISTINCT s.uuid), 0), 2
  ) AS percent_fully_labeled
FROM Study s
LEFT JOIN fully_labeled f ON f.uuid = s.uuid;

-- for atlas, returns fully labeled study with QA, perspective, and segmentation
-- cant test yet bc there are not enough reviews 