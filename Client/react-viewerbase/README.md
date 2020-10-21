### Install

```bash
// with npm
npm i react-viewerbase --save-exact

// with yarn
yarn add react-viewerbase --exact

```

新版本的react-viewerbase:

```bash
//with npm 
npm i @ohif/ui --save-exact
//with yarn
yarn add @ohif/ui --exact
```

### Usage

**使用的是react语法模式,render()方法返回UI组件**

```javascript
import React, { Component } from 'react';
import { LayoutButton } from 'react-viewerbase';

class Example extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedCell: {
        className: 'hover',
        col: 1,
        row: 1,
      },
    };
  }
  render() {
    return (
      <LayoutButton
        selectedCell={this.state.selectedCell}
        onChange={cell => this.setState({ selectedCell: cell })}
      />
    );
  }
}
```

### 



