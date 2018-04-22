import React, { Component } from 'react';
import Menu from './components/Menu'
import Controls from './components/Controls'

class App extends Component {
  constructor() {
    super();
    this.state = {
      loading: true,
    };
  }

  render() {
    return (
      <div>
        <Menu title="Lightware"/>
        <Controls />
      </div>
    );
  }
}

export default App;
