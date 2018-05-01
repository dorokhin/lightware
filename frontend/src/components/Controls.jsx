import axios from 'axios';
import React, { Component } from 'react';
import { Label } from 'semantic-ui-react'
import CustomCheckbox from './CustomCheckbox'
import CustomInputRange from './CustomInputRange'


class Controls extends Component {
  constructor() {
    super();
    this.state = {
      status: true,
      checked: false,
      channels: { "switches": {} },
      dimmableChannels: { "dimmer": {} }
    };
    this.ApiAddress = "https://lightware.dorokhin.moscow/api/";
  }


  componentDidMount() {
    axios.get( this.ApiAddress + "channel/status")
    .then(res => {
      const channels = res.data;
      this.setState({
        channels,
        loading: false
      })
    })
    .catch(function (error) {
      console.log(error);
    });


    axios.get( this.ApiAddress + "dimmer/status")
    .then(res => {
      const dimmableChannels = res.data;
      this.setState({
        dimmableChannels
      });
    })
    .catch(function (error) {
      console.log(error);
    })
  }

  static updateStatus() {
    console.log("click");

  }

  render() {
    return (
      <div className="ui main text container">
        <div className="ui segment">
          <p>Channel control switch</p>

          <div className="ui form">
          {
            Object.keys(this.state.channels.switches).map(
              item =>
              this.state.channels.switches[item].active ?
                <div key={this.state.channels.switches[item].id} className="inline field">
                  <div className="ui toggle checkbox">
                    <CustomCheckbox
                      id={this.state.channels.switches[item].id}
                      label="-"
                      toggle
                      checked={ this.state.channels.switches[item].state }
                      onClick={() => this.updateStatus()}
                    />

                  </div>
                  <Label color={this.state.channels.switches[item].color} horizontal>{this.state.channels.switches[item].name}</Label>
                </div> : '' )}

            <div className="ui hidden divider"></div>

            {
              Object.keys(this.state.dimmableChannels.dimmer).map(
                item =>
                  this.state.dimmableChannels.dimmer[item].active ?
                    <div key={this.state.dimmableChannels.dimmer[item].id} className="inline field">

                      <div className="ui padded segment no-scroll">
                        <h4 className="ui horizontal divider header"><i className="idea icon"></i>{this.state.dimmableChannels.dimmer[item].name}</h4>
                          <CustomInputRange
                            id={this.state.dimmableChannels.dimmer[item].id}
                            value={this.state.dimmableChannels.dimmer[item].value}
                          />
                      </div>

                      <div className="ui hidden divider"></div>
                    </div> : '' )}

                <div className="inline field">

                </div>
            <div className="ui hidden divider"></div>
          </div>
        </div>
      </div>
    );
  }
}

export default Controls;
