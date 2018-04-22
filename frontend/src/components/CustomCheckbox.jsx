import axios from 'axios';
import React, { Component } from 'react';
import { Checkbox } from 'semantic-ui-react'


class CustomCheckbox extends Component {
  constructor() {
    super();
    this.state = {
      checked: false
    };
      this.ApiAddress = "http://192.168.1.109:5000/api/";
  }

  componentDidMount() {
    this.setState({
      checked: this.props.checked,
    });
  }

  updateStatus(id) {
    this.setState({
      checked: !this.state.checked,
    });
    axios.post( this.ApiAddress + "channel/set/state", {"channel": id, "state": !this.state.checked})


  }

  render() {
    return (

      <Checkbox id={this.props.id}
                label={this.props.label}
                checked={this.state.checked}
                onClick={() => this.updateStatus(this.props.id)}
      />

    );
  }
}

export default CustomCheckbox;
