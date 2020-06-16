import React, { useEffect, useRef, useState } from 'react';
import Axios from 'axios';
import { Button, Checkbox, Col, List, Row } from 'antd';

function rect2style(data, imgShape, imgRect) {
  return {
    position: 'fixed',
    top: data.top / imgShape.height * imgRect.height + imgRect.top,
    left: data.left / imgShape.width * imgRect.width + imgRect.left,
    height: (data.bottom - data.top) / imgShape.height * imgRect.height,
    width: (data.right - data.left) / imgShape.width * imgRect.width,
  };
}

function Rect({ data, value, onChange, ...props }) {
  return (
    <List.Item
      extra={
        <Checkbox
          checked={value>0}
          onChange={(e) => {onChange(e.target.checked ? 3 : 0)}}
        >
          消除
        </Checkbox>
      }
      {...props}
    >
      <List.Item.Meta
        title={['无', '低', '中', '高'][data.level] + '风险 - ' + data.type}
        description={data.description}
      />
    </List.Item>
  );
}

export default function Correct({ image, onFinish }) {
  const imgEl = useRef();
  const [imgShape, setImgShape] = useState();
  const [imgRect, setImgRect] = useState();
  const levels_default = {};
  for (let r of image.rects) {
    levels_default[r.id] = 0;
  }
  const [levels, setLevels] = useState(levels_default);
  const hover_default = {};
  for (let r of image.rects) {
    hover_default[r.id] = false;
  }
  const [hover, setHover] = useState(hover_default);
  useEffect(() => {
    let active = true;
    function update() {
      if (imgEl.current) {
        const { naturalHeight: height, naturalWidth: width } = imgEl.current;
        setImgShape({ height, width });
        setImgRect(imgEl.current.getBoundingClientRect());
      }
      if (active) {
        setTimeout(update, 100);
      }
    }
    setTimeout(update, 100);
    return () => {
      active = false;
    };
  }, [image]);
  function submit() {
    Axios.post(`/api/image/${image.id}/`, levels)
      .then(({data: r}) => {
        onFinish(r);
      });
  }
  return (
    <Row gutter={24} style={{ height: '100%' }}>
      <Col span={12} style={{ height: '100%' }}>
        <img
          ref={imgEl}
          src={image.file}
          style={{
            display: 'block',
            maxHeight: '100%',
            maxWidth: '100%',
            margin: 'auto',
          }}
        />
        {imgShape && imgRect ? image.rects.map((r) => (
          <div
            key={r.id}
            style={{
              ...rect2style(r, imgShape, imgRect),
              background: levels[r.id] ? 'rgba(128, 128, 128, 1)' : 'none',
              border: hover[r.id] ? '3px solid #44f' : 'none',
            }}
          />
        )) : null}
      </Col>
      <Col span={12} style={{ height: '100%', overflowX: 'auto' }}>
        <List footer={<Button type="primary" onClick={submit}>提交</Button>}>
          {image.rects.map((r) => (
            <Rect
              key={r.id}
              data={r}
              value={levels[r.id]}
              onChange={(l) => setLevels({...levels, [r.id]: l})}
              onMouseEnter={() => {hover[r.id] = true}}
              onMouseLeave={() => {hover[r.id] = false}}
            />
          ))}
        </List>
      </Col>
    </Row>
  );
};
