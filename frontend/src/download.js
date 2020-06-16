import React from 'react';
import { Button } from 'antd';

export default function Download({ image, onFinish }) {
  return (
    <>
      <img
        src={image.corrected}
        style={{
          display: 'block',
          maxHeight: '100%',
          maxWidth: '100%',
          margin: 'auto',
        }}
      />
      <Button
        type="primary"
        onClick={() => {onFinish(null)}}
        style={{
          position: 'absolute',
          bottom: 12,
          right: 12,
        }}
      >
        再传一张
      </Button>
    </>
  );
};
