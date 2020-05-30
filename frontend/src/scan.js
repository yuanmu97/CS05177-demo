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
  function scan() {
    const rects = [
      {
        type: 'A',
        description: '图片的左上角容易泄露隐私',
        top: 0,
        left: 0,
        right: 100,
        bottom: 100,
        level: 1,
      },
      {
        type: 'B',
        description: '这里更容易泄露隐私',
        top: 100,
        left: 100,
        right: 200,
        bottom: 200,
        level: 3,
      },
    ];
    Axios.post(`/api/image/${image.id}/rects/`, { rects });
  }
  return (
    <>
      <Result title="正在检测隐私区域" icon={<Spin size="large" />} />
      <Button type="primary" className="submit" onClick={scan}>模拟检测</Button>
    </>
  );
};
