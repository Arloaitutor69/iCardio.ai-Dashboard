SELECT
    DATE(kc.created_at) AS group_key,
    u.first_name || ' ' || u.last_name AS user_name,
    COUNT(*) AS label_count
FROM keypoint_collection_label kc
JOIN frame f ON kc.frame_id = f.uuid
JOIN media m ON f.media_id = m.uuid
JOIN view_label vl ON m.dicom_id = vl.dicom_id
JOIN view_class vc ON vl.view_class_id = vc.uuid
JOIN "user" u ON kc.user_id = u.uuid
WHERE
    (:view_filter IS NULL OR vc.view = ANY(:view_filter))
    AND (:user_filter IS NULL OR (u.first_name || ' ' || u.last_name) = ANY(:user_filter))
    AND (:since IS NULL OR kc.created_at >= :since)
GROUP BY group_key, user_name
ORDER BY group_key ASC, user_name;
