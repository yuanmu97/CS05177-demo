import React, { useState } from 'react';
import { Upload as U } from 'antd';
import { CloudUploadOutlined } from '@ant-design/icons';

export default function Upload({ onFinish }) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(false);
  function onChange({ file }) {
    setUploading(file.status === 'uploading');
    setError(file.status === 'error');
    if (file.status === 'done') {
      onFinish(file.response);
    }
  }
  return (
    <U.Dragger
      action="/api/image/"
      name="image"
      accept="image/*"
      showUploadList={false}
      onChange={onChange}
    >
      <p className="ant-upload-drag-icon">
        <CloudUploadOutlined />
      </p>
      <p className="ant-upload-text">
        {error ? '上传出错，请重新选择' : uploading ? '正在上传…' : '点击或拖动图片到这里'}
      </p>
    </U.Dragger>
  );
};
