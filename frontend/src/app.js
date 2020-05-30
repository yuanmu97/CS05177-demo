import React, { useState } from 'react';
import { Layout, Steps } from 'antd';

import Upload from './upload';
import Scan from './scan';
import Correct from './correct';
import Download from './download';
import './style.css';

export default function App() {
  const [image, setImage] = useState();
  const step = ((image) => {
    if (!image) return 0;
    if (!image.scanned) return 1;
    if (!image.corrected) return 2;
    return 3;
  })(image);
  const content = {
    0: <Upload onFinish={setImage} />,
    1: <Scan image={image} onFinish={setImage} />,
    2: <Correct image={image} onFinish={setImage} />,
    3: <Download image={image} onFinish={setImage} />,
  }[step];
  return (
    <Layout>
      <Layout.Header className="header">
        <Steps current={step} className="steps">
          <Steps.Step title="上传图片" />
          <Steps.Step title="检测隐私区域" />
          <Steps.Step title="编辑图片" />
          <Steps.Step title="下载图片" />
        </Steps>
      </Layout.Header>
      <Layout.Content className="content">
        {content}
      </Layout.Content>
    </Layout>
  );
};
