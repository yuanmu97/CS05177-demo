import React, { useEffect, useRef, useState } from 'react';
import Axios from 'axios';
import { Button, Checkbox, Popover } from 'antd';

function Rect({ data, imgShape, imgRect, value, onChange }) {
  if (data && imgShape && imgRect) {
    let className = 'edit-rect';
    className += ` edit-rect-correct-${value}`;
    className += ` edit-rect-${data.level}`;
    function f(e) {
      if (e.target.checked) {
        onChange(3);
      } else {
        onChange(0);
      }
    }
    const content = (
      <>
        <p>{data.description}</p>
        <p>类型：{data.type}</p>
        <p>风险：{['无', '低', '中', '高'][data.level]}</p>
        <p>
          <Checkbox checked={value>0} onChange={f}>
            这是隐私泄露，需要消除
          </Checkbox>
        </p>
      </>
    );
    return (
      <Popover content={content}>
        <div
          className={className}
          style={{
            top: data.top / imgShape.height * imgRect.height + imgRect.top,
            left: data.left / imgShape.width * imgRect.width + imgRect.left,
            height: (data.bottom - data.top) / imgShape.height * imgRect.height,
            width: (data.right - data.left) / imgShape.width * imgRect.width,
          }}
        />
      </Popover>
    );
  } else {
    return null;
  }
}

export default function Correct({ image, onFinish }) {
  const imgEl = useRef();
  const [imgShape, setImgShape] = useState();
  const [imgRect, setImgRect] = useState();
  const level_default = {};
  for (let r of image.rects) {
    level_default[r.id] = 0;
  }
  const [levels, setLevels] = useState(level_default);
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
    <>
      <img ref={imgEl} className="edit" src={image.file} />
      {image.rects.map((r) => (
        <Rect key={r.id} data={r} imgShape={imgShape} imgRect={imgRect} value={levels[r.id]} onChange={(l) => setLevels({...levels, [r.id]: l})} />
      ))}
      <Button type="primary" className="submit" onClick={submit}>提交</Button>
    </>
  );
};
