import React from 'react';

import { OuputTable } from './Table'

  const dataSource = [
    {
      key: '1',
      day: 1,
      tan: 32,
      nox: 23,
    },
    {
      key: '2',
      day: 2,
      tan: 42,
      nox: 23,
    },
  ];

export const Output: React.FC = () => {
    return (
        <OuputTable dataSource={dataSource}/>
    )
}
