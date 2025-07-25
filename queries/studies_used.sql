SELECT COUNT(DISTINCT s.icid) AS predicted_study_count
FROM Study s
JOIN Dicom d ON d.study_id = s.uuid
LEFT JOIN view_prediction vp ON vp.dicom_id = d.uuid AND vp.is_deleted = FALSE
LEFT JOIN quality_prediction qp ON qp.dicom_id = d.uuid AND qp.is_deleted = FALSE
WHERE vp.uuid IS NOT NULL OR qp.uuid IS NOT NULL;

-- for atlas, which studies have prediction associated and therefore have been used in ai 