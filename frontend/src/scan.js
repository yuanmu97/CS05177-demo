import React, { useEffect } from 'react';
import Axios from 'axios';
import { Button, Result, Spin } from 'antd';

export default function Scan({ image, onFinish }) {
  useEffect(() => {
    let active = true;
    function update() {
      Axios.get(`/api/image/${image.id}/`)
        .then(({data: r}) => {
          if (r.scanned) {
            onFinish(r);
          } else if (active) {
            setTimeout(update, 1000);
          }
        });
    }
    setTimeout(update, 1000);
    return () => {
      active = false;
    };
  }, [image]);
  return (
    <Result title="正在检测隐私区域" icon={<Spin size="large" />} />
  );
};
