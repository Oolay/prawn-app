import React from 'react';

import { Table } from 'antd';

import { CONC_COLUMNS } from './tableCols'

  interface Props {
      dataSource: any
  }

  export const OuputTable: React.FC<Props> = ({ dataSource }) => {

    return (
        <Table columns={CONC_COLUMNS} dataSource={dataSource} />
    )
  };
