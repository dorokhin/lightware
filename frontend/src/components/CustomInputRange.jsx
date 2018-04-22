import axios from 'axios';
import React, { Component } from 'react';
import InputRange from 'react-input-range';

class CustomInputRange extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: 0,
    };

    this.ApiAddress = "http://192.168.1.109:5000/api/";
  }

  componentDidMount() {
    this.setState({
      value: this.props.value,
    });
  }
  updateStatus(id, level) {
    this.setState({
      value: level,
    });
    axios.post( this.ApiAddress + "dimmer/set/state", {"dimmer": id, "value": level})
  }

  render() {
    return (
      <InputRange
        formatLabel={value => `${value} %`}
        maxValue={100}
        minValue={0}
        value={this.state.value}
        onChange={value => this.setState({ value })}
        onChangeComplete={value => this.updateStatus(this.props.id, { value }["value"])} />
    );
  }
}

export default CustomInputRange;