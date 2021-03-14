import React from 'react';

import { Form, Input } from 'antd'

export const InputForm: React.FC = () => {

    return (
        <>
            <Form
                labelCol={{ span: 15, offset: 1 }}
                wrapperCol={{ span: 5 }}
                layout="horizontal"
                size='small'
            >
                
                <Form.Item label="Pond production area (ha)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond area (ha)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond depth (m)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond cycle (days)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond production area (ha)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond area (ha)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond depth (m)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond cycle (days)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond production area (ha)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond area (ha)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond depth (m)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond cycle (days)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond production area (ha)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond area (ha)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond depth (m)">
                    <Input type='number' />
                </Form.Item>

                <Form.Item label="Pond cycle (days)">
                    <Input type='number' />
                </Form.Item>

            </Form>
        </>
    )
};
