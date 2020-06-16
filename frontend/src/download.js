import React from 'react';
import { Button } from 'antd';

export default function Download() {
  function reload() {
    location.reload();
  }
  return (
    <>
      <p>download</p>
      <Button type="primary" onClick={reload}>再传一张</Button>
    </>
  );
};
