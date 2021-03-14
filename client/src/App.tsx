import React from 'react';
import logo from './logo.svg';
import './App.less';

import { Layout } from 'antd';

import { InputForm } from './InputForm'
import { Output } from './Output'


const { Header, Footer, Sider, Content } = Layout;

function App() {
  return (
    <div className="App">
      <Layout>
        <Header className="App-header">Prawn Farm Nutrient Model</Header>
        <Layout>
          <Sider className="App-sider" theme="light" width="300">
            <InputForm />
          </Sider>
          <Content>
            <Output />
          </Content>
        </Layout>
        <Footer>Powered by Dooles</Footer>
      </Layout>
    </div>
  );
}

export default App;
