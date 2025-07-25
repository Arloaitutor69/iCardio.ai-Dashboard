SELECT COUNT(DISTINCT s.icid) AS labeled_study_count
FROM study s
JOIN dicom d ON d.study_id = s.uuid
JOIN media m ON m.dicom_id = d.uuid
JOIN frame f ON f.media_id = m.uuid
LEFT JOIN segmentation_label sl ON sl.frame_id = f.uuid
LEFT JOIN keypoint_collection_label kcl ON kcl.frame_id = f.uuid
LEFT JOIN phase_label pl ON pl.frame_id = f.uuid
WHERE sl.uuid IS NOT NULL OR kcl.uuid IS NOT NULL OR pl.uuid IS NOT NULL;


 -- for atlas